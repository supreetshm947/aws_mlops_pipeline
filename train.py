import os
import random
import pandas as pd
import joblib
from typing import Dict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import boto3
import argparse
from datetime import datetime

def train_random_forest(df: pd.DataFrame,
                        target_column: str,
                        hyperparameters: Dict[str, int]):

    X = df.drop(target_column, axis=1)
    y = df[target_column]

    X = X.to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    model = RandomForestClassifier(**hyperparameters)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy: {accuracy}")

    return model, accuracy


def main():
    parser = argparse.ArgumentParser(description='Train a Random Forest model on the Iris dataset.')
    parser.add_argument('--BUCKET_NAME', type=str, required=True, help='S3 bucket name for input/output files.')
    parser.add_argument('--INPUT_FILE', type=str, required=True, help='Input file name in the S3 bucket.')
    parser.add_argument('--OUTPUT_MODEL_NAME', type=str, required=True, help='Trained model name.')

    parser.add_argument('--n_estimators', type=int, required=True, help='Number of trees in the forest.')
    parser.add_argument('--max_depth', type=int, required=True, help='Maximum depth of the tree.')
    parser.add_argument('--min_samples_split', type=int, required=True,
                        help='Minimum number of samples to split a node.')
    parser.add_argument('--min_samples_leaf', type=int, required=True, help='Minimum number of samples at a leaf node.')
    parser.add_argument('--random_state', type=int, required=True, help='Random State')

    args = parser.parse_args()

    file_bucket = args.BUCKET_NAME
    input_file = args.INPUT_FILE
    output_model_name = args.OUTPUT_MODEL_NAME

    # file_bucket = "mlops-bucket-files"
    # input_file = "iris.csv"
    # output_model_path = "mlops-model-artifact-bucket/model.joblib"

    s3 = boto3.client('s3')

    # Download the input file from S3
    #s3.download_file(file_bucket, input_file, '/opt/ml/input/data/iris.csv')

    df = pd.read_csv('/opt/ml/input/data/train/iris.csv')

    # Define hyperparameters dynamically
    hyperparameters = {
        'n_estimators': args.n_estimators,
        'max_depth': args.max_depth,
        'min_samples_split': args.min_samples_split,
        'min_samples_leaf': args.min_samples_leaf,
        'random_state': args.random_state,
    }

    # Train the model
    model, accuracy = train_random_forest(df, 'variety', hyperparameters)

    # Save the model to the local file system
    model_output_path_local = f"/opt/ml/model/{output_model_name}.joblib"
    joblib.dump(model, model_output_path_local)

    # # Upload the model to S3
    # s3.upload_file(model_output_path_local, output_model_path.split('/')[0], '/'.join(output_model_path.split('/')[1:]))
    # print(f"Model saved to s3://{output_model_path}")

if __name__ == '__main__':
    main()