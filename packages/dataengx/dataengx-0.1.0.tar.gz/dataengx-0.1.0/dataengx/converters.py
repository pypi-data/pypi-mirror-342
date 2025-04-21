import pandas as pd
import duckdb
import json
import sqlite3
import pyarrow.parquet as pq

def convert_parquet_to_csv(parquet_file, csv_file):
    """
    Convert a Parquet file to a CSV file.

    Args:
        parquet_file (str): Path to the input .parquet file.
        csv_file (str): Path to save the output .csv file.

    CLI:
        dataengx convert-parquet-to-csv input.parquet output.csv
    """
    df = pd.read_parquet(parquet_file)
    df.to_csv(csv_file, index=False)


def csv_to_json(csv_file, json_file):
    """
    Convert a CSV file to JSON (newline-delimited format).

    Args:
        csv_file (str): Path to the input .csv file.
        json_file (str): Path to save the output .json file.

    CLI:
        dataengx csv-to-json input.csv output.json
    """
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient="records", lines=True)


def csv_to_nested_json(csv_file, json_file, group_by):
    """
    Convert a CSV to nested JSON by grouping on a specific column.

    Args:
        csv_file (str): Path to the input .csv file.
        json_file (str): Path to save the output nested .json.
        group_by (str): Column name to group by.

    CLI:
        dataengx csv-to-nested-json input.csv output.json --group-by category
    """
    df = pd.read_csv(csv_file)
    grouped = df.groupby(group_by).apply(lambda x: x.to_dict(orient="records")).to_dict()
    with open(json_file, "w") as f:
        json.dump(grouped, f, indent=4)


def split_parquet_to_csv(parquet_file, output_dir, chunk_size=10000):
    """
    Split a large Parquet file into multiple CSV chunks.

    Args:
        parquet_file (str): Path to the input .parquet file.
        output_dir (str): Directory to save CSV chunks.
        chunk_size (int): Number of rows per chunk. Default is 10,000.

    CLI:
        dataengx split-parquet input.parquet ./output_dir --chunk-size 5000
    """
    df = pd.read_parquet(parquet_file)
    total_chunks = (len(df) // chunk_size) + 1
    for i in range(total_chunks):
        chunk = df[i * chunk_size:(i + 1) * chunk_size]
        chunk.to_csv(f"{output_dir}/chunk_{i + 1}.csv", index=False)


def csv_to_sqlite(csv_file, sqlite_file, table_name="data"):
    """
    Convert a CSV file into a SQLite database table.

    Args:
        csv_file (str): Path to the input .csv file.
        sqlite_file (str): Path to the output .sqlite file.
        table_name (str): Name of the table to create or overwrite.

    CLI:
        dataengx csv-to-sqlite input.csv db.sqlite --table my_table
    """
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(sqlite_file)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


def parquet_to_jsonl(parquet_file, jsonl_file):
    """
    Convert a Parquet file to newline-delimited JSON (JSONL).

    Args:
        parquet_file (str): Input .parquet file path.
        jsonl_file (str): Output .jsonl file path.

    CLI:
        dataengx parquet-to-jsonl input.parquet output.jsonl
    """
    df = pd.read_parquet(parquet_file)
    with open(jsonl_file, "w") as f:
        for record in df.to_dict(orient="records"):
            f.write(json.dumps(record) + "\n")


def jsonl_to_csv(jsonl_file, csv_file):
    """
    Convert a newline-delimited JSON file to CSV.

    Args:
        jsonl_file (str): Input .jsonl file path.
        csv_file (str): Output .csv file path.

    CLI:
        dataengx jsonl-to-csv input.jsonl output.csv
    """
    with open(jsonl_file, "r") as f:
        records = [json.loads(line) for line in f]
    df = pd.DataFrame(records)
    df.to_csv(csv_file, index=False)


def query_csv_with_sql(csv_file, query):
    """
    Run an SQL query on a CSV file using DuckDB.

    Args:
        csv_file (str): Path to the CSV file.
        query (str): SQL query to execute.

    Returns:
        pd.DataFrame: Resulting DataFrame from the query.

    CLI:
        dataengx query-csv input.csv "SELECT COUNT(*) FROM data"
    """
    con = duckdb.connect()
    con.execute(f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{csv_file}')")
    result = con.execute(query).fetchdf()
    con.close()
    return result


def export_dataframe(df, output_file, file_format="csv"):
    """
    Export a DataFrame to CSV, JSON, or Parquet.

    Args:
        df (pd.DataFrame): DataFrame to export.
        output_file (str): Output file path.
        file_format (str): One of 'csv', 'json', or 'parquet'.

    CLI: (used internally after queries or transforms)
        dataengx export result.csv --format csv
    """
    if file_format == "csv":
        df.to_csv(output_file, index=False)
    elif file_format == "json":
        df.to_json(output_file, orient="records", lines=True)
    elif file_format == "parquet":
        df.to_parquet(output_file, index=False)
    else:
        raise ValueError("Unsupported format. Choose from 'csv', 'json', or 'parquet'.")
