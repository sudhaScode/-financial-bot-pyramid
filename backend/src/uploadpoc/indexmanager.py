from src.vectorstore.matching_engine import MatchingEngine
import os
from google.cloud import aiplatform
from google.cloud import storage
from google.protobuf import field_mask_pb2 as field_mask

class IndexManager:
  """Manages the creation, deployment, and initialization of an index."""

  def __init__(self, engine):
    """
    Args:
        engine: The indexing engine to use Matchengine.
    """
    self.engine = engine

  def create_index(self, me_embedding_dir: str, me_dimensions: str):
    
    """Creates an index with the specified name and schema.
    """
    index_update_method="streaming"
    index_algorithm="tree-ah"
    try:
      index = self.engine.create_index(
      embedding_gcs_uri=f"gs://{me_embedding_dir}/init_index",
      dimensions=me_dimensions,
      index_update_method="streaming",
      index_algorithm="tree-ah",)

      if index:
        print(index.name)
      return index
    except Exception as e:
      print(f"Creaeting index failed {e}")

  def deploy_index(self):
    """Deploys the specified index to make it available for searches.
    """
    try:
      index_endpoint = self.engine.deploy_index()

      if index_endpoint:
          print(f"Index endpoint resource name: {index_endpoint.name}")
          print(
              f"Index endpoint public domain name: {index_endpoint.public_endpoint_domain_name}"
          )
          print("Deployed indexes on the index endpoint:")
          for d in index_endpoint.deployed_indexes:
              print(f"    {d.id}")

    except Exception as e:
      print(f" error deploying index: {e}")


  def initialize_index(self, project_id: str, me_region: str, me_embedding_dir: str,embeddings:str):
        """Initializes the index with the provided data.
        """

        # initialize vector storehasattr(MatchingEngine, 'get_index_and_endpoint')
        if (True):
          try:
            me_index_id, me_index_endpoint_id = self.engine.get_index_and_endpoint()
            #print( me_index_id, me_index_endpoint_id, "get_index_and_endpoint")
            if me_index_id and me_index_endpoint_id:
              #print("entered to create index obj")
              me = MatchingEngine.from_components(
                  project_id=project_id,
                  region=me_region,
                  gcs_bucket_name=f"gs://{me_embedding_dir}".split("/")[2],
                  embedding=embeddings,
                  index_id=me_index_id,
                  endpoint_id=me_index_endpoint_id,
                  #credentials_path= os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
              )
              return me
          except Exception as e:
            print(f"Error retrieving IDs from MatchingEngineUtils: {e}")
  def add_documents_to_embedding_bucket( self, project_id: str, location: str, machineengine: MatchingEngine, texts: list, metadatas: list):
      """Adds documents to the index.
      receive the Machine engine index
       -- check index endpoint is empty n
        -- if index endpoint is empty 
          add new documents to the end point by machine engine
        -- else delete the content of the bucket and add new documents to the index
        empty index
        empty bucket
        add new documents to the index
      doc_ids = machineIndex.add_texts(texts=texts, metadatas=metadatas)
      """

      index_id, index_endpoint_id =self.engine.get_index_and_endpoint()
      project_id=project_id
      location = "asia-south1"
      api_endpoint = f"{location}-aiplatform.googleapis.com"
      print(api_endpoint,".........................................................................")
      """
      check = self.check_data_in_index_endpoint(index_endpoint_id=index_endpoint_id,location=location)
      if check == True:
        #dlete data points
        print("Data points exits in index.....................................")
        try:
          data_response = self.delete_all_data_from_index_endpoint(
              project=project_id,
              index_endpoint_id=index_endpoint_id,
              location=location,
              api_endpoint=api_endpoint,
          )
          #delete the folder from bucket
          bucket_name = "financial-bot-pyramid-temp-index"
          folder_path=f"gs://{bucket_name}/documents"
          self.delete_folder_from_bucket(bucket_name, folder_path)
          print("deleted exiting folders from bucket")
          machineengine.add_texts(texts=texts, metadatas=metadatas)
        except Exception as e:
          print(f"Error deleting data from index endpoint: {e}")

      else:
        # add data to machine index
        print("no data in index endpoint........................................")
        self.delete_folder_from_bucket(bucket_name, folder_path)
        machineengine.add_texts(texts=texts, metadatas=metadatas)
        """
      print("adding documents to index........................................")
     
      machineengine.add_texts(texts=texts, metadatas=metadatas)


  def delete_all_data_from_index_endpoint(
      project: str,
      index_endpoint_id: str,
      location: str,
      api_endpoint: str
  ):
      # The AI Platform services require regional API endpoints.

      client_options = {"api_endpoint": api_endpoint}
      # Initialize client that will be used to create and send requests.
      # This client only needs to be created once, and can be reused for multiple requests.
      client = aiplatform.gapic.IndexEndpointServiceClient(client_options=client_options)
      index_endpoint = client.index_endpoint_path(
          project=project, location=location, index_endpoint=index_endpoint_id
      )
      response = client.delete_data(index_endpoint=index_endpoint)
      print("Long running operation:", response.operation.name)
      delete_data_response = response.result(timeout=120)
      return delete_data_response

  def index_documents_sample(
      project: str,
      index_endpoint_id: str,
      gcs_source_uri: str,
       location: str = "asia-south1",
      api_endpoint: str = "projects/897611931269/locations/asia-south1/indexEndpoints/957859345746362368",
  ):
      # The AI Platform services require regional API endpoints.
      client_options = {"api_endpoint": api_endpoint}
      # Initialize client that will be used to create and send requests.
      # This client only needs to be created once , and can be reused for multiple requests.
      client = aiplatform.gapic.IndexEndpointServiceClient(client_options=client_options)
      index_endpoint = client.index_endpoint_path(
          project=project, location=location, index_endpoint=index_endpoint_id
      )
      gcs_source = {"uris": [gcs_source_uri]}
      index_request = {"gcs_source": gcs_source}
      response = client.index_documents(index_endpoint=index_endpoint, index_request=index_request)
      print("Long running operation:", response.operation.name)
      index_documents_response = response.result(timeout=120)
      print("index_documents_response:", index_documents_response)


  def delete_folder_from_bucket(bucket_name: str )-> bool:
      """Deletes a folder and its contents from a Cloud Storage bucket.

      Args:
          bucket_name (str): The name of the Cloud Storage bucket.
          folder_path (str): The path to the folder within the bucket.
      """
      folder_path = "/documents"
      storage_client = storage.Client()
      bucket = storage_client.bucket(bucket_name)

      blob_iterator = bucket.list_blobs(prefix=folder_path)  # List blobs in the folder
      for blob in blob_iterator:
          blob.delete()  # Delete each blob individually

      # Optionally, delete the folder itself if empty
      folder_blob = bucket.blob(folder_path)
      if folder_blob.exists():
        """
          try:
              folder_blob.delete()
              print(f"Deleted folder '{folder_path}' from bucket '{bucket_name}'")
          except Exception as e:
              print(f"Error deleting folder '{folder_path}': {e}")
          """
        return True
      else:
          return False


  def check_data_in_index_endpoint( project: str, index_endpoint_id: str, location: str):

      # The AI Platform services require regional API endpoints.
      client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
      # Initialize client that will be used to create and send requests.
      # This client only needs to be created once, and can be reused for multiple requests.
      client = aiplatform.gapic.IndexEndpointServiceClient(client_options=client_options)
      index_endpoint = client.get_index_endpoint(
          name="projects/{}/locations/{}/indexEndpoints/{}".format(
              project, location, index_endpoint_id
          )
      )
      if index_endpoint.index_count > 0:
         return True
      else:
          return False


