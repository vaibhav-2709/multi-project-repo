def simulate_savings(df, app_name, reduction_percent):
    """
    Simulate how much data can be saved
    """
    app_data = df[df['app'] == app_name]

    total_usage = app_data['data_usage'].sum()

    reduced_usage = total_usage * (1 - reduction_percent / 100)
    saved = total_usage - reduced_usage

    return saved


def generate_suggestions(df):
    """
    Generate smart optimization suggestions
    """
    suggestions = []

    app_usage = df.groupby('app')['data_usage'].sum().sort_values(ascending=False)

    for app, usage in app_usage.items():
        if usage > 100000:  # threshold
            suggestions.append(
                f"Reduce {app} usage by 20% to save approx {usage * 0.2:.2f} MB"
            )

    return suggestions