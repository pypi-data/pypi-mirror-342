from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings

class ModelTrainer:
    def __init__(self, target_col, model_type='random_forest'):
        self.target_col = target_col
        self.model_type = model_type.lower()
        self.model = None
        self.class_distribution = None
        
    def train(self, df):
        """Universal model training with validation"""
        self._validate_dataset(df)
        X, y = self._split_features_target(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self._check_data_health(X_train, y_train)
        self.model = self._get_model()
        self.model.fit(X_train, y_train)
        
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
        return RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight='balanced'
        )

    def _evaluate(self, X_test, y_test):
        """Auto-evaluation metrics"""
        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"\nModel Evaluation:")
        print(f"- Test Accuracy: {acc:.2%}")
        print(f"- Class Distribution: {self.class_distribution}")