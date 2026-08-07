import pandas as pd
from pathlib import Path


input_file = (
    Path(__file__).parent.parent
    / "data"
    / "raw"
    / "youtube_dataset.csv"
)

output_file = (
    Path(__file__).parent.parent
    / "data"
    / "processed"
    / "youtube_clean.csv"
)


def clean_data():

    df = pd.read_csv(input_file)

    print("Original rows:", len(df))


    # Remove duplicate videos
    df = df.drop_duplicates(
        subset=["video_id"]
    )


    # Convert numeric columns
    numeric_columns = [
        "views",
        "likes",
        "comments"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    # Fill missing engagement values
    df[numeric_columns] = df[numeric_columns].fillna(0)


    # Convert upload date
    df["upload_date"] = pd.to_datetime(
        df["upload_date"],
        errors="coerce"
    )


    output_file.parent.mkdir(
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )


    print("Clean rows:", len(df))
    print("Saved:", output_file)


if __name__ == "__main__":
    clean_data()
