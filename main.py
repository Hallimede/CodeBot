import os
import yaml

from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


def is_valid_file(file_path, excluded_paths):
    return all(excluded_path not in file_path for excluded_path in excluded_paths)

def has_valid_extension(file_name, valid_extensions):
    return file_name.endswith(valid_extensions)

def load_env_vars(file):
    with open(file, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        os.environ.update({k: v for k, v in yaml_data.items() if isinstance(v, str)})

file_extensions_to_check = (".py", ".js", ".css", ".html", ".txt")
excluded_paths = ["/env/", "/venv/", "/node_modules/"]
load_env_vars("key.yaml")
        
# project_name = input("Enter project name: ")

# root_dir = f"workspace/{project_name}/{project_name}"

docs = []

root_dir = input("Enter project directory: ")

for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        if has_valid_extension(file, file_extensions_to_check) and is_valid_file(dirpath, excluded_paths):
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                docs.extend(loader.load_and_split())
            except Exception as e:
                print(e)

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
print(f"{len(texts)}")

embeddings = OpenAIEmbeddings(
                deployment="text-embedding-ada-002",
                openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
                chunk_size=1,
            )

db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever()
# retriever.search_kwargs["k"] = 3

model = ChatOpenAI(
            temperature=1.0,
            model_name=os.environ.get("OPENAI_API_MODEL", ""),
            openai_api_key=os.environ.get("OPENAI_API_KEY", "gpt-3.5-turbo"),
        )

qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

# questions = ["how to use playwright"]

# for question in questions:
#     result = qa({"question": question, "chat_history": chat_history})
#     chat_history.append((question, result["answer"]))
#     print(f"-> **Question**: {question} \n")
#     print(f"**Answer**: {result['answer']} \n")

chat_history = []

while True:
    question = input("Enter question: ")
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    print(f"\n\n-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
