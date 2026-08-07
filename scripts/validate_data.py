import pandas as pd
from pathlib import Path


file_path = (
    Path(__file__).parent.parent
    / "data"
    / "raw"
    / "youtube_dataset.csv"
)


required_columns = [
    "video_id",
    "title",
    "channel",
    "views",
    "likes",
    "comments"
]


def validate():

    if not file_path.exists():
        print("Dataset not found")
        return False

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")


    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print(
            "Missing columns:",
            missing_columns
        )
        return False


    missing_values = df[required_columns].isnull().sum()

    print("\nMissing values:")
    print(missing_values)


    print("\nValidation complete")

    return True


if __name__ == "__main__":
    validate()