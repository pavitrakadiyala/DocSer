import os
import time
import pinecone
from uuid import uuid4
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import asyncio
import concurrent.futures

# # Set API keys
PINECONE_API_KEY = 'add key' #add
OPENAI_KEY = 'add key' #add

# Set up environment variables
os.environ['OPENAI_API_KEY'] = OPENAI_KEY #add key
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY #add key

# Initialize Pinecone 
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = pinecone.Pinecone(api_key=pinecone_api_key)
index_name = "one-vector-vsc2"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

# Create index if it doesn't exist
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)


index = pc.Index(index_name)

# Initialize embeddings using Hugging Face model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Function to extract text from a PDF
def pdf_to_documents(pdf_file_path):
    reader = PdfReader(pdf_file_path)
    documents = []
    file_name = os.path.basename(pdf_file_path)  
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            document = Document(page_content=text, metadata={"source": file_name, "page_number": page_num + 1})
            documents.append(document)
    return documents

# Function to extract text from a .txt file
def txt_to_documents(txt_file_path):
    documents = []
    file_name = os.path.basename(txt_file_path)  
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        if text:
            document = Document(page_content=text, metadata={"source": file_name})
            documents.append(document)
    return documents

# Function to chunk documents
def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=100)
    chunked_documents = []
    for document in documents:
        chunks = text_splitter.split_text(document.page_content)
        for chunk in chunks:
            chunked_doc = Document(page_content=chunk, metadata=document.metadata)
            chunked_documents.append(chunked_doc)
    return chunked_documents

# Store documents in Pinecone
def store_documents_in_pinecone(chunked_documents):
    uuids = [str(uuid4()) for _ in range(len(chunked_documents))]
    vector_store.add_documents(documents=chunked_documents, ids=uuids)

# process the PDF or TXT file in the background
async def process_file_async(file_path, file_type):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        if file_type == 'pdf':
            documents = await loop.run_in_executor(pool, pdf_to_documents, file_path)
        elif file_type == 'txt':
            documents = await loop.run_in_executor(pool, txt_to_documents, file_path)
        chunked_documents = await loop.run_in_executor(pool, chunk_documents, documents)
        await loop.run_in_executor(pool, store_documents_in_pinecone, chunked_documents)
    return "Processed"

# Function to create and run the retrieval QA chain
async def ask_question_async(query):
    # document retrieval
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}) 
    loop = asyncio.get_event_loop()
    relevant_documents = await loop.run_in_executor(None, retriever.get_relevant_documents, query)

    # chat-based LLM for final answer generation
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Load the QA chain
    qa_chain = load_qa_chain(llm, chain_type="stuff")

    # Prepare inputs 
    inputs = {
        "question": query,
        "input_documents": relevant_documents
    }
    
    #  QA chain
    response = await loop.run_in_executor(None, qa_chain.invoke, inputs)
    
    # Format response 
    answer_text = response.get('output_text', 'No relevant information found.')
    
    # output 
    formatted_answer = {
        "answer": answer_text,
        "documents": [
            {
                "content": doc.page_content[:200],  # first 200 characters for preview
                "full_content": doc.page_content,  
                "metadata": {
                    "source": doc.metadata.get("source", "unknown"),
                    "page_number": doc.metadata.get("page_number", "N/A")
                }
            }
            for doc in relevant_documents[:3]  # Return top 3 most similar
        ]
    }
    
    return formatted_answer

# Flask setup
app = Flask(__name__)
CORS(app)  # Enable CORS 

app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'

# Render the index HTML page (your frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading files
@app.route('/upload', methods=['POST'])
async def upload_file():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"})

    files = request.files.getlist('files')  
    if len(files) == 0:
        return jsonify({"error": "No files selected"})

    processing_tasks = []

    for file in files:
        if file and (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Determine file type and process 
            file_type = 'pdf' if file.filename.endswith('.pdf') else 'txt'
            task = asyncio.ensure_future(process_file_async(file_path, file_type))
            processing_tasks.append(task)
    
    await asyncio.gather(*processing_tasks)

    return jsonify({"message": "Files uploaded and processed successfully!"})

# Route for querying documents
@app.route('/query', methods=['POST', 'OPTIONS'])
async def query_file():
    if request.method == 'OPTIONS':
        return jsonify({"message": "CORS preflight"}), 200

    data = request.get_json()
    query = data.get('query', '')

    if query:
        answer = await ask_question_async(query)

        return jsonify({
            "answer": answer['answer'],
            "documents": answer['documents']
        })

    return jsonify({"error": "No query provided"}), 400

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
