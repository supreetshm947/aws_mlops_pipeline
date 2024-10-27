# Buckets
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