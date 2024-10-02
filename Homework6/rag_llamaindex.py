"""imports"""
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.ollama import Ollama

# Step 1: Loading the files
documents = SimpleDirectoryReader('./knowledge_base').load_data()

# Step 2: Load embedding model
embed_model = HuggingFaceEmbedding()

# Step 3: Indexing and storing embedding to disk
# create client
db = chromadb.PersistentClient(path='./database')
chroma_collection = db.get_or_create_collection('handbook_collection')

# create vector store
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# index the documents
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model
)

# Step 4: Load embeddings from disk
db2 = chromadb.PersistentClient(path='./database')
chroma_collection = db2.get_or_create_collection('handbook_collection')
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model
)

# Step 5: Initialize the Llama model
llm = Ollama(model="llama3.2", request_timeout=500.0)

# Step 6: Query the system
query_engine = index.as_query_engine(llm=llm)


query = "What is the policy for drugs?"

response = query_engine.query(query)

print(response)
