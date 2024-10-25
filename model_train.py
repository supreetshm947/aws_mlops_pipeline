import argparse
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Parse the input arguments from the SageMaker job
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--max-depth', type=int, default=None)

    # SageMaker specific arguments
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])

    args = parser.parse_args()

    # Load the training data
    train_data = pd.read_csv(os.path.join(args.train, 'iris.csv'))

    X = train_data.drop('variety', axis=1)
    y = train_data['variety']

    X = X.to_numpy()

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=args.n_estimators, max_depth=args.max_depth)
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"accuracy={accuracy}")

    # Save the model to the output directory
    model_output_path = os.path.join(args.model_dir, 'model.joblib')
    joblib.dump(model, model_output_path)
