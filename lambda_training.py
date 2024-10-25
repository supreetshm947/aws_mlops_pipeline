import boto3
import os
from datetime import datetime
import random
import time

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker', region_name='eu-north-1')

    # Generate a unique training job name using current timestamp
    job_name = f"rf-training-job-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    hyperparameters = {
        'n_estimators': str(random.randint(1, 2)),
        'max_depth': str(random.randint(1, 5)),
        'min_samples_split': str(random.randint(2, 3)),
        'min_samples_leaf': str(random.randint(1, 2)),
        'random_state': str(42),
    }

    # Define the SageMaker training job request
    response = sagemaker_client.create_training_job(
        TrainingJobName=job_name,
        AlgorithmSpecification={
            'TrainingImage': '662702820516.dkr.ecr.eu-north-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3',
            'TrainingInputMode': 'File'
        },
        RoleArn=os.environ['SAGEMAKER_ROLE_ARN'],
        InputDataConfig=[
            {
                'ChannelName': 'train',
                'DataSource': {
                    'S3DataSource': {
                        'S3DataType': 'S3Prefix',
                        'S3Uri': 's3://mlops-bucket-files/iris.csv',  # Path to Iris dataset in S3
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                },
                'ContentType': 'text/csv',
                'InputMode': 'File'
            },
        ],
        OutputDataConfig={
            'S3OutputPath': 's3://mlops-model-artifact-bucket/'  # Path to save model artifacts
        },
        ResourceConfig={
            'InstanceType': 'ml.m5.large',
            'InstanceCount': 1,
            'VolumeSizeInGB': 5,
        },
        StoppingCondition={
            'MaxRuntimeInSeconds': 3600
        },
        HyperParameters={
            'sagemaker_program': 'train.py',
            'sagemaker_submit_directory': 's3://mlops-bucket-files/train.tar.gz',
            'BUCKET_NAME': 'mlops-bucket-files',
            'INPUT_FILE': 'iris.csv',
            'OUTPUT_MODEL_NAME': f"model-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}",
            **hyperparameters
        }
    )

    i = 0
    while True:
        response = sagemaker_client.describe_training_job(TrainingJobName=job_name)
        status = response['TrainingJobStatus']
        print(f"Current job status: {status}")

        if status in ['Completed', 'Failed', 'Stopped'] or i==4:
            break
        i+=1
        time.sleep(60)  # Wait for 1 minute before polling again
    print(status)
    if status == 'Completed':
        # Retrieve model artifacts and hyperparameters
        model_artifacts = response['ModelArtifacts']['S3ModelArtifacts']
        output_model_name = response['HyperParameters']['OUTPUT_MODEL_NAME']

        accuracy = None
        if 'FinalMetricDataList' in response and len(response['FinalMetricDataList']) > 0:
            for metric in response['FinalMetricDataList']:
                if metric['MetricName'] == 'Accuracy':
                    accuracy = metric['Value']
                    break
        print(model_artifacts, output_model_name, accuracy)

    return {
        'statusCode': 200,
        'body': f"SageMaker training job '{job_name}' initiated successfully.",
        'sagemaker_response': response
    }
