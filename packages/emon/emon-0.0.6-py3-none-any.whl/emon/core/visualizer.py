import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

class DataVisualizer:
    @staticmethod
    def show_class_balance(df, target_col):
        """Class distribution visualization"""
        plt.figure(figsize=(10, 6))
        sns.countplot(x=target_col, data=df)
        plt.title('Target Class Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
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
        plt.tight_layout()
        plt.show()
        
    @staticmethod
    def show_feature_distributions(df, target_col):
        """Visualize feature distributions by target class"""
        features = [col for col in df.columns if col != target_col]
        target_values = df[target_col].unique()
        
        # If there are too many features, only show the first 6
        if len(features) > 6:
            print(f"Showing distributions for the first 6 of {len(features)} features")
            features = features[:6]
            
        # Create a grid of plots for each feature
        fig, axes = plt.subplots(len(features), 1, figsize=(12, 4*len(features)))
        if len(features) == 1:
            axes = [axes]  # Ensure axes is always a list
            
        for i, feature in enumerate(features):
            if pd.api.types.is_numeric_dtype(df[feature]):
                # For numeric features, show KDE plots for each class
                for target_value in target_values:
                    subset = df[df[target_col] == target_value]
                    sns.kdeplot(subset[feature], ax=axes[i], label=str(target_value))
                axes[i].set_title(f'Distribution of {feature} by {target_col}')
                axes[i].legend()
            else:
                # For categorical features, show count plots
                sns.countplot(x=feature, hue=target_col, data=df, ax=axes[i])
                axes[i].set_title(f'Distribution of {feature} by {target_col}')
                axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.show()
        
    @staticmethod
    def show_correlation_matrix(df, target_col=None):
        """Visualize correlation matrix of features"""
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.shape[1] < 2:
            print("Not enough numeric features for correlation analysis")
            return
            
        plt.figure(figsize=(12, 10))
        corr = numeric_df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                    square=True, linewidths=.5, annot=True, fmt='.2f')
        
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.show()
        
    @staticmethod
    def show_pairplot(df, target_col, max_features=5):
        """Show pairwise relationships between features"""
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        
        if target_col in numeric_df.columns:
            numeric_df = numeric_df.drop(target_col, axis=1)
            
        # If there are too many features, select only the first few
        if numeric_df.shape[1] > max_features:
            print(f"Too many features for pairplot. Showing only {max_features} features.")
            numeric_df = numeric_df.iloc[:, :max_features]
            
        # Add back the target column
        plot_df = pd.concat([numeric_df, df[target_col]], axis=1)
        
        # Create the pairplot
        sns.pairplot(plot_df, hue=target_col, diag_kind='kde')
        plt.suptitle('Pairwise Feature Relationships', y=1.02)
        plt.tight_layout()
        plt.show()