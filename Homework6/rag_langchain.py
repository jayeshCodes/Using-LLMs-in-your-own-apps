from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.ollama import Ollama as LlamaIndexOllama

# from langchain_community.embeddings import LangchainEmbedding
from langchain_chroma import Chroma
from langchain_community.llms import Ollama as LangChainOllama

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from llama_index.llms.ollama import Ollama

# Step 1: Loading the files (if needed)
# documents = SimpleDirectoryReader('./knowledge_base').load_data()

# Step 2: Load embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Wrap the llama_index embedding model for LangChain
# langchain_embeddings = LangchainEmbedding(embed_model)

# Initialize Chroma database
db = Chroma(persist_directory="./database", embedding_function=embed_model)

# Create retriever
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Create Ollama language model - llama3.2
llm = Ollama(model="llama3.2")

# Create prompt template
template = """Answer the question based only on the following context and extract out a meaningful answer. \
Please write in full sentences with correct spelling and punctuation. If it makes sense, use lists. \
If the context doesn't contain the answer, just respond that you are unable to find an answer.

CONTEXT: {context}

QUESTION: {question}

ANSWER:"""
prompt = ChatPromptTemplate.from_template(template)

# Create the RAG chain using LCEL with prompt printing and streaming output
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Function to ask questions
def ask_question(question):
    print("Answer:\n")
    full_answer = ""
    for chunk in rag_chain.stream(question):
        print(chunk, end="", flush=True)
        full_answer += chunk
    print("\n")
    return full_answer

# Example usage
if __name__ == "__main__":
    while True:
        user_question = input("Ask a question (or type 'quit' to exit): ")
        if user_question.lower() == 'quit':
            break
        answer = ask_question(user_question)
        print("\nFull answer received. Length:", len(answer))