from setuptools import setup, find_packages

setup(
    name="server_extension",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jupyter_server",
        "google-generativeai",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "google.generativeai"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A JupyterLab extension for generating questions and summarizing URLs",
    keywords="jupyter,jupyterlab,jupyterlab-extension",
    url="https://github.com/dstl-lab/ContentGen/tree/main",
    project_url="https://github.com/dstl-lab/ContentGen/tree/main",
    include_package_data=True,
    python_requires=">=3.6",
    platforms="Linux, Mac OS X, Windows",
    entry_points={
        "jupyter_server.extensions": [
            "server_extension = server_extension:_load_jupyter_server_extension"
        ],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
    data_files=[
        ("share/jupyter/labextensions/server-extension", [
            "install.json",
        ]),
    ],
)
