import os
import urllib.request
import time

def create_library(wait_interval=1):  # Allow customization of wait interval
    """
    Downloads and creates the matching library directory with a wait interval.

    Args:
        wait_interval (float, optional): The number of seconds to wait between retries.
            Defaults to 1.
    """

    if not os.path.exists("vectorstore"):
        os.makedirs("vectorstore")

    url_prefix = "https://raw.githubusercontent.com/GoogleCloudPlatform/generative-ai/main/language/use-cases/document-qa/utils"
    files = ["__init__.py", "matching_engine.py", "matching_engine_utils.py"]

    for fname in files:
        download_url = f"{url_prefix}/{fname}"
        destination_path = f"vectorstore/{fname}"

        try:
            urllib.request.urlretrieve(download_url, filename=destination_path)
        except urllib.error.URLError as e:
            print(f"Error downloading {fname}: {e}")
            # Retry logic here
            wait_before_retry(wait_interval)

def wait_before_retry(interval):
    """
    Waits for a specified interval before retrying a download.

    Args:
        interval (float): The number of seconds to wait.
    """

    print(f"Waiting {interval} seconds before retry...")
    time.sleep(interval)

