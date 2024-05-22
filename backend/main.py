import time
#import scripts
import vertexai
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from src.uploadpoc.retrivalengine import ask
from src.uploadpoc.ragsystem import upload
from src.utility.functionstore import wrap 
from langchain_community.document_loaders import  DirectoryLoader


app = FastAPI()

# Allow only the specified origin (replace with your frontend's actual origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG System!"}
###__________________________________________CHILD BOT END POINTS___________________________####
#chat with child bot
@app.post("/query")
async def context_chat(payload : dict)  -> dict:
    #send the query to llm
    try:
        message = payload.get("message")
        response = ask(message)
        response = {"ragsystem_response": response}
        return response
    except Exception as e:
        return { "error": str(e)}
        #raise HTTPException(status_code=500, detail=str(e))
     
    
max_file_size_bytes = 10 * 1024 * 1024
#get summarization with from child bot
@app.post("/upload")
async def upload_context(file: UploadFile = File(...)):
    
    try:
        file_path =f"./resources/uploads/{file.filename}"
        print(file_path)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        # Call the method to update the vector store index
        
    except Exception as e:
        return { "error": str(e)}
        #raise HTTPException(status_code=500, detail=str(e))
    upload(file_path)
    return {"message": "Upload successful"}


@app.get("/summarize")
async def summarize() -> dict:
    try:
        #summarize
        response = ask("summarize the finnacial data provided for icici bank")
        response = {"ragsystem_summarize": response}
        return response
    except Exception as e:
        return { "error": str(e)}

"""
###__________________________________________PARENT BOT END POINTS___________________________####
from src.chatpoc.retrivalengine import parent_chat
@app.post("/chat")
async def chat(payload: dict) -> dict:
    try:
        message = payload.get("message")
        response = parent_chat(message)
        return {"ragsystem_response": response}
    except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))
        return { "error": str(e)}

###__________________________________________UTILITY END POINTS___________________________####
## save the docuements to rag system
@app.post("/persist")
async def persist_document()-> dict:
    try:
        ##call the persist storage function
        return {"message": "Document saved successfully"}
    except Exception as e:
        return { "error": str(e)}



async def read():
    folder_path = f"./resources/uploads"
    documents = DirectoryLoader(folder_path).load()
    return documents



"""
"""
@app.post("/upload")
async def upload_context(files: list[UploadFile] = File(...)):
    Uploads multiple files received from an API call and stores them in the directory.

    Args:
        files (List[UploadFile]): A list of UploadFile objects containing the uploaded files.

    Returns:
        Dict[str, str]: A dictionary with a message if successful or an error message if unsuccessful.
 

    try:
        upload_directory = "./resources/uploads"  

        # Create the upload directory if it doesn't exist
        os.makedirs(upload_directory, exist_ok=True)  

        uploaded_files = []
        for file in files:
            file_path = os.path.join(upload_directory, file.filename)
            uploaded_files.append(file_path)  # Track uploaded file paths

            # Write the file to the specified directory
            with open(file_path, "wb") as buffer:
                await buffer.write(await file.read())

        # Call the method to update the vector store index
        response = upload()

        return {"message": f"Files uploaded successfully: {', '.join(uploaded_files)}", "response": response}

    except Exception as e:
        print(f"Error uploading files: {e}")
        return {"error": str(e)}



"""
#uvicorn main:app --reload