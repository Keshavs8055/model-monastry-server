def preprocess_data(df, config):
    # Strip and lowercase DataFrame column names
    df.columns = df.columns.str.strip().str.lower()

    # Drop columns
    if 'drop_columns' in config:
        drop_cols = config['drop_columns']

        # If accidentally passed a single string
        if isinstance(drop_cols, str):
            drop_cols = [drop_cols]

        # Normalize config column names to lowercase
        drop_cols = [col.strip().lower() for col in drop_cols]

        print("Columns in df:", df.columns.tolist())
        print("Columns to drop:", drop_cols)

        df = df.drop(columns=drop_cols, errors='ignore')

    # Drop NA rows
    if config.get('drop_na_rows'):
        df = df.dropna()

    # Fill missing values
    fill_method = config.get('fill_missing')
    if fill_method == 'mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif fill_method == 'median':
        df = df.fillna(df.median(numeric_only=True))
    elif fill_method == 'mode':
        df = df.fillna(df.mode().iloc[0])

    return df
