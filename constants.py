from dotenv import load_dotenv
import os

load_dotenv()

DATA_BUCKET_NAME=os.getenv("DATA_BUCKET_NAME")
DATA_FILE_NAME=os.getenv("DATA_FILE_NAME")
SCRIPT_FILE_NAME=os.getenv("SCRIPT_FILE_NAME")
AWS_ROLE=os.getenv("AWS_ROLE")