import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  ILayoutRestorer
} from '@jupyterlab/application';

import { MainAreaWidget } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { INotebookTracker } from '@jupyterlab/notebook';
import { requestAPI } from './handler.js';
import '../style/index.css';
import { NotebookPanel } from '@jupyterlab/notebook';

// Add these at the top level, before the plugin definition
let isFollowupMode = false;
let previousQuestion = "";
let lastInsertedCellIndex = -1;
let notebookDirectory: string = ''; // current notebook directory
let notebookName: string = ''; // current notebook name
let currentRowId: number | null = null;
let userDecision: 'applied' | 'canceled' | 'followed_up' | null = null;

/**
 * Initialization data for the server-extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'server-extension:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [INotebookTracker],
  optional: [ILayoutRestorer],
  activate: (app: JupyterFrontEnd, notebookTracker: INotebookTracker, restorer: ILayoutRestorer | null) => {
    console.log('JupyterLab extension server-extension is activated ::))');

    const newWidget = () => {
      const content = new Widget();
      content.node.classList.add('chatbot-panel');

      // Create chat container first
      const chatContainer = document.createElement('div');
      chatContainer.classList.add('chat-container');

      // Create header inside chat container
      const chatHeader = document.createElement('div');
      chatHeader.classList.add('chat-header');

      // Add notebook name and model info
      const notebookNameDiv = document.createElement('div');
      notebookNameDiv.classList.add('notebook-name-display');
      notebookNameDiv.textContent = 'No notebook open';

      const modelInfo = document.createElement('div');
      modelInfo.classList.add('model-info');
      modelInfo.textContent = 'gemini-2.0-flash';

      chatHeader.appendChild(notebookNameDiv);
      chatHeader.appendChild(modelInfo);
      chatContainer.appendChild(chatHeader);

      // Create messages container
      const messagesContainer = document.createElement('div');
      messagesContainer.classList.add('messages-container');
      chatContainer.appendChild(messagesContainer);

      // Create input container
      const inputContainer = document.createElement('div');
      inputContainer.classList.add('input-container');

      // Add text input
      const inputBox = document.createElement('textarea');
      inputBox.classList.add('chat-input');
      inputBox.placeholder = 'Generate a practice question based on selected code...';

      // Create mode toggle button
      const modeToggleButton = document.createElement('button');
      modeToggleButton.textContent = '📝';
      modeToggleButton.classList.add('mode-toggle');
      modeToggleButton.title = 'Toggle between Question Generation and URL Summary';
      let isUrlMode = false;

      // Simplify mode toggle functionality
      modeToggleButton.addEventListener('click', () => {
        isUrlMode = !isUrlMode;
        isFollowupMode = false; // Reset follow-up mode when switching modes
        
        if (isUrlMode) {
          modeToggleButton.textContent = '🔗';
          inputBox.placeholder = 'Enter URL to summarize content...';
        } else {
          modeToggleButton.textContent = '📝';
          inputBox.placeholder = 'Generate a practice question based on selected code...';
        }
      });

      // Simplify interface assembly
      inputContainer.appendChild(modeToggleButton);
      inputContainer.appendChild(inputBox);
      chatContainer.appendChild(inputContainer);

      // Append chat container to content
      content.node.appendChild(chatContainer);

      // Create button container for Apply/Cancel
      const buttonContainer = document.createElement('div');
      buttonContainer.id = "chat-buttons-container"; 
      content.node.appendChild(buttonContainer);

      // Modify the handleMessage function to handle follow-up questions
      const handleMessage = async () => {
        const message = inputBox.value.trim();
        if (message) {
          // Show user message immediately
          addMessageToChat('user', message);
          inputBox.value = ''; // Clear input
          
          // Show loading indicator
          showLoadingIndicator();
          
          try {
            // Get current notebook
            const currentNotebook = notebookTracker.currentWidget;
            const notebookContent: { index: number; content: string }[] = [];

            updateNotebookDirectory();
            
            const notebookCodeCells: {
              index: number;          // Cell index in the notebook
              content: string;        // Raw code content of the cell
              isDataLoading: boolean; // Whether this cell loads a dataset
              dataframeVar: string | null; // Variable name of the loaded DataFrame (if any)
            }[] = [];
          
            const dataLoadingPattern = /(pd\.read_(csv|excel|json|html)\(|sns\.load_dataset\(|pd\.DataFrame\(|pd\.DataFrame\.from_dict\(|pd\.DataFrame\.from_records\()/; // Regular expression pattern to detect DataFrame creation
            const dataLoadingCells: number[] = []; // List to store indices of dataset-loading cells
            if (currentNotebook && currentNotebook.content) {
              const notebook = currentNotebook.content;
              const notebookModel = notebook?.model;

              if (notebookModel) {
                try {
                  const cells = notebookModel.cells;
                  const notebookWidget = currentNotebook.content; // Get notebook widget properly
                  if (!notebookWidget) {
                    addMessageToChat('system', 'Error: No active notebook');
                    return;
                  }

                  // Get selected cells using notebook's active cell index
                  const activeIndex = notebookTracker.currentWidget?.content.activeCellIndex ?? 0;
                  const selectedCells = [cells.get(activeIndex)]; // Use active cell as selected cell

                  // Handle cells differently based on mode
                  if (isUrlMode) {
                    // URL mode - process all cells
                    for (let i = 0; i < cells.length; i++) {
                      const cell = cells.get(i);
                      notebookContent.push({
                        index: i + 1,
                        content: cell.sharedModel.getSource()
                      });
                    }
                  } else {
                    // Question mode - require cell selection
                    if (selectedCells.length === 0) {
                      addMessageToChat('system', '⚠️ Warning: Please select cells to generate a question about their content');
                      return;
                    }
                    
                    for (let i = 0; i < cells.length; i++) {
                      const cell = cells.get(i);
                      const cellContent = cell.sharedModel.getSource();

                      notebookContent.push({
                          index: i + 1,
                          content: cellContent
                      });
                      
                      if (cell.type === 'code') {

                        const loadsData = dataLoadingPattern.test(cellContent);

                        let dataframeVar: string | null = null; // DataFrame variable name
                        if (loadsData) { 

                          dataLoadingCells.push(i + 1);

                          const dataLoadingPattern = /(\b\w+)\s*=\s*(?:pd\.read_\w+\(|sns\.load_dataset\(|pd\.DataFrame\()/;
                          const assignmentMatch = cellContent.match(dataLoadingPattern);

                          if (assignmentMatch) {
                              dataframeVar = assignmentMatch[1];  // Extract variable name
                          }
                        }
                        console.log('DataFrame detected: ' + dataframeVar);

                        notebookCodeCells.push({
                          index: i + 1,
                          content: cellContent,
                          isDataLoading: loadsData,
                          dataframeVar: dataframeVar
                        });
                      }
                    }
                  }

                  // For URL mode, we don't need cell content <-- Ylesia: actually we do
                  console.log(isUrlMode ? 'URL mode - processing all cells' : 'Selected cells content:', selectedCells);

                  // Prepare the request body with follow-up information if needed
                  let relevantContent;
                  if (!isUrlMode) {
                          // Get only selected cells
                          // relevantContent = selectedCells.map((cell, index) => ({
                          //     index: index + 1,
                          //     content: cell.model.sharedModel.getSource()
                          // send up to past 5 ' #', or headers of notebook content for the topic range from the active cell index
                          const activeIndex = notebookTracker.currentWidget?.content.activeCellIndex ?? 0;
                          const cells = notebookModel.cells;
                          const relevantCells = [];
                          let headerCount = 0;
                          for (let i = activeIndex; i >= 0; i--) {
                              const cell = cells.get(i);
                              if (cell.type === 'markdown' && cell.sharedModel.getSource().startsWith('#')) {
                                  headerCount++;
                              }
                              if (headerCount >= 5) {
                                  break;
                              }
                              relevantCells.unshift({
                                  index: i + 1,
                                  content: cell.sharedModel.getSource()
                              });
                          }
                          relevantContent = relevantCells;
                          console.log("Relevant Content: " + JSON.stringify(relevantContent));
                  }
                  
                  const requestBody = {
                    message: message,
                    notebookContent: relevantContent || notebookContent,
                    promptType: isUrlMode ? 'summary' : 'question',
                    selectedCell: !isUrlMode ? selectedCells[selectedCells.length - 1].sharedModel.getSource() : null,
                    questionType: !isUrlMode ? 'coding' : null,
                    activeCellIndex: notebookTracker.currentWidget?.content.activeCellIndex ?? 0,
                    isFollowup: isFollowupMode,
                    previousQuestion: previousQuestion,
                    notebookName: notebookName,
                    ...(isUrlMode ? {} : { 
                      notebookDirectory,
                      notebookCodeCells
                    })
                  };
                  console.log("Request body:", requestBody);
                  
                  // log user decision if is a follow up
                  if (isFollowupMode && currentRowId !== null && userDecision === null) {
                    await requestAPI('log-usage', {
                      method: 'POST',
                      body: JSON.stringify({ row_id: currentRowId, user_decision: 'followed_up' })
                    });
                  }
                  

                  // Making POST request to message endpoint
                  const response = await requestAPI<any>('message', {
                    method: 'POST',
                    body: JSON.stringify(requestBody)
                  });

                  console.log("Working up to here");
                  // console.log(response.reply)
                  console.log(response)
                  
                  // record row_id
                  currentRowId = response.row_id;

                  // Process response and update UI
                  const croppedString = response.reply.substring(7, response.reply.length - 4);
                  const llmOutput = JSON.parse(croppedString);
                  let returnedIndex;
                  if (isFollowupMode){
                    returnedIndex = notebookTracker.currentWidget?.content.activeCellIndex;
                  }
                  else{
                    returnedIndex = notebookTracker.currentWidget?.content.activeCellIndex + 1;
                  }
                  const summary = llmOutput.summary;

                  // Hide loading indicator before showing response
                  hideLoadingIndicator();
                  
                  // Show response
                  const safeIndex = returnedIndex;
                  addMessageToChat('assistant', 'Location: ' + safeIndex + '\n\nSummary: ' + summary);
                  
                  console.log(`Inserting new cell at index ${safeIndex} with summary:`, summary);

                  const pageTitle = llmOutput.title || inputBox.value;  // Use title if available, otherwise fallback to URL

                  // If in follow-up mode, remove the previous cell before inserting the new one
                  if (isFollowupMode && lastInsertedCellIndex >= 0 && notebookModel) {
                    // Remove the previous cell
                    notebookModel.sharedModel.deleteCell(lastInsertedCellIndex);
                    // Remove existing buttons from chat area
                    removeChatButtons();
                  }

                  // Insert the new cell
                  notebookModel.sharedModel.insertCell(safeIndex, {
                    cell_type: 'markdown',
                    source: formatQuestionCell(pageTitle, summary),
                    metadata: { 
                      temporary: true,
                    }
                  });

                  // Update tracking variables for potential follow-up
                  lastInsertedCellIndex = safeIndex;
                  previousQuestion = summary;
                  isFollowupMode = true; // Enable follow-up mode after generating content

                  if (notebookTracker.currentWidget && notebookTracker.currentWidget.content) {
                    notebookTracker.currentWidget.content.activeCellIndex = safeIndex;
                  }

                  attachButtonsBelowChat(safeIndex, notebookModel);
                  setTimeout(() => attachButtonListeners(safeIndex, notebookModel), 100);
                } catch (error) {
                  // Hide loading indicator on error
                  hideLoadingIndicator();
                  console.error('Failed to get response:', error);
                  addMessageToChat('system', 'Error: Failed to get response');
                  isFollowupMode = false; // Reset follow-up mode on error
                }
              }
            }
          } catch (error) {
            // Hide loading indicator on error
            hideLoadingIndicator();
            console.error('Error in handleMessage:', error);
            addMessageToChat('system', 'Error: Failed to process request');
            isFollowupMode = false; // Reset follow-up mode on error
          }
        }
      };

      // Add event listeners
      // sendButton.addEventListener('click', handleMessage);
      inputBox.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) { // Allow Shift+Enter for new lines
          event.preventDefault(); // Prevent default to avoid new line
          if (isUrlMode) {
            // URL mode validation
            if (inputBox.value.trim()) {
              console.log('Valid URL:', inputBox.value);
              handleMessage();
            } else {
              addMessageToChat('system', 'Error: Please input a valid link to get response');
            }
          } else {
            // Question mode - no URL validation needed
            if (inputBox.value.trim()) {
              handleMessage();
            } else {
              addMessageToChat('system', 'Error: Please enter a question');
            }
          }
        }
      });
    
      // Function to add messages to chat with better code formatting
      const addMessageToChat = (role: string, text: string) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', role);
        
        // For assistant messages, format code blocks
        if (role === 'assistant') {
          // Simple regex to identify Python code blocks
          const formattedText = text.replace(
            /```python\s*([\s\S]*?)```/g,
            '<pre class="python-code"><code>$1</code></pre>'
          );
          messageDiv.innerHTML = formattedText.replace(/\n/g, "<br>");
        } else {
          messageDiv.innerHTML = text.replace(/\n/g, "<br>");
        }
        
        // Add to messages container
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom of messages container
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      };

      // Add a loading indicator function
      const showLoadingIndicator = () => {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('chat-message', 'system', 'loading-indicator');
        loadingDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div> Generating response...';
        loadingDiv.id = 'loading-indicator';
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      };

      // Remove loading indicator
      const hideLoadingIndicator = () => {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
          loadingIndicator.remove();
        }
      };

      // Update notebook name
      const updateNotebookName = () => {
        // Get current notebook
        const currentNotebook = notebookTracker.currentWidget;

        if (currentNotebook instanceof NotebookPanel) {
          const name = currentNotebook.title.label;
          notebookName = name;

          // Get notebook name
          notebookNameDiv.textContent = `Notebook: ${notebookName}`;
        } else {
          notebookNameDiv.textContent = 'No notebook detected...';
        }
      };

      const updateNotebookDirectory = () => {
        const currentNotebook = notebookTracker.currentWidget;
    
        if (currentNotebook && currentNotebook.context) {
            const notebookPath = currentNotebook.context.path;
            // console.log("notebookPath: " + notebookPath);
            // notebookDirectory = notebookPath.substring(0, notebookPath.lastIndexOf('/'));
            
            const lastSlashIndex = notebookPath.lastIndexOf('/');
            // If '/' is found, extract the directory path; otherwise, default to "."
            notebookDirectory = lastSlashIndex !== -1 
                ? notebookPath.substring(0, lastSlashIndex) 
                : ".";  // Current directory if no `/` is found

            console.log("Notebook Directory updated:", notebookDirectory);
        }
      };
    
    
      // Listen for changes in the active notebook
      notebookTracker.currentChanged.connect(() => {
        updateNotebookName();
        updateNotebookDirectory;
      });

      // Initial update
      updateNotebookName();
      updateNotebookDirectory;

      const widget = new MainAreaWidget({ content });
      widget.id = 'chatbot-widget';
      widget.title.label = 'Chat';
      widget.title.closable = true;

      // Add widget to the right panel
      app.shell.add(widget, 'right');

      if (restorer) {
        restorer.add(widget, 'chatbot-widget');
      }

      return widget;
    };

    // Create and display the widget
    newWidget();
  }
};

// Add these helper functions
const removeChatButtons = () => {
  const panel = document.getElementById("chat-buttons-container");
  if (panel) {
    panel.innerHTML = "";  // Clear the buttons from the UI
  }
};

const attachButtonsBelowChat = (index: number, notebookModel: any) => {
  console.log(`Adding buttons below chat for cell at index ${index}`);

  // Ensure the chat buttons container exists
  let panel = document.getElementById("chat-buttons-container");
  if (!panel) {
    console.error("Chat buttons container not found!");
    return;
  }

  // Create Apply button
  const applyBtn = document.createElement("button");
  applyBtn.textContent = "✅ Apply";
  applyBtn.className = "apply-btn";
  applyBtn.onclick = () => applyChanges(index, notebookModel);

  // Create Cancel button
  const cancelBtn = document.createElement("button");
  cancelBtn.textContent = "❌ Cancel";
  cancelBtn.className = "cancel-btn";
  cancelBtn.onclick = () => cancelChanges(index, notebookModel);

  // Add buttons to the panel
  panel.appendChild(applyBtn);
  panel.appendChild(cancelBtn);
};

const attachButtonListeners = (index: number, notebookModel: any) => {
  // Implementation details
};

const applyChanges = async (index: number, notebookModel: any) => {
  console.log(`Applying changes for cell at index ${index}`);
  
  // Remove temporary metadata
  if (notebookModel.sharedModel.cells[index]) {
    delete notebookModel.sharedModel.cells[index].metadata.temporary;
  }
  
  // Reset follow-up mode
  isFollowupMode = false;
  previousQuestion = "";
  lastInsertedCellIndex = -1;
  
  // Remove the buttons from the chat area
  removeChatButtons();

  // log user decision
  userDecision = 'applied';
  await requestAPI('log-usage', {
    method: 'POST',
    body: JSON.stringify({ row_id: currentRowId, user_decision: 'applied' })
  });
};

const cancelChanges = async (index: number, notebookModel: any) => {
  console.log(`Cancelling changes and deleting cell at index ${index}`);
  
  // Remove the inserted summary cell
  notebookModel.sharedModel.deleteCell(index);
  
  // Reset follow-up mode
  isFollowupMode = false;
  previousQuestion = "";
  lastInsertedCellIndex = -1;
  
  // Remove the buttons from the chat area
  removeChatButtons();

  // log user decision
  userDecision = 'canceled';
  await requestAPI('log-usage', {
    method: 'POST',
    body: JSON.stringify({ row_id: currentRowId, user_decision: 'canceled' })
  });
};

// Update the helper function to format the cell content
const formatQuestionCell = (title: string, content: string): string => {
  // Split the content into question and answer parts
  const parts = content.split(/Answer:\s*```python/);
  
  if (parts.length < 2) {
    // If we can't split properly, return the original content
    return `### ${title}\n\n${content}`;
  }
  
  // Extract question and answer
  let question = parts[0].replace('Question:', '').trim();
  let answer = '```python' + parts[1];
  
  // Format with orange alert for question and collapsible section for answer
  return `<div class="alert alert-warning">
  <h3>Question 🤔 ${title}</h3>
  
  ${question}
</div>

<details>
  <summary><strong>Click to reveal answer</strong></summary>
  
${answer}
</details>`;
};

export default plugin;
