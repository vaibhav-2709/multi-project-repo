def clean_column_names(df):
    """
    Clean column names:
    - Lowercase
    - Replace spaces with _
    - Remove special characters
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("/", "_", regex=False)
    )
    return df