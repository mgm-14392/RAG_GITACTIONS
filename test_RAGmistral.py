import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document
from rag_mistral import RAGSystem  # Assuming the class is in rag_mistral.py
import time


@pytest.fixture
def setup_rag_system():
    """Fixture to initialize the RAGSystem for tests."""
    # Mock the .docx file loading to return a valid Document
    with patch("rag_mistral.DocxDocument") as mock_docx:
        # Mock the paragraphs in the .docx file
        mock_paragraphs = [MagicMock(text="This is a test recipe.")]
        mock_docx.return_value.paragraphs = mock_paragraphs

        # Initialize the RAGSystem with the mocked .docx file
        rag_system = RAGSystem(docx_file_path="recipes.docx")
        return rag_system


# Unit tests for the RAGSystem class

def test_vector_store_add(setup_rag_system):
    """Test adding documents to the vector store."""
    doc = Document(page_content="This is a test document.")
    rag_system = setup_rag_system
    doc_id = rag_system.vector_store.add_documents([doc])
    assert len(doc_id) == 1  # Should return a list with one ID


def test_vector_store_initialization(setup_rag_system):
    """Test that the vector store is initialized correctly."""
    rag_system = setup_rag_system
    vector_store = rag_system.vector_store
    assert vector_store is not None  # Check that it's initialized
    assert hasattr(vector_store, "embedding_function")  # Check for embedding function


def test_vector_store_retrieve(setup_rag_system):
    """Test document retrieval from the vector store."""
    doc = Document(page_content="Artificial Intelligence is evolving.")
    rag_system = setup_rag_system
    rag_system.vector_store.add_documents([doc])
    retrieved_docs = rag_system.vector_store.similarity_search("What is AI?")
    assert len(retrieved_docs) > 0  # It should return at least one document


# Tests for the RAG workflow (integration tests)

def test_full_pipeline(setup_rag_system):
    """Test the full RAG pipeline (retrieve + generate)."""
    state = {"question": "What is Task Decomposition?", "context": [], "answer": ""}
    response = setup_rag_system.graph.invoke(state)
    assert "answer" in response
    assert isinstance(response["answer"], str)
    assert len(response["answer"]) > 0  # Ensure it generates a response


def test_retrieve_function(setup_rag_system):
    """Test the retrieval function."""
    state = {"question": "What is Task Decomposition?", "context": [], "answer": ""}
    result = setup_rag_system.retrieve(state)
    assert "context" in result
    assert isinstance(result["context"], list)
    assert len(result["context"]) > 0  # Should retrieve at least one document


def test_generate_function(setup_rag_system):
    """Test the generate function."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = MagicMock(content="Mocked LLM response")

    setup_rag_system.llm = mock_llm
    
    state = {
        "question": "What is Task Decomposition?",
        "context": [Document(page_content="Task decomposition is...")],
        "answer": "",
    }
    result = setup_rag_system.generate(state)
    assert "answer" in result
    assert result["answer"] == "Mocked LLM response"


# Performance tests ensure the system is efficient

def test_retrieval_speed(setup_rag_system):
    """Test the speed of the retrieval function."""
    state = {"question": "How does RAG work?", "context": [], "answer": ""}
    start_time = time.time()
    setup_rag_system.retrieve(state)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 5.0  # Ensure retrieval is under 5 seconds


def test_generation_speed(setup_rag_system):
    """Test the speed of the generation function."""
    state = {"question": "What is Task Decomposition?", "context": [], "answer": ""}
    start_time = time.time()
    setup_rag_system.generate(state)
    elapsed_time = time.time() - start_time
    assert elapsed_time < 5.0  # Response should be generated in under 5 seconds