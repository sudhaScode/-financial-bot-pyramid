import json
import time
import uuid
import os
import logging
import google.auth
import vertexai
from typing import List
import google.auth.transport.requests
from langchain_community.document_loaders import PyPDFLoader
import numpy as np
import vertexai
import langchain
from src.vectorestorecreator import create_library
from src.uploadpoc.embeddingconfig import CustomVertexAIEmbeddings
from langchain_community.document_loaders import  DirectoryLoader
#from ...scripts.scripts import set_gcp_credentials
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from langchain_google_vertexai import VertexAI

from src.utility.functionstore import (
    create_gcs_bucket,
    copy_to_bucket,
    delete_gcs_blob,
    read_bucket,
    pre_chunking,
    rate_limit,
    text_chunk,
    read_folder,
    documents_markup,
    check_and_create_bucket,
    pdf_folder_reader,
    read_upload
)
from src.vectorstore.matching_engine import MatchingEngine
from src.vectorstore.matching_engine_utils import MatchingEngineUtils
from src.uploadpoc.indexmanager import IndexManager

project_id = "cap-curious-creators"  # @param {type:"string"}
region = "asia-south1"  # @param {type:"string"}
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'./env/key.json'
### Vertex AI init
vertexai.init(project=project_id, location=region)
print("Vertex AI service initialized")

# Matching index engine
me_region = "asia-south1"
me_index_name = f"financial-bot-pyramid-temp-index"  # @param {type:"string"}
me_embedding_dir = f"financial-bot-pyramid-temp-embedd-bucket"  # @param {type:"string"}
me_dimensions = 768  # when using Vertex PaLM Embedding
pyramid_doc_bucket="financial-bot-pyramid-temp-bucket"

#LLM model configs
# Text model instance integrated with langChain
llm = VertexAI(
    model_name="text-bison@002",
    max_output_tokens=1024,
    temperature=0.2,
    top_p=0.8,
    top_k=40,
    verbose=True,
)

# Embeddings API integrated with langChain
EMBEDDING_QPM = 100
EMBEDDING_NUM_BATCH = 5
embeddings = CustomVertexAIEmbeddings(
    requests_per_minute=EMBEDDING_QPM,
    num_instances_per_batch=EMBEDDING_NUM_BATCH,
    model_name="textembedding-gecko@latest",
    index_type="IVF_FLAT"
)
## create bucket
exit = check_and_create_bucket(project_id, me_embedding_dir, region)
if not exit:# check point for bucket creation
    print("creating bucket")    
    create_gcs_bucket(project_id, me_embedding_dir, region)

mengine = MatchingEngineUtils(project_id, me_region, me_index_name)

indexengine = IndexManager(mengine)
#### CREATE INDEX______________
index_id, _ = mengine.get_index_and_endpoint()
if index_id is None or index_id == "":
    # index methods
    print("creating index")
    index = indexengine.create_index(me_embedding_dir, me_dimensions) 
    print("deploy index")
    indexengine.deploy_index()

print("initializing index")
machineIndex = indexengine.initialize_index(project_id,me_region, me_embedding_dir, embeddings)
print("initialized index", machineIndex)



#### ___________________________________UPLOAD FEATURE CHILD PYRAMID BOT_______________________________________________ ####
folder_path = f"./resources/uploads"
#entries = os.listdir(folder_path)
"""
if len(entries) >10 and len(entries) <20:
    documents = read_folder(f"./resources/uploads")
    print(documents, "folder reader")
    texts, metadata = documents_markup(documents)
    # deletes the old data adds new data
    indexengine.add_documents_to_embedding_bucket(project_id, region,machineIndex, texts, metadata)
"""
def upload(file_path):
    """
    indexengine.delete_folder_from_bucket(pyramid_doc_bucket) 
    copy_to_bucket(pyramid_doc_bucket, f"./resources/uploads")
    documents = read_bucket(pyramid_doc_bucket, f"documents")
    texts, metadatas = documents_markup(documents)
    machineIndex.add_texts(texts=texts, metadatas=metadatas)
"""
    #documents = read_upload()
    #documents = read_folder(folder_path) # not working
    #document = pdf_folder_reader(f"./resources/uploads")
    #documents.append(document)
    #texts, metadata = documents_markup(documents)
    #print("adding documents", texts)
    # deletes the old data adds new data
    #indexengine.add_documents_to_embedding_bucket(project_id, region,machineIndex, texts, metadata)
    

    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return "Upload successful"

#documents = read_upload()
"""
#documents = read_folder(folder_path) # not working
#document = pdf_folder_reader(f"./resources/uploads")
#documents.append(document)
texts, metadata = documents_markup(documents)
print("adding documents", texts)
"""
"""
loder = DirectoryLoader(f"./resources/uploads/")
documents = loder.load()
for document in documents:
    print(document.page_content, "folder reader")

#credentials, id = google.auth.default()

# Assuming you have valid scopes for your API
scopes = ["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/devstorage.full_control"]

try:
  # Obtain credentials with the specified scopes (assuming you have them set up)
  cred, _ = google.auth.default(scopes=scopes)

  # ... (use the credentials for API calls)

  # Refresh the token using the same scopes
  cred.refresh(google.auth.transport.requests.Request())

except google.auth.exceptions.RefreshError as e:
  print(f"Error refreshing token: {e}")

#request = google.auth.transport.requests.Request()
#credentials.refresh(request)
#print(credentials.token, id,  "fetched from default 382 matchin gengine.py")
"""