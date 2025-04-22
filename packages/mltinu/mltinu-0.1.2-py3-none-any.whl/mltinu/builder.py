# mltinu/builder.py
"""
CodeBuilder: Generates a single Jupyter Notebook code cell tailored to the specified ML task
(classification, regression, or clustering) for any scikit-learn model (e.g., LR, LogReg, KNN, etc.).
"""

import os
import pandas as pd
import logging
from typing import Tuple, Dict, Optional
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Map common scikit-learn estimator names to their modules
MODULE_MAP = {
    'LogisticRegression': 'linear_model',
    'LinearRegression':   'linear_model',
    'Ridge':              'linear_model',
    'Lasso':              'linear_model',
    'KNeighborsClassifier': 'neighbors',
    'KNeighborsRegressor':  'neighbors',
    'SVC':                'svm',
    'SVR':                'svm',
    'DecisionTreeClassifier': 'tree',
    'DecisionTreeRegressor':  'tree',
    'RandomForestClassifier':  'ensemble',
    'RandomForestRegressor':   'ensemble',
    'GradientBoostingClassifier': 'ensemble',
    'GradientBoostingRegressor':  'ensemble',
    'AdaBoostClassifier':   'ensemble',
    'AdaBoostRegressor':    'ensemble',
    'KMeans':              'cluster'
}

def get_model_module(model_name: str, task: str) -> str:
    """Return the sklearn submodule for a given model name, using task as fallback."""
    if model_name in MODULE_MAP:
        return MODULE_MAP[model_name]
    # fallback based on task
    if task == 'classification':
        return 'ensemble'
    if task == 'regression':
        return 'ensemble'
    if task == 'unsupervised':
        return 'cluster'
    return 'ensemble'

class CodeBuilder:
    def __init__(
        self,
        csv_path: str,
        target: Optional[str],
        model_name: str,
        api_key: Optional[str] = None
    ):
        self.csv_path = csv_path
        self.target = target
        self.model_name = model_name
        self.api_key = "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"
        if not self.api_key:
            raise ValueError("Please set the MLTINU_API_KEY environment variable or pass api_key.")
        if not os.path.isfile(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        self.llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
            model="llama-3.3-70b-versatile",
        )
        self.task = self._infer_task()
        self.module = get_model_module(self.model_name, self.task)

    def _infer_task(self) -> str:
        name = self.model_name.lower()
        if 'classifier' in name:
            return 'classification'
        if 'regressor' in name:
            return 'regression'
        if self.target is None:
            return 'unsupervised'
        return 'classification'

    def _get_csv_info(self) -> Tuple[str, Dict[str, str]]:
        df = pd.read_csv(self.csv_path)
        head_str = df.head().to_string(index=False)
        dtypes = df.dtypes.apply(lambda x: x.name).to_dict()
        return head_str, dtypes

    def _get_prompt(self, head_str: str, dtypes: Dict[str, str]) -> str:
        numeric_cols = [c for c, dt in dtypes.items() if dt in ("int64", "float64")]
        categorical_cols = [c for c in dtypes if c not in numeric_cols]

        lines = [
            f"# Load and inspect data",
            f"import pandas as pd",
            f"df = pd.read_csv('{self.csv_path}')",
            "df.head(), df.info()",
            f"numeric_cols = {numeric_cols}; categorical_cols = {categorical_cols}",
            "# Build preprocessing pipelines",
            "from sklearn.impute import SimpleImputer",
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder",
            "from sklearn.compose import ColumnTransformer",
            "from sklearn.pipeline import Pipeline",
            "num_pipe = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])",
            "cat_pipe = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('encoder', OneHotEncoder(handle_unknown='ignore'))])",
            "preprocessor = ColumnTransformer([('num', num_pipe, numeric_cols), ('cat', cat_pipe, categorical_cols)])",
            "# Model import based on model_name",
            f"from sklearn.{self.module} import {self.model_name}"  
        ]
        if self.task == 'classification':
            lines += [
                "# Classification split and pipeline",
                "from sklearn.model_selection import train_test_split",
                f"X = df.drop('{self.target}', axis=1); y = df['{self.target}']",
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)",
                f"clf = {self.model_name}(random_state=42)",
                "pipeline = Pipeline([('preprocessor', preprocessor), ('estimator', clf)])",
                "pipeline.fit(X_train, y_train)",
                "preds = pipeline.predict(X_test)",
                "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix",
                "print(dict(accuracy=accuracy_score(y_test, preds), precision=precision_score(y_test, preds, average='weighted'),",
                "           recall=recall_score(y_test, preds, average='weighted'), f1=f1_score(y_test, preds, average='weighted'),",
                "           confusion=confusion_matrix(y_test, preds)))"
            ]
        elif self.task == 'regression':
            lines += [
                "# Regression split and pipeline",
                "from sklearn.model_selection import train_test_split",
                f"X = df.drop('{self.target}', axis=1); y = df['{self.target}']",
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)",
                f"reg = {self.model_name}(random_state=42)",
                "pipeline = Pipeline([('preprocessor', preprocessor), ('estimator', reg)])",
                "pipeline.fit(X_train, y_train)",
                "preds = pipeline.predict(X_test)",
                "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score",
                "print(dict(MAE=mean_absolute_error(y_test, preds),",
                "           RMSE=mean_squared_error(y_test, preds, squared=False),",
                "           R2=r2_score(y_test, preds)))"
            ]
        else:
            lines += [
                "# Clustering on all features",
                "X_proc = preprocessor.fit_transform(df)",
                f"clusterer = {self.model_name}()",
                "labels = clusterer.fit_predict(X_proc)",
                "from sklearn.metrics import silhouette_score",
                "print(dict(inertia=getattr(clusterer, 'inertia_', None),",
                "           silhouette=silhouette_score(X_proc, labels)))"
            ]
        lines.append("# End of single-cell ML workflow")
        return "\n".join(lines)

    def generate_code(self) -> str:
        head_str, dtypes = self._get_csv_info()
        prompt = self._get_prompt(head_str, dtypes)
        logger.info("Prompt for LLM: %s", prompt)
        response = self.llm.invoke([
            {"role": "system", "content": "You are a professional coder."},
            {"role": "user", "content": prompt}
        ])
        return getattr(response, "content", str(response)).strip()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate a single-cell ML workflow notebook for any sklearn model (LR, LogReg, KNN, etc.).")
    parser.add_argument("csv_path", help="Path to the input CSV file.")
    parser.add_argument("--target", help="Name of the target column (omit for clustering).", default=None)
    parser.add_argument("model_name", help="Scikit-learn model class name, e.g., 'LogisticRegression', 'KNeighborsClassifier', 'KMeans'.")
    args = parser.parse_args()

    builder = CodeBuilder(args.csv_path, args.target, args.model_name)
    print(builder.generate_code())
