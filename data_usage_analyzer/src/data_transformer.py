import pandas as pd

def get_app_distribution(row):
    """
    Personalized distribution based on user behavior and age
    """
    behavior = row['user_behavior_class']
    age = row['age']

    if behavior >= 4:
        youtube = 0.50
    else:
        youtube = 0.30

    if age < 25:
        instagram = 0.30
    else:
        instagram = 0.20

    whatsapp = 0.15
    facebook = 0.10

    others = 1 - (youtube + instagram + whatsapp + facebook)

    return {
        "YouTube": youtube,
        "Instagram": instagram,
        "WhatsApp": whatsapp,
        "Facebook": facebook,
        "Others": others
    }


def convert_to_app_level(df):
    rows = []

    for _, row in df.iterrows():
        distribution = get_app_distribution(row)

        total_time = row['app_usage_time_min_day']
        total_data = row['data_usage_mb_day']

        for app, ratio in distribution.items():
            rows.append({
                "user_id": row['user_id'],
                "app": app,
                "usage_time": total_time * ratio,
                "data_usage": total_data * ratio,
                "user_behavior_class": row['user_behavior_class'],
                "age": row['age'],
                "gender": row['gender']
            })

    return pd.DataFrame(rows)


def save_processed_data(df, path):
    df.to_csv(path, index=False)