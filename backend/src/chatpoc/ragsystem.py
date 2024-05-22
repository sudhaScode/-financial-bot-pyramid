import json
import time
import uuid
import os
import google.auth
import vertexai
import logging
import google.auth.transport.requests
import numpy as np
import vertexai
import langchain
from src.vectorestorecreator import create_library
from src.chatpoc.embeddingconfig import CustomVertexAIEmbeddings
#from ...scripts.scripts import set_gcp_credentials

from langchain_google_vertexai import VertexAI

from src.utility.functionstore import (
    create_gcs_bucket,
    copy_to_bucket,
    delete_gcs_blob,
    read_bucket,
    doc_metadata_creator,
    rate_limit,
    text_chunk,
    read_folder,
    documents_markup,
    check_and_create_bucket
)

#create a matching library
#create_library()
# Import custom Matching Engine packages
from src.vectorstore.matching_engine import MatchingEngine
from src.vectorstore.matching_engine_utils import MatchingEngineUtils
from src.chatpoc.indexmanager import IndexManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

project_id = "cap-curious-creators"  # @param {type:"string"}
region = "asia-south1"  # @param {type:"string"}

# Matching index engine
me_region = "asia-south1"
pyramid_storage_bucket="financial-bot-pyramid-persist-bucket"
me_index_name = f"financial-bot-pyramid-persist-index"  
me_embedding_dir = f"financial-bot-pyramid-perssit-embedd-bucket"  
me_dimensions = 768 

"""
### Vertex AI init
vertexai.init(project=project_id, location=region)
print("Vertex AI service initialized")
#LLM model configs
#set_gcp_credentials()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'./env/key.json'
print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), "environment set up")
#os.unsetenv("GOOGLE_APPLICATION_CREDENTIALS")
"""
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

# Matching Engine API integrated with langChain
mengine = MatchingEngineUtils(project_id, me_region, me_index_name)

indexengine = IndexManager(mengine)
index_id,_ = mengine.get_index_and_endpoint()
print("index id at chat poc 81", index_id)
if index_id is None or index_id == "" :
    # index methods
    print("creating index")
    index = indexengine.create_index(me_embedding_dir, me_dimensions) 
    print("deploy index")
    indexengine.deploy_index()

print("initializing index")
machineIndex = indexengine.initialize_index(project_id,me_region, me_embedding_dir, embeddings)
print("initialized index", machineIndex)



#####_________________________________________________SAVE DOCUMENTS FEATURE PARENT PYRAMID BOT_____________________________________________#####
## save the doceumts for parent bot> a new doc storage bucket, a new embeddings bucket , new vertex index
def update_bucket():
    indexengine.persist_storage_bucket(project_id,me_region, me_embedding_dir, embeddings)
