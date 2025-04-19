from .core.cleaner import DataCleaner
from .core.trainer import ModelTrainer
from .core.saver import ModelSaver
from .core.visualizer import DataVisualizer

_cleaner = None
_model = None

def clean(data_path, target_col):
    global _cleaner
    try:
        _cleaner = DataCleaner(target_col)
        df = _cleaner.clean(data_path)
        print(f"Cleaned data: {df.shape[0]} rows, {df.shape[1]} features")
        return df
    except Exception as e:
        print(f"Cleaning failed: {str(e)}")
        raise

def train(df, target_col, model_type='random_forest'):
    global _model
    try:
        trainer = ModelTrainer(target_col, model_type)
        _model = trainer.train(df)
        return _model
    except Exception as e:
        print(f"Training failed: {str(e)}")
        raise

def model(filename, model_type='joblib'):
    if not _model or not _cleaner:
        raise RuntimeError("Train model first using emon.train()")
    try:
        saver = ModelSaver(_cleaner)
        saver.save(_model, filename, model_type)
        print(f"Model saved to {filename}")
    except Exception as e:
        print(f"Saving failed: {str(e)}")
        raise

def visualize(df, target_col):
    DataVisualizer.show_class_balance(df, target_col)
    if _model and hasattr(_model, 'feature_importances_'):
        DataVisualizer.show_feature_importance(_model, df.drop(target_col, axis=1).columns)