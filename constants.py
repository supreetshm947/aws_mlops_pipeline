from dotenv import load_dotenv
import os

load_dotenv()

DATA_BUCKET_NAME=os.getenv("TF_VAR_DATA_BUCKET_NAME")
ARTIFACT_BUCKET_NAME=os.getenv("TF_VAR_ARTIFACT_BUCKET_NAME")
DATA_FILE_NAME=os.getenv("TF_VAR_DATA_FILE_NAME")
SCRIPT_FILE_NAME=os.getenv("TF_VAR_SCRIPT_FILE_NAME")
AWS_ROLE=os.getenv("TF_VAR_AWS_ROLE")