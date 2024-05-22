import os
import vertexai

def init():
    project_id = "cap-curious-creators"  # @param {type:"string"}
    region = "asia-south1"  # @param {type:"string"}
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'./env/key.json'
    ### Vertex AI init
    vertexai.init(project=project_id, location=region)
    print("Vertex AI service initialized")

