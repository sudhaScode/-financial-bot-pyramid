from vectorstore.matching_engine import MatchingEngine
import os
from google.cloud import aiplatform
from google.cloud import storage
from google.protobuf import field_mask_pb2 as field_mask
from utility.functionstore import copy_to_bucket, read_bucket, documents_markup

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

  def persist_storage_bucket(project_id, pyramid_storage_bucket, machineIndex):
    folder_path = f"./resources/uploads"
    try:
      copy_to_bucket(pyramid_storage_bucket, folder_path) #bucket_name: str, local_file_path: str
      parent_documents = read_bucket(project_id, pyramid_storage_bucket)
      texts, metadatas = documents_markup(parent_documents)

      doc_ids = machineIndex.add_texts(texts, metadatas)
    except Exception as e:
      raise Exception(f"Error adding documents to bucket: {e}")
      


