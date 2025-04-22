# mltinu/builder.py
"""
CodeBuilder: Generates a complete Jupyter notebook script for loading a CSV,
preprocessing, training a model, and evaluating metrics—all in a single code cell.
"""

import os
import pandas as pd
import logging
from typing import Tuple, Dict
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CodeBuilder:
    def __init__(
        self,
        csv_path: str,
        target: str,
        model_name: str,
        api_key: str = None
    ):
        """
        Parameters:
            csv_path (str): Path to the input CSV file.
            target (str): Name of the target column.
            model_name (str): scikit-learn model class name, e.g., 'RandomForestClassifier'.
            api_key (str, optional): API key for the LLM. Reads from MLTINU_API_KEY if None.
        """
        self.csv_path = csv_path
        self.target = target
        self.model_name = model_name
        # Retrieve API key from env if not provided
        self.api_key = "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"
        if not self.api_key:
            raise ValueError("Please set the MLTINU_API_KEY environment variable")
        if not os.path.isfile(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Initialize the LLM client
        self.llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
            model="llama-3.3-70b-versatile",
        )

    def _get_csv_info(self) -> Tuple[str, Dict[str, str]]:
        df = pd.read_csv(self.csv_path)
        head_str = df.head().to_string(index=False)
        dtypes = df.dtypes.apply(lambda x: x.name).to_dict()
        return head_str, dtypes

    def _get_prompt(self, head_str: str, dtypes: Dict[str, str]) -> str:
        # Detect numeric vs. categorical columns
        numeric_cols = [c for c, dt in dtypes.items() if dt in ("int64", "float64")]
        categorical_cols = [c for c in dtypes if c not in numeric_cols]

        return (
            "You are TINU, an expert ML engineer. Generate a single Jupyter Notebook code cell that accomplishes the following steps:\n"
            f"1. Load the CSV at '{self.csv_path}' into a pandas DataFrame.\n"
            "2. Display df.head() and df.info().\n"
            f"3. Identify numeric columns: {numeric_cols} and categorical columns: {categorical_cols}.\n"
            "4. Preprocess data: impute numeric columns with median, scale with StandardScaler; "
            "impute categorical columns with mode and encode with OneHotEncoder.\n"
            f"5. Split data into train/test (80/20) stratified on '{self.target}', random_state=42.\n"
            f"6. Instantiate and train a scikit-learn {self.model_name}(random_state=42).\n"
            "7. Evaluate on the test set: print accuracy, precision, recall, F1-score, and confusion matrix.\n"
            "8. All code should reside in a single cell without helper functions."
        )

    def generate_code(self) -> str:
        head_str, dtypes = self._get_csv_info()
        prompt = self._get_prompt(head_str, dtypes)
        logger.info("Generating code with prompt: %s", prompt)
        response = self.llm.invoke(
            [
                {"role": "system", "content": "You are a professional coder."},
                {"role": "user", "content": prompt}
            ]
        )
        return getattr(response, "content", str(response)).strip()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a complete ML notebook code cell from a CSV."
    )
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    parser.add_argument("target", help="Name of the target column.")
    parser.add_argument("model_name", help="Scikit-learn model class name, e.g., 'RandomForestClassifier'.")
    args = parser.parse_args()

    builder = CodeBuilder(args.csv_path, args.target, args.model_name)
    code = builder.generate_code()
    print(code)
