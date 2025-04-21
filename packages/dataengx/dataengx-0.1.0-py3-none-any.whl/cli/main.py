import argparse
from dataengx import (
    convert_parquet_to_csv,
    csv_to_json,
    csv_to_nested_json,
    split_parquet_to_csv,
    csv_to_sqlite,
    parquet_to_jsonl,
    jsonl_to_csv,
    query_csv_with_sql,
    export_dataframe
)
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="DataEngX CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parquet to CSV
    p2c = subparsers.add_parser("parquet-to-csv")
    p2c.add_argument("input")
    p2c.add_argument("output_dir")
    p2c.add_argument("--filename", default=None)

    # CSV to JSON
    c2j = subparsers.add_parser("csv-to-json")
    c2j.add_argument("input")
    c2j.add_argument("output")

    # CSV to Nested JSON
    c2nj = subparsers.add_parser("csv-to-nested-json")
    c2nj.add_argument("input")
    c2nj.add_argument("output")

    # Split Parquet to CSV
    split = subparsers.add_parser("split-parquet-to-csv")
    split.add_argument("input")
    split.add_argument("output_dir")
    split.add_argument("--row_limit", type=int, default=5000)

    # CSV to SQLite
    c2sql = subparsers.add_parser("csv-to-sqlite")
    c2sql.add_argument("input")
    c2sql.add_argument("output")

    # Parquet to JSONL
    p2jsonl = subparsers.add_parser("parquet-to-jsonl")
    p2jsonl.add_argument("input")
    p2jsonl.add_argument("output")

    # JSONL to CSV
    j2csv = subparsers.add_parser("jsonl-to-csv")
    j2csv.add_argument("input")
    j2csv.add_argument("output")

    # Query CSV with SQL
    query = subparsers.add_parser("query-csv")
    query.add_argument("query")
    query.add_argument("csv_path")

    # Export DataFrame to format
    export = subparsers.add_parser("export-dataframe")
    export.add_argument("format", choices=["csv", "parquet", "json"])
    export.add_argument("output_dir")
    export.add_argument("filename")

    args = parser.parse_args()

    # Dispatcher
    if args.command == "parquet-to-csv":
        convert_parquet_to_csv(args.input, args.output_dir, args.filename)
    elif args.command == "csv-to-json":
        csv_to_json(args.input, args.output)
    elif args.command == "csv-to-nested-json":
        csv_to_nested_json(args.input, args.output)
    elif args.command == "split-parquet-to-csv":
        split_parquet_to_csv(args.input, args.output_dir, args.row_limit)
    elif args.command == "csv-to-sqlite":
        csv_to_sqlite(args.input, args.output)
    elif args.command == "parquet-to-jsonl":
        parquet_to_jsonl(args.input, args.output)
    elif args.command == "jsonl-to-csv":
        jsonl_to_csv(args.input, args.output)
    elif args.command == "query-csv":
        result_df = query_csv_with_sql(args.query, csv_path=args.csv_path)
        print(result_df)
    elif args.command == "export-dataframe":
        # Create a sample DataFrame (or load from somewhere)
        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
        export_dataframe(df, args.output_dir, args.filename, fmt=args.format)

if __name__ == "__main__":
    main()
