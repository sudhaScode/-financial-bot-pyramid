import os
from google.cloud import storage
import google.auth
from langchain_community.document_loaders import GCSDirectoryLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import textwrap
import re
import pdfplumber


##check bucket exits are not
import google.cloud.storage as gcs

def check_and_create_bucket(bucket_name: str, project_id: str, region: str) -> bool:
    """Checks if a Cloud Storage bucket exists and creates it if not.

    Args:
        bucket_name (str): The name of the bucket to check and create.
        project_id (str): The ID of your Google Cloud project.
        region (str): The region where the bucket should be created.
    """

    storage_client = gcs.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    print(f"Checking if bucket {bucket.exists()} exists...")
    if bucket.exists():
        return False
    else:
        return True
    
#Create bucket
def create_gcs_bucket(project_id: str, bucket_name: str, location: str = "us-central1"):
    """
    Creates a Google Cloud Storage (GCS) bucket programmatically within a Python application.

    Args:
        project_id (str): Your GCP project ID.
        bucket_name (str): The desired name for the GCS bucket.
        location (str, optional): The regional location for the bucket. Defaults to "us-central1".

    Raises:
        ValueError: If project_id or bucket_name is not provided.
        RuntimeError: If an error occurs during bucket creation.
    """

    if not project_id:
        raise ValueError("Project ID is required.")
    if not bucket_name:
        raise ValueError("Bucket name is required.")

    # Construct the GCS URI
    bucket_uri = f"gs://{bucket_name}"

    # Use environment variables for secure authentication (recommended)
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        # Use application default credentials if available
        client = storage.Client()
        try:
            client.create_bucket(bucket_name, location=location)
            print(f"Bucket '{bucket_name}' created successfully in {location}.")
        except Exception as e:
            raise RuntimeError(f"Error creating bucket: {e}")

#copy documents to gcs temp bucket
def copy_to_bucket(bucket_name: str, local_file_path: str):

    if not bucket_name:
        raise ValueError("Bucket name is required.")
    if not local_file_path:
        raise ValueError("Local file path is required.")
    

    # Use application default credentials if available (recommended)
    storage_client = storage.Client()

    try:
        # Construct the destination GCS URI with the specified path within the bucket
        destination_uri = f"gs://{bucket_name}/documents"

        # Upload the file to the GCS bucket with the desired path
        blob = storage_client.bucket(bucket_name)
        blob.upload_from_filename(local_file_path)

        print(f"File '{local_file_path}' copied successfully to '{destination_uri}'.")
    except Exception as e:
        raise RuntimeError(f"Error copying file: {e}")    

#Delete bucket

def delete_gcs_blob(bucket_name: str, blob_name: str):
  """Deletes a blob from a Google Cloud Storage bucket.

  Args:
      bucket_name (str): The name of the bucket containing the blob.
      blob_name (str): The name of the blob to delete.

  Raises:
      ValueError: If either bucket or blob name is empty or None.
      google.auth.exceptions.Forbidden: If the user lacks permission to delete the blob.
      google.cloud.exceptions.NotFound: If the bucket or blob does not exist.
  """

  if not bucket_name or not blob_name:
      raise ValueError("Bucket and blob names cannot be empty or None.")

  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(blob_name)

  try:
      blob.delete()
      print(f"Blob '{blob_name}' deleted from bucket '{bucket_name}' successfully.")
  except (google.auth.exceptions.Forbidden, google.cloud.exceptions.Forbidden) as e:
      raise PermissionError(f"Permission error occurred while deleting blob: {e}")
  except google.cloud.exceptions.NotFound as e:
      print(f"Blob '{blob_name}' not found in bucket '{bucket_name}'. Skipping deletion.")


#Reading bucket
def read_bucket(project_name: str, storage_bucket_name: str):
    try:
      loader = GCSDirectoryLoader( project_name=project_name, bucket=storage_bucket_name)
      documents = loader.load()
    except Exception as e:
        print("Unable to read bucket: FileNotFoundError", e)
        return None

#
    return documents

#read bucket
def read_folder(folder_path):
    try:
        loader = DirectoryLoader(folder_path)
        documents = loader.load()
        return documents
    except Exception as e:
        print("Unable to read folder not found", e)

def read_upload():
        folder_path = f"./src/utility/uploads"
        loader = DirectoryLoader(folder_path)
        documents = loader.load()
        return documents
 
#Add document name and source to the metadata
def pre_chunking(documents):
    # Add document name and source to the metadata
    for document in documents:
        doc_md = document.metadata
        document_name = doc_md["source"].split("/")[-1]
        # derive doc source from Document loader
        doc_source_prefix = "/".join("temp-documents/".split("/")[:3])
        doc_source_suffix = "/".join(doc_md["source"].split("/")[4:-1])
        source = f"{doc_source_prefix}/{doc_source_suffix}"
        document.metadata = {"source": source, "document_name": document_name}
    return documents


# Utility functions for Embeddings API with rate limiting
def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time()
        yield
        after = time.time()
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time)


def text_chunk(documents):

    # split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
    )
    try:
        doc_splits = text_splitter.split_documents(documents)
        # Add chunk number to metadata
        for idx, split in enumerate(doc_splits):
            split.metadata["chunk"] = idx
    except Exception as e:
        print("chunking")

    return doc_splits
def preprocess_text(raw_text):
    # Remove dots
    text_without_dots = raw_text.replace('.', '.')
    
    # Normalize whitespace
    text_normalized = ' '.join(text_without_dots.split())
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    
    # Use the sub method to replace matched characters with an empty string
    cleaned_text = re.sub(pattern, '', text_normalized)

    return cleaned_text 
def documents_markup(documents):
    print("adding metadata to documents")
    print(documents)
    for document in documents:
        doc_md = document.metadata
        document_name = doc_md["source"].split("/")[-1]
        # derive doc source from Document loader
        doc_source_prefix = "/".join("temp-documents/".split("/")[:3])
        doc_source_suffix = "/".join(doc_md["source"].split("/")[4:-1])
        source = f"{doc_source_prefix}/{doc_source_suffix}"
        document.metadata = {"source": source, "document_name": document_name}

    doc_splits = text_chunk(documents)

    texts = [doc.page_content for doc in doc_splits]
    metadatas = [
        [
            {"namespace": "source", "allow_list": [doc.metadata["source"]]},
            {"namespace": "document_name", "allow_list": [doc.metadata["document_name"]]},
            {"namespace": "chunk", "allow_list": [str(doc.metadata["chunk"])]},
        ]
        for doc in doc_splits]
    print(texts, metadatas)
    return texts, metadatas


def preprocess_text(raw_text):
    # Remove dots
    text_without_dots = raw_text.replace('.', '.')
    
    # Normalize whitespace
    text_normalized = ' '.join(text_without_dots.split())
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    
    # Use the sub method to replace matched characters with an empty string
    cleaned_text = re.sub(pattern, '', text_normalized)

    return cleaned_text 

# read folder alternative

def pdf_folder_reader(folder_path):

    pdf_text =""
    try:

        for filename in os.listdir(folder_path):

            if filename.endswith(".pdf"):
                file_path = os.path.join(folder_path, filename)

                #print(f"Reading file: {file_path}")
                #read the pdf
                with pdfplumber.open(file_path) as file:
                    for page in file.pages:
                        pdf_text += page.extract_text()
            else:
                with open(file_path, "r") as f:
                    pdf_text += f.read( encoding="utf-8")
        pdf_text = preprocess_text(pdf_text)
    except Exception as e:
        print("Error reading pdf files")
    return pdf_text



def wrap(text, width=120, remove_extra_spaces=True, header_char="", header_repeat=0, title="", title_spacing=0):
  """Wraps a string with improved formatting, header breakdown, and title elevation (user-controlled).

  Args:
      s (str): The string to be wrapped.
      width (int, optional): The maximum line width. Defaults to 120.
      remove_extra_spaces (bool, optional): Whether to remove extra spaces before wrapping. Defaults to True.
      header_char (str, optional): Character to use for header breakdown line. Defaults to "".
      header_repeat (int, optional): Number of times to repeat the header character. Defaults to 0.
      title (str, optional): The title to be displayed. Defaults to "".
      title_spacing (int, optional): Number of blank lines before/after the title. Defaults to 0.

  Returns:
      str: The formatted string with header breakdown and title elevation.
  """

  # Remove extra spaces before wrapping for cleaner output
  if remove_extra_spaces:
      s = text.strip()  # Remove leading/trailing whitespace
      s = " ".join(s.split())  # Collapse consecutive spaces

  # Header breakdown line
  header_line = ""
  if header_char and header_repeat > 0:
      header_line = header_char * header_repeat + "\n"

  # Title with optional spacing
  title_section = ""
  if title:
      title_padding = "\n" * title_spacing
      title_section = f"{title_padding}{title}{title_padding}"

  # Combine elements with wrapped content
  formatted_text = header_line + title_section + "\n" + wrap(s, width=width)

  print("After formatting:\n")
  print("formatted_text")
  return formatted_text

  
"""

def add_documents_to_embedding_bucket( self, project_id: str, location: str, machineengine: MatchingEngine, texts: list, metadatas: list):

    index_id, index_endpoint_id =self.engine.get_index_and_endpoint()
    project_id=project_id
    location = "asia-south1"
    api_endpoint = f"{location}-aiplatform.googleapis.com"
    print(api_endpoint,".........................................................................")
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