# from groq import Groq
import google.generativeai as genai
import json
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import sys
import traceback
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import re  # Add import for regex
import sqlite3
from datetime import datetime, timezone

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

gemini_api_key = str(os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# set up SQLite database
db_path = os.path.join(os.path.dirname(__file__), "contentgen_logs.db")
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        prompt_type TEXT,
        question_type TEXT,
        notebook_name TEXT,
        notebook_dir TEXT,
        selected_cell TEXT,
        user_input TEXT,
        previous_question TEXT,
        prompt_template TEXT,
        llm_response TEXT,
        user_decision TEXT
    )
"""
)
con.commit()
con.close()

prompt_summary = """
# Task: Webpage Summarization and Notebook Integration

## Input
1. Notebook content: The Jupyter notebook that needs to be augmented with webpage information
2. Webpage text: Content extracted from the URL the user provided

## Instructions
1. Analyze the notebook content to understand its topic and structure
2. Examine the webpage text and extract the key information
3. Create a concise, well-structured summary of the webpage content
4. Determine the most logical location in the notebook to insert this summary
   - Find a contextually appropriate position based on topic relevance
   - Consider section breaks, headers, or related content

## Response Format
Return ONLY a valid JSON string with these three fields:
{
  "indexToInsert": <integer index where the summary should be inserted>,
  "title": "<title of the webpage or a descriptive headline>",
  "summary": "<your concise, formatted summary of the webpage content>"
}

## Note
Your summary should be comprehensive enough to convey the key points but brief enough to fit well within the notebook flow.
"""

prompt_question = """
# Task Definition
You are an educational content generator analyzing a Jupyter notebook lecture to create related practice exercises.

# Context
I will provide you with:
- The complete notebook content including text and code cells
- The currently selected cell that should serve as a reference
- Variables and outputs from executed code cells
- The question type being requested

# Instructions
1. Analyze the notebook content to understand the educational concepts
2. Focus on the selected cell's structure and purpose
3. Generate a new code example that:
   - Do not repeat the same code as the selected cell!
   - Follows a similar structure to the selected cell
   - Implements related concepts with minor but relevant differences 
   - Uses existing datasets/DataFrames from the executed variables
   - No need to import any libraries, espeically pandas or numpy!!!!!!!!!!!!

4. Create a concise lecture question that:
   - Is directly related to the notebook content before the insertion point
   - Has your generated code as the correct answer
   - Is appropriate for the specified question type

# Response Format
Respond with ONLY a valid JSON string in this exact format:
{{
  "indexToInsert": notebook.activeCellIndex,
  "title": "Brief descriptive title for this question",
  "summary": "Question: [Your question here]\\n\\nAnswer:\\n```python\\n[Your code here]\\n```"
}}

# Notebook Details
Notebook content: {notebook_content}
Current Selected Cell: {selected_cell}
Code cells: {code_cells}
Executed code variables: {executed_variables}
Question type: {question_type}
User question: {user_input}
"""

# Add a new prompt for follow-up questions
prompt_followup = """
# Task Definition
You are an educational content generator refining a previously generated practice exercise.

# Context
I will provide you with:
- The complete notebook content
- The previously generated question and answer
- The user's follow-up request for modifications

# Instructions
1. Analyze the user's follow-up request to understand what changes they want
2. Modify the previously generated question and answer code to address their request
   - Implements related concepts with minor but relevant differences 
   - No need to import any libraries, espeically pandas or numpy! 
   - Continue using the same dataframes and columns as in the original question unless the user specifically requests otherwise
   - Maintain consistency with the data structures used in the original question
3. Common requests include:
   - Making the question easier or harder
   - Focusing on a different aspect of the concept
   - Simplifying or expanding the code

# Response Format
Respond with ONLY a valid JSON string in this exact format:
{{
  "indexToInsert": notebook.activeCellIndex,
  "title": "Brief descriptive title for this question",
  "summary": "Question: [Your modified question here]\\n\\nAnswer:\\n```python\\n[Your modified code here]\\n```"
}}

# Details
Notebook content: {notebook_content}
Previous question and answer: {previous_question}
User follow-up request: {user_input}
"""

executed_results = {}


import os
import sys
import traceback
from io import StringIO


def clean_code(code):
    """
    Removes Jupyter magic commands (e.g., %%timeit) and any other invalid notebook syntax.
    """
    cleaned_lines = []
    for line in code.split("\n"):
        if not line.strip().startswith("%%"):  # Remove cell magic commands
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def execute_code(code, directory):
    """
    Executes Python code in the specified directory and captures both
    output (print statements) and variables defined in the execution.
    """

    # Save the original working directory
    original_directory = os.getcwd()

    # Redirect stdout and stderr to capture output
    output_buffer = StringIO()
    error_buffer = StringIO()

    # Dictionary to store the execution namespace
    local_vars = {}

    try:
        # Change to the specified directory if provided
        if directory:
            os.chdir(directory)
            if directory not in sys.path:
                sys.path.insert(0, directory)
                print("Added directory to paths")

        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir())
        print("sys.path:", sys.path)

        print("Flushing stdout...")
        sys.stdout.flush()
        sys.stderr.flush()

        code = clean_code(code)

        # Use redirect_stdout() and redirect_stderr() to safely capture output
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            print("Executing code...")
            exec(code, globals())

        print("Execution completed!")

        # Extract captured output and errors
        output = output_buffer.getvalue().strip()
        print("Output:", output)
        error = error_buffer.getvalue().strip()
        print("Error:", error)

    except Exception as e:
        print(f"Exception: {e}")
        error = traceback.format_exc()
        output = ""

    finally:
        # Restore stdout, stderr, and working directory
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        os.chdir(original_directory)

    # Remove built-in functions and modules
    executed_results = {k: v for k, v in globals().items() if not k.startswith("__")}
    print(
        "To be returned:",
        {"output": output, "error": error, "variables": executed_results},
    )

    return {"output": output, "error": error, "variables": executed_results}


def validate_url(url):
    """
    Validates if a string is a proper URL.
    Returns (is_valid, error_message)
    """
    # Simple URL validation using regex
    url_pattern = re.compile(
        r"^(?:http|https)://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ipv4
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    if not url_pattern.match(url):
        return False, "Invalid URL format"

    return True, ""


def fetch_url_content(url):
    """
    Fetches and extracts main content from a URL.
    Returns (success, content_or_error)
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.decompose()

        # Extract page title
        title = soup.title.string if soup.title else url

        # Extract text from remaining tags
        text = soup.get_text(separator=" ", strip=True)

        # Clean up text: remove excessive whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Get a reasonable length of text (first 8000 chars to avoid token limits)
        text = text[:8000]

        return True, {"title": title, "content": text}

    except requests.exceptions.RequestException as e:
        return False, f"Failed to fetch URL: {str(e)}"
    except Exception as e:
        return False, f"Error processing URL content: {str(e)}"


class MessageHandler(APIHandler):
    @tornado.web.authenticated
    async def post(self):
        try:
            global prompt_summary
            global prompt_question
            global prompt_followup
            global executed_results

            # Get all variables upfront
            input_data = self.get_json_body()
            user_input = input_data.get("message", "")
            nt_content = input_data.get("notebookContent", "")
            user_notebook = str(nt_content)
            prompt_type = input_data.get("promptType", "")
            selected_cell = input_data.get("selectedCell", "")
            question_type = input_data.get("questionType", "")
            code_cells = input_data.get("notebookCodeCells", [])
            is_followup = input_data.get("isFollowup", False)
            previous_question = input_data.get("previousQuestion", "")
            notebook_directory = input_data.get("notebookDirectory", "")
            notebook_name = input_data.get("notebookName", "")

            # Create a local prompt variable - no global modification
            if prompt_type == "summary":
                current_prompt = prompt_summary
                prompt_template_name = "prompt_summary"  # for db
            elif is_followup:
                current_prompt = prompt_followup
                prompt_template_name = "prompt_followup"  # for db
            else:
                current_prompt = prompt_question
                prompt_template_name = "prompt_question"  # for db

            # insert to db
            try:
                con = sqlite3.connect(db_path)
                cur = con.cursor()
                cur.execute(
                    """
                    INSERT INTO logs (
                        timestamp,
                        prompt_type,
                        question_type,
                        notebook_name,
                        notebook_dir,
                        selected_cell,
                        user_input,
                        previous_question,
                        prompt_template,
                        llm_response,
                        user_decision
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        datetime.now(timezone.utc).isoformat(),
                        prompt_type,
                        question_type,
                        notebook_name,
                        notebook_directory,
                        selected_cell,
                        user_input,
                        previous_question,
                        prompt_template_name,
                        None,  # LLM response (to be updated later)
                        None,  # user_decision (to be updated later)
                    ),
                )

                row_id = cur.lastrowid
                con.commit()
                con.close()
            except Exception as e:
                print("Initial DB insert failed:", e)
                row_id = None

            # Handle URL validation and content fetching for summary mode
            webpage_content = None
            if prompt_type == "summary":
                # Validate URL
                is_valid, error_msg = validate_url(user_input)
                if not is_valid:
                    self.set_status(400)
                    self.finish(json.dumps({"error": error_msg}))
                    return

                # Fetch URL content
                success, result = fetch_url_content(user_input)
                if not success:
                    self.set_status(400)
                    self.finish(json.dumps({"error": result}))
                    return

                webpage_content = result
                print(
                    f"Successfully fetched URL content. Title: {webpage_content['title']}"
                )
                print(f"Content length: {len(webpage_content['content'])} characters")

            if current_prompt == prompt_question:
                try:
                    # Handle code execution for questions
                    if question_type != "conceptual":

                        print(f"Notebook directory: {notebook_directory}")

                        notebook_code_cells = input_data.get("notebookCodeCells", [])
                        print(f"Number of code cells: {len(notebook_code_cells)}")

                        if notebook_code_cells:
                            execution_result = execute_code(
                                "\n\n".join(
                                    cell["content"] for cell in notebook_code_cells
                                ),
                                notebook_directory,
                            )
                            print("Code execution result:", execution_result)
                            executed_results = execution_result.get("variables", {})
                        else:
                            executed_results = {}
                except Exception as e:
                    print("Error during code execution:", e)
                    traceback.print_exc()  # Print full stack trace
                    self.set_status(500)
                    self.finish(
                        json.dumps({"error": f"Code execution failed: {str(e)}"})
                    )
                    return

                try:
                    # Construct question prompt without truncation
                    current_prompt = prompt_question.format(
                        notebook_content=user_notebook,
                        selected_cell=selected_cell,
                        code_cells=str(code_cells),
                        executed_variables=str(executed_results),
                        question_type=question_type,
                        user_input=user_input,
                    )
                except Exception as e:
                    print("Error constructing question prompt:", e)
                    traceback.print_exc()
                    self.set_status(500)
                    self.finish(
                        json.dumps({"error": f"Failed to construct prompt: {str(e)}"})
                    )
                    return

            try:
                # Construct prompt based on type
                if is_followup:
                    current_prompt = prompt_followup.format(
                        notebook_content=user_notebook,
                        previous_question=previous_question,
                        user_input=user_input,
                    )
                elif current_prompt == prompt_question:
                    current_prompt = prompt_question.format(
                        notebook_content=user_notebook,
                        selected_cell=selected_cell,
                        code_cells=str(code_cells),
                        executed_variables=str(executed_results),
                        question_type=question_type,
                        user_input=user_input,
                    )
                # For summary prompt, add the webpage content
                elif prompt_type == "summary":
                    # Append the webpage content to the prompt
                    current_prompt = f"{current_prompt}\n\nWebpage URL: {user_input}\nWebpage Title: {webpage_content['title']}\nWebpage Content: {webpage_content['content']}"

                print("Final prompt:", current_prompt)

                # Make API call
                print("\n=== LLM Request Details ===")
                print(f"Prompt Type: {prompt_type}")
                print(
                    f"Question Type: {question_type if prompt_type == 'question' else 'N/A'}"
                )
                print(
                    f"Using Selected Cells: {input_data.get('useSelectedCells', False)}"
                )
                print(f"User Input: {user_input}")
                print("\nFull Prompt being sent to LLM:")
                print("------------------------")
                print(current_prompt)
                print("------------------------\n")

                llm_response = model.generate_content(current_prompt)
                print("\n=== LLM Response ===")
                print(llm_response.text)
                print("------------------------\n")

                output = llm_response.text

                if row_id is not None:
                    try:
                        con = sqlite3.connect(db_path)
                        cur = con.cursor()
                        cur.execute(
                            "UPDATE logs SET llm_response = ? WHERE id = ?",
                            (output, row_id),
                        )
                        con.commit()
                        con.close()
                        print(f"Logged LLM response to row {row_id}")
                    except Exception as e:
                        print("Failed to update llm_response in DB:", e)

                # Construct and send response
                response_data = {"reply": output, "status": "success", "row_id": row_id}
                print("Sending response:", response_data)
                self.finish(json.dumps(response_data))

            except Exception as e:
                print("Error during API call or response handling:", e)
                traceback.print_exc()
                self.set_status(500)
                self.finish(
                    json.dumps(
                        {
                            "error": f"API or response handling failed: {str(e)}",
                            "prompt_length": len(current_prompt),
                        }
                    )
                )
                return

        except Exception as e:
            print("Outer most layer exception:", e)
            traceback.print_exc()
            self.set_status(500)
            self.finish(json.dumps({"error": f"Request failed: {str(e)}"}))

    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({"status": "Message service is running"}))


class LogUsageHandler(APIHandler):
    @tornado.web.authenticated
    def post(self):
        try:
            input_data = self.get_json_body()
            row_id = input_data.get("row_id")
            decision = input_data.get("user_decision")

            print(f"row_id: {row_id}")
            print(f"decision: {decision}")
            print("About to insert user decision...")

            if row_id is None or decision not in ["applied", "canceled", "followed_up"]:
                self.set_status(400)
                self.finish(json.dumps({"error": "Invalid input"}))
                return

            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute(
                "UPDATE logs SET user_decision = ? WHERE id = ?", (decision, row_id)
            )
            con.commit()
            con.close()

            print(f"Added user decision ({decision}) for row {row_id}.")

            self.finish(json.dumps({"status": "logged", "row_id": row_id}))
        except Exception as e:
            print("Error in LogUsageHandler:", e)
            self.set_status(500)
            self.finish(json.dumps({"error": str(e)}))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    message_pattern = url_path_join(base_url, "server-extension", "message")
    log_pattern = url_path_join(base_url, "server-extension", "log-usage")
    handlers = [
        (message_pattern, MessageHandler),
        (log_pattern, LogUsageHandler),
    ]
    web_app.add_handlers(host_pattern, handlers)
