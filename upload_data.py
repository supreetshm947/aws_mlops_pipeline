import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from constants import DATA_BUCKET_NAME, DATA_FILE_NAME, SCRIPT_FILE_NAME

def upload_data(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}.")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available for AWS.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return False
    except Exception as e:
        print(f"Error occurred while uploading file: {e}")
        return False


if __name__=="__main__":
    # upload_data(DATA_FILE_NAME, DATA_BUCKET_NAME)
    # upload_data(SCRIPT_FILE_NAME, DATA_BUCKET_NAME)
    upload_data("metric.json", DATA_BUCKET_NAME)