# **DocSemantic: Semantic Document Search System**

## **Overview**

**DocSemantic** is a semantic search system that allows users to upload documents (PDFs or text files) and query them using natural language. This system is powered by AI techniques to understand and retrieve relevant sections from the documents based on the user's query. It is built using a combination of Flask for the backend, React for frontend, Pinecone for efficient vector storage and retrieval, and pre-trained sentence transformers for generating document embeddings.

## **Features**

- **Upload Documents**: Upload multiple PDF or text files to index for searching.
- **Semantic Query**: Perform natural language searches on the uploaded documents.
- **Relevant Results**: Retrieve the three most contextually relevant answers from your document set.

## **Project Architecture**

1. **Frontend**: 
   - React-based interface for document upload and query submission.
   - Components:
     - `FileUpload`: Allows users to upload PDF or text files for indexing.
     - `QueryForm`: Allows users to enter a natural language query and see results from the indexed documents.

2. **Backend**:
   - **Flask**: Serves the API endpoints for file upload and querying.
   - **Pinecone**: Stores vector embeddings of the documents and handles fast semantic search.
   - **Sentence Transformers**: Converts the uploaded documents and queries into embeddings for comparison.

3. **API Endpoints**:
   - `/upload`: Upload and process documents.
   - `/query`: Submit queries to retrieve answers from uploaded documents.

## **Technologies Used**

- **React**: Frontend framework.
- **Flask**: Backend web framework.
- **Pinecone**: Vector database for fast and scalable search.
- **Sentence Transformers**: Pre-trained models for converting text into embeddings.
- **PyPDF2**: For parsing and extracting text from PDF documents.
- **OpenAI**: For handling advanced language processing tasks.

## **Setup Instructions**

### **Prerequisites**

Ensure you have the following installed:
- Python 3.8 or higher
- Node.js (for running the frontend)
- [Pinecone account and API key](https://www.pinecone.io/)
- OpenAI API Key
- Install the requirements.txt

### **Local Setup**
1. **Clone the Repository**
2. **Backend Setup**:
     - Make a virutal environment: python -m venv venv
     - Install the python dependencies (requirements.txt): pip install -r requirements.txt
     - Add your api keys for pinecone and openai
     - Run the backend: python trial.py
3. **Frontend Setup**:
     - Go into the frontend folder: cd Frontend
     - Install the modules: npm install
     - Satrt the front end: npm start

Now use the application!

## **Images**
## **Assumptions**
## **Future Scope**
   

