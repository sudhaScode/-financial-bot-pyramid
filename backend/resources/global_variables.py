# Project variables
PROJECT_ID = "cap-curious-creators"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}

# Matching index engine
ME_REGION = "us-central1"
ME_INDEX_NAME = f"{PROJECT_ID}-temp-index"  # @param {type:"string"}
ME_EMBEDDING_DIR = f"{PROJECT_ID}-temp-bucket"  # @param {type:"string"}
ME_DIMENSIONS = 768  # when using Vertex PaLM Embedding



# Temporary variables
GCS_TEMP_BUCKET = "cap-curious-creators-temp"  # @param {type:"string"}
#folder_prefix = f"Financial_documents/"




# Persistent variables
GCS_PERSISTENT_BUCKET = "cap-curious-creators-persistent"  # @param {type:"string"}