from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import warnings

class ModelTrainer:
    def __init__(self, target_col, model_type='random_forest'):
        self.target_col = target_col
        self.model_type = model_type.lower()
        self.model = None
        self.class_distribution = None
        self.feature_columns = []
        self.scaler = None
        self.metrics = {}
        
    def train(self, df):
        """Universal model training with validation"""
        self._validate_dataset(df)
        X, y = self._split_features_target(df)
        
        # Store feature column names for later use
        self.feature_columns = X.columns.tolist()
        
        # Scale features if needed
        if self.model_type in ['svm', 'logistic_regression', 'knn']:
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self._check_data_health(X_train, y_train)
        self.model = self._get_model()
        
        # Train the model
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        self._evaluate(X_test, y_test)
        return self.model

    def _validate_dataset(self, df):
        """Critical validations"""
        if self.target_col not in df.columns:
            raise ValueError(f"Target column '{self.target_col}' missing")
        if len(df) < 10:
            raise ValueError("Insufficient data (<10 rows)")
        if df[self.target_col].nunique() < 2:
            raise ValueError("Target requires at least 2 classes")

    def _split_features_target(self, df):
        """Separate features and target"""
        return df.drop(self.target_col, axis=1), df[self.target_col]

    def _check_data_health(self, X, y):
        """Warnings and recommendations"""
        if len(X) < 50:
            warnings.warn(f"Small dataset ({len(X)} rows)", UserWarning)
            
        class_counts = y.value_counts(normalize=True)
        self.class_distribution = class_counts.to_dict()
        
        if any(prob < 0.1 for prob in class_counts):
            imbalance = [cls for cls, prob in class_counts.items() if prob < 0.1]
            warnings.warn(f"Imbalanced classes: {imbalance}", UserWarning)

    def _get_model(self):
        """Model selection with safety defaults"""
        if self.model_type == 'xgboost':
            return XGBClassifier(
                max_depth=5,
                learning_rate=0.1,
                random_state=42,
                eval_metric='logloss'
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                random_state=42
            )
        elif self.model_type == 'logistic_regression':
            return LogisticRegression(
                C=1.0,
                max_iter=1000,
                random_state=42,
                class_weight='balanced'
            )
        elif self.model_type == 'svm':
            return SVC(
                C=1.0,
                kernel='rbf',
                probability=True,
                random_state=42,
                class_weight='balanced'
            )
        elif self.model_type == 'knn':
            return KNeighborsClassifier(
                n_neighbors=5,
                weights='uniform'
            )
        elif self.model_type == 'decision_tree':
            return DecisionTreeClassifier(
                max_depth=5,
                random_state=42,
                class_weight='balanced'
            )
        else:  # default to random_forest
            return RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight='balanced'
            )

    def _evaluate(self, X_test, y_test):
        """Auto-evaluation metrics with comprehensive reporting"""
        # Make predictions
        preds = self.model.predict(X_test)
        
        # Calculate metrics
        acc = accuracy_score(y_test, preds)
        report = classification_report(y_test, preds, output_dict=True)
        conf_matrix = confusion_matrix(y_test, preds)
        
        # Store metrics for later use
        self.metrics = {
            'accuracy': acc,
            'classification_report': report,
            'confusion_matrix': conf_matrix.tolist()
        }
        
        # Cross-validation score
        if len(y_test) >= 10:  # Only do cross-validation if we have enough data
            try:
                cv_scores = cross_val_score(self.model, X_test, y_test, cv=min(5, len(y_test)//2))
                self.metrics['cv_scores'] = cv_scores.tolist()
                self.metrics['cv_mean'] = cv_scores.mean()
            except Exception as e:
                print(f"Cross-validation skipped: {str(e)}")
        
        # Print evaluation results
        print(f"\nModel Evaluation:")
        print(f"- Test Accuracy: {acc:.2%}")
        print(f"- Class Distribution: {self.class_distribution}")
        
        # Print classification report
        print("\nClassification Report:")
        for class_name, metrics in report.items():
            if class_name in ['accuracy', 'macro avg', 'weighted avg']:
                continue
            print(f"- Class '{class_name}': Precision={metrics['precision']:.2f}, Recall={metrics['recall']:.2f}, F1-Score={metrics['f1-score']:.2f}")
        
        # Print cross-validation results if available
        if 'cv_mean' in self.metrics:
            print(f"\nCross-Validation Accuracy: {self.metrics['cv_mean']:.2%}")