import matplotlib.pyplot as plt

def plot_app_usage(df):
    app_usage = df.groupby('app')['data_usage'].sum()

    plt.figure()
    app_usage.plot(kind='bar')
    plt.title("Total Data Usage per App")
    plt.xlabel("App")
    plt.ylabel("Data Usage (MB)")
    plt.show()


def plot_user_behavior(df):
    behavior = df.groupby('user_behavior_class')['data_usage'].sum()

    plt.figure()
    behavior.plot(kind='bar')
    plt.title("Data Usage by User Behavior Class")
    plt.xlabel("Behavior Class")
    plt.ylabel("Data Usage (MB)")
    plt.show()