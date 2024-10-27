terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws",
            version = "~> 5.0"
        }
    }
}

provider "aws" {
    region = "eu-north-1"
}

module "my_s3_buckets" {
    source = "./modules/storage"
    DATA_BUCKET_NAME = var.DATA_BUCKET_NAME
    ARTIFACT_BUCKET_NAME = var.ARTIFACT_BUCKET_NAME
    DATA_FILE_NAME = var.DATA_FILE_NAME
}