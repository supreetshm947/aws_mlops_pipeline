
variable "DATA_BUCKET_NAME" {
    description = "name of the data bucket"
    type = string
}

variable "ARTIFACT_BUCKET_NAME" {
    description = "name of the artifact bucket"
    type = string
}

variable "DATA_FILE_NAME" {
  description = "The local path of data file"
  type        = string
}

##########################################

resource "aws_s3_bucket" "data_bucket" {
    bucket = "${var.DATA_BUCKET_NAME}"
}

resource "aws_s3_bucket" "artifact_bucket" {
    bucket = "${var.ARTIFACT_BUCKET_NAME}"
}

resource "aws_s3_object" "data_object" {
  bucket = aws_s3_bucket.data_bucket.bucket
  key    = "${var.DATA_FILE_NAME}"
  source = "${var.DATA_FILE_NAME}"
  acl    = "private" 
}