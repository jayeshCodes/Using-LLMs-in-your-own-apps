from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


# Step 1: Loading the files
loader = UnstructuredFileLoader('./undergraduate_handbook.pdf')
documents = loader.load()

# Step 2: Split the text into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=5000,
    chunk_overlap=500
)

texts = text_splitter.split_documents(documents)

# Step 3: Load embedding model
embeddings = HuggingFaceEmbeddings()

# Step 4: Initialize Chroma database
db = Chroma.from_documents(texts, embeddings)

# Step 5: Initialize the Llama model
llm = Ollama(model="llama3.2")

system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
retriever=db.as_retriever()
chain = create_retrieval_chain(
    retriever,
    question_answer_chain
    )

# Step 6: Query the system
query = "Is there a dress code?"
response = chain.invoke({"input": query})


print(response['answer'])