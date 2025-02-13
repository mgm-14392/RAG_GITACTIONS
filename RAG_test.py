import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict


OPENAI_KEY = os.environ["OPENAI_API_KEY"]
LANGSMITH_KEY = os.environ["LANGSMITH_API_KEY"]
MISTRAL_KEY = os.environ["MISTRAL_API_KEY"]

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_KEY
os.environ["MISTRAL_API_KEY"] = MISTRAL_KEY

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

if not os.environ.get("LANGSMITH_TRACING"):
  os.environ["LANGSMITH_TRACING"] = getpass.getpass("Enter API key for Lansmith: ")

if not os.environ.get("MISTRAL_API_KEY"):
  os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

# Componenets
# chat model : OpenAI
# Embeddings model : HuggingFaceEmbeddings
# Vector store: FAISSS

# Chat model
#llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Chat model 2
llm = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Vector store
index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# Load and chunk contents of the blog
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
#print(f"Split blog post into {len(all_splits)} sub-documents.")

# Index chunks
document_ids = vector_store.add_documents(documents=all_splits)
#print(document_ids[:3])

# Loads a predifined prompt template from LangChain Hub
# This template structures the input for the LLM like: Context, Question and Answer
# It ensures the LlM recieves both the question and relevant retrieved context
prompt = hub.pull("rlm/rag-prompt")

# Define state structure for application
# it is a dictionary with a fixed set of keys, each
# associated with a specific type. It provides static
# type checking while retaining the flexibility of standard
# dictionaries at runtime
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    """
    This function retrieves relevant documents from a vector store
    by searching for documents most similar to the question

    input: TypedDict with question, context and answer as keys
    ouput: retrived document stored in context
    """
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    """
    This function generates the answer using the LLM, that
    receives the formated prompt with context and answer
    input: TypedDict with question, context and answer as keys
    output : generated answer
    """
    docs_content = "\n\n".join(doc.page_content for doc in state["context"]) # create formated string from retrieved documents
    messages = prompt.invoke({"question": state["question"], "context": docs_content}) # format the prompt using the retrieved context and question
    response = llm.invoke(messages) # send the formatted promp to the LLM and get response
    return {"answer": response.content} # return the generated answer


# Build the application workflow
# StateGraph(State) creates a workflow (state machine) where functions (retrieve and generate are steps), it also automatically
# merges returned dicts into state
# add_seauence([retrieve, generate])  defines the execution order: retrieve context, generate answer based on retrieved context
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
# add_edge(START, "retrieve") specifies that the process starts with the retrieve step
graph_builder.add_edge(START, "retrieve")
# graph_builder.compile(): Finalizes the workflow.
graph = graph_builder.compile()

#How Does This Work in Practice?
# User asks a question → "What is Task Decomposition?"
# Retrieve step → Searches the vector store for documents about the Task Decomposition.
# Generate step → Constructs a prompt with the retrieved context and asks the LLM to answer.
# LLM generates an answer 
# Final output is returned.

response = graph.invoke({"question": "What is Task Decomposition?"})
#print(response["answer"])