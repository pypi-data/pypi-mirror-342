import pandas as pd
from automl.main import AutoML
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run the AutoML pipeline.")
    parser.add_argument('--train', type=str, required=True, help='Path to the training data CSV file.')
    parser.add_argument('--test', type=str, help='Path to the test data CSV file.')
    parser.add_argument('--target', type=str, required=True, help='Name of the target column.')
    parser.add_argument('--output', type=str, help='Path to save the predictions CSV file.')
    parser.add_argument('--columns', type=str, nargs='+', help='List of columns to include in the output file.')

    args = parser.parse_args()

    # Load data
    df_train = pd.read_csv(args.train)
    df_test = pd.read_csv(args.test) if args.test else None

    # Initialize and run AutoML
    automl = AutoML(target_column=args.target)
    automl.fit(df_train, df_test)

    # Save predictions if output path is provided
    if args.output and df_test is not None:
        predictions = automl.predict(df_test)
        columns_to_include = args.columns if args.columns else df_test.columns.tolist()
        automl.create_csv(df_test, predictions, columns_to_include, args.output)


if __name__ == "__main__":
    main() 