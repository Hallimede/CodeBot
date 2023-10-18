# CodeBot


CodeBot is designed to provide a Q&A system based on a code project. It utilizes a document retrieval chain to retrieve relevant information from a given project directory, and then uses the language model to generate answers to user questions based on the retrieved information.


# Setup

1. Make sure you have the necessary dependencies installed. You can install them using pip: 

```bash
$ pip install -r requirements.txt
```

2. Set up your OpenAI API key by creating a file named "key.yaml" and adding your API key in the following format:

```yaml
OPENAI_API_KEY: "${YOUR_API_KEY}"
# OPENAI_API_MODEL: "gpt-4"
OPENAI_API_MODEL: "gpt-3.5-turbo"
```

3. Provide the project directory path to search for relevant information. The code will recursively go through the directory and retrieve information from valid files with specific extensions (e.g. .py, .js, .css, .html, .txt, ...). You can provide the project directory path when prompted.
