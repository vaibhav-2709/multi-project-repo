import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib


def prepare_features(df):
    """
    Convert categorical data to numeric
    """
    df = df.copy()

    # One-hot encoding for app
    df = pd.get_dummies(df, columns=['app'], drop_first=True)

    # Encode gender
    df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})

    return df


def train_model(df):
    """
    Train regression model
    """
    df = prepare_features(df)

    X = df.drop(columns=['data_usage'])
    y = df['data_usage']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5

    print("\n--- MODEL PERFORMANCE ---")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

    # Save model
    joblib.dump(model, "models/data_usage_model.pkl")

    return model