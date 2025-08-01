def preprocess_data(df, config):
    # Drop columns
    if 'drop_columns' in config:
        df = df.drop(columns=config['drop_columns'], errors='ignore')

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

    # Optional: Add more logic (encode categoricals, normalize, etc.)

    return df
