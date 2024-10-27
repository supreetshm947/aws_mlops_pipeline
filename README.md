# MLOps Pipeline Project on AWS

An end-to-end MLOps pipeline built on AWS to automate and manage machine learning workflow. It uses **AWS SageMaker** for model training and deployment, **Lambda** functions for processing and integration, **API Gateway** to create RESTful endpoints for model predictions, and **S3** for storing model artifacts and input data. 

The infrastructure is managed and provisioned using **Terraform**, enabling scalable, consistent, and repeatable deployments. This setup provides a robust way to implement and maintain ML pipelines in production, facilitating continuous integration and delivery of machine learning models.

## Key AWS Services
- **SageMaker**: Model training, deployment, and endpoint management.
- **Lambda**: Event-driven compute for handling model inference requests.
- **API Gateway**: RESTful API management to expose SageMaker endpoints.
- **S3**: Data storage for input data and model artifacts.
