# mltinu/cli.py
import sys
import argparse
from .builder import CodeBuilder

def main():
    p = argparse.ArgumentParser(prog="mltinu")
    p.add_argument("--csv",    "-c", required=True, help="Path to input CSV")
    p.add_argument("--target", "-t", required=True, help="Target column name")
    p.add_argument("--model",  "-m", required=True, help="Model name (e.g. RandomForest)")
    args = p.parse_args()

    builder = CodeBuilder(csv_path=args.csv, target=args.target, model_name=args.model)
    code = builder.generate_code()
    sys.stdout.write(code)

if __name__ == "__main__":
    main()
