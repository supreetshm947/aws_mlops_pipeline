import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from constants import AWS_ROLE

# Set up SageMaker session and role
sagemaker_session = sagemaker.Session()
role = AWS_ROLE

# Define the SKLearn estimator
sklearn_estimator = SKLearn(
    entry_point='model_train.py',
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    framework_version='0.23-1',
    py_version='py3',
    hyperparameters={
        'n-estimators': str(100),
        'max-depth': str(10)
    },
    output_path='s3://mlops-model-artifact-bucket/'  # The S3 path where the model artifact will be stored
)

# Launch the training job
sklearn_estimator.fit({'train': 's3://mlops-bucket-files/iris.csv'})
