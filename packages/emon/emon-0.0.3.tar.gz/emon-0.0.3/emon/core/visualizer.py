import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualizer:
    @staticmethod
    def show_class_balance(df, target_col):
        """Class distribution visualization"""
        plt.figure(figsize=(10, 6))
        sns.countplot(x=target_col, data=df)
        plt.title('Target Class Distribution')
        plt.xticks(rotation=45)
        plt.show()

    @staticmethod
    def show_feature_importance(model, feature_names):
        """Model interpretation visualization"""
        plt.figure(figsize=(12, 6))
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        plt.title("Feature Importances")
        plt.bar(range(len(indices)), importances[indices])
        plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=90)
        plt.show()