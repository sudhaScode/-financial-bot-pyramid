

rm -rf cache
Run following commands on terminal
- -  conda --version
- -  conda create -p venv python==3.11
- -  conda activate venv/ -> go to the backend subfolder path
- -  pip install -r requirements.txt 
- -  cat sudorequirements.txt | xargs sudo apt install -y
- -  gcloud auth login  or  gcloud config set account `ACCOUNT`
- -  gcloud config set project PROJECT_ID[cap-curious-creators]
cap-curious-creators@appspot.gserviceaccount.com
- - $ gcloud auth activate-service-account "" --key-file="env/key.json"
  - Activated service account credentials for: [cap-curious-creators@appspot.gserviceaccount.com]


  - gcloud init
  - gcloud auth application-default login

  - gcloud auth application-default login --impersonate-service-account cap-curious-creators@appspot.gserviceaccount.com

  - gcloud projects add-iam-policy-binding cap-curious-creators --member="cap-curious-creators@appspot.gserviceaccount.com" --role roles/owner


gcloud auth application-default login [ACCOUNT] [--no-browser] [--client-id-file=CLIENT_ID_FILE] [--disable-quota-project] [--no-launch-browser] [--login-config=LOGIN_CONFIG] [--scopes=SCOPE,[SCOPE,…]] [GCLOUD_WIDE_FLAG …]

gcloud auth application-default login --scopes https://www.googleapis.com/auth/cloud-platform, https://www.googleapis.com/auth/devstorage.full_control


# UPLOAD POC
## Features
  - Summarizing documents on demand - post
  - Preparing context for Q&A - post
  - Saving the dcocuemnts for furure use  - get


  these are my requirement to add new text data to index
  where i aleady initialized the index with Machine engine , i need to remove the old data from the index and add new data to it.
  
possible package confilict for protobuf
use command `conda install protobuf -y`

  `Make the upload design session component, display the tile like, prompting on ${docuement name}`
  `if the file not uploaded show upload file title if file uploaded show prompting on ${docuement name}`




  https://partner.cloudskillsboost.google/course_templates/894/labs/461436 - Discovery Engine API 

## resources
 https://github.com/GoogleCloudPlatform/generative-ai
  intro_langchain_palm_api.ipynb

  gsutil cp gs://partner-usecase-bucket/genai023/langchain_1hr_sprint.ipynb .
Markdown
from IPython.display import Markdown, display
len(pages)#36
response1 = stuff_chain.run(pages[:12])
response2 = stuff_chain.run(pages[12:24])
response3 = stuff_chain.run(pages[24:])

# Combine the Markdown strings
combined_markdown = response1+response2+response3

# Display the combined markdown
p= Markdown(combined_markdown)

use markdown package for fontend - npm install markdown

fetch('/summarize')
  .then(response => response.text())
  .then(markdownContent => {  
    const summaryElement = document.getElementById('summary');
    summaryElement.innerHTML = marked(markdownContent);
  });
