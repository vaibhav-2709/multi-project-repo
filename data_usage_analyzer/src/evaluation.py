def evaluate_savings(df):
    """
    Evaluate how much data is saved after optimization
    """
    total_before = df['data_usage'].sum()

    # Top 3 data-consuming apps
    app_usage = df.groupby('app')['data_usage'].sum().sort_values(ascending=False)
    top_apps = app_usage.head(3).index

    df_copy = df.copy()

    # Apply 20% reduction
    for app in top_apps:
        df_copy.loc[df_copy['app'] == app, 'data_usage'] *= 0.8

    total_after = df_copy['data_usage'].sum()

    savings = total_before - total_after
    percent = (savings / total_before) * 100

    print("\n--- SAVINGS EVALUATION ---")
    print(f"Before Optimization: {total_before:.2f} MB")
    print(f"After Optimization: {total_after:.2f} MB")
    print(f"Total Saved: {savings:.2f} MB")
    print(f"Percentage Reduction: {percent:.2f}%")

    return percent