from .core.cleaner import DataCleaner
from .core.trainer import ModelTrainer
from .core.saver import ModelSaver
from .core.visualizer import DataVisualizer
import pandas as pd
import os

_cleaner = None
_model = None
_current_dataset = None

def clean(data, target_col):
    """Clean and prepare data for modeling
    
    Args:
        data: Either a file path (CSV) or a pandas DataFrame
        target_col: The name of the target column to predict
        
    Returns:
        A cleaned pandas DataFrame ready for training
    """
    global _cleaner, _current_dataset
    try:
        _cleaner = DataCleaner(target_col)
        df = _cleaner.clean(data)
        _current_dataset = df.copy()
        print(f"Cleaned data: {df.shape[0]} rows, {df.shape[1]} features")
        print(f"Features: {_cleaner.original_columns}")
        return df
    except Exception as e:
        print(f"Cleaning failed: {str(e)}")
        raise

def train(df, target_col, model_type='random_forest'):
    """Train a model on the provided dataset
    
    Args:
        df: A pandas DataFrame with features and target column
        target_col: The name of the target column to predict
        model_type: Type of model to train ('random_forest', 'xgboost', 'gradient_boosting',
                   'logistic_regression', 'svm', 'knn', 'decision_tree')
        
    Returns:
        The trained model
    """
    global _model
    try:
        trainer = ModelTrainer(target_col, model_type)
        _model = trainer.train(df)
        return _model
    except Exception as e:
        print(f"Training failed: {str(e)}")
        raise

def model(filename, model_type='joblib'):
    """Save the trained model with metadata
    
    Args:
        filename: Path to save the model (without extension)
        model_type: Format to save the model in (currently only 'joblib' is supported)
        
    Returns:
        None
    """
    if not _model or not _cleaner:
        raise RuntimeError("Train model first using emon.train()")
    try:
        saver = ModelSaver(_cleaner)
        saver.save(_model, filename, model_type)
        print(f"Model saved to {filename}.joblib")
        print(f"Usage guide saved to {filename}_guide.json")
        print("\nThe guide contains:")
        print("- Required features for prediction")
        print("- Class labels mapping")
        print("- Input format instructions")
    except Exception as e:
        print(f"Saving failed: {str(e)}")
        raise

def visualize(df=None, target_col=None, plot_type='all'):
    """Visualize dataset and model insights
    
    Args:
        df: A pandas DataFrame (if None, uses the last cleaned dataset)
        target_col: The name of the target column (if None, uses the last cleaner's target)
        plot_type: Type of visualization ('class_balance', 'feature_importance',
                  'distributions', 'correlation', 'pairplot', or 'all')
        
    Returns:
        None
    """
    # Use current dataset if none provided
    if df is None:
        if _current_dataset is None:
            raise ValueError("No dataset available. Clean data first or provide a DataFrame.")
        df = _current_dataset
    
    # Use current target column if none provided
    if target_col is None:
        if _cleaner is None:
            raise ValueError("No target column specified. Clean data first or provide a target column.")
        target_col = _cleaner.target_col
    
    # Show visualizations based on the plot_type
    if plot_type in ['class_balance', 'all']:
        DataVisualizer.show_class_balance(df, target_col)
    
    if plot_type in ['feature_importance', 'all']:
        if _model and hasattr(_model, 'feature_importances_'):
            DataVisualizer.show_feature_importance(_model, df.drop(target_col, axis=1).columns)
        elif plot_type == 'feature_importance':
            print("No model with feature importances available.")
    
    if plot_type in ['distributions', 'all']:
        DataVisualizer.show_feature_distributions(df, target_col)
    
    if plot_type in ['correlation', 'all']:
        DataVisualizer.show_correlation_matrix(df, target_col)
    
    if plot_type in ['pairplot', 'all']:
        DataVisualizer.show_pairplot(df, target_col)

def load_model(filename):
    """Load a saved model with its metadata
    
    Args:
        filename: Path to the saved model file (.joblib)
        
    Returns:
        A tuple of (model, metadata)
    """
    import joblib
    try:
        filename = filename if filename.endswith('.joblib') else f"{filename}.joblib"
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Model file not found: {filename}")
            
        package = joblib.load(filename)
        model = package['model']
        metadata = package['metadata']
        
        print(f"Model loaded successfully from {filename}")
        print(f"Target column: {metadata['target_column']}")
        print(f"Class mapping: {metadata['class_mapping']}")
        print(f"Required features: {metadata['feature_info']['original_columns']}")
        
        return model, metadata
    except Exception as e:
        print(f"Loading model failed: {str(e)}")
        raise

def predict(model, data, metadata=None):
    """Make predictions using a trained model
    
    Args:
        model: A trained model
        data: Input data as a pandas DataFrame or dictionary
        metadata: Model metadata (optional if using a model from load_model)
        
    Returns:
        Predictions with class labels
    """
    try:
        # Convert dictionary to DataFrame if needed
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        # Ensure we have the required features
        if metadata and 'feature_info' in metadata:
            required_features = metadata['feature_info']['original_columns']
            missing_features = [f for f in required_features if f not in data.columns]
            if missing_features:
                raise ValueError(f"Missing required features: {missing_features}")
        
        # Make predictions
        predictions = model.predict(data)
        
        # Convert numeric predictions to class labels if metadata is available
        if metadata and 'class_mapping' in metadata:
            class_mapping = metadata['class_mapping']
            predictions = [class_mapping.get(str(p), class_mapping.get(p, p)) for p in predictions]
        
        return predictions
    except Exception as e:
        print(f"Prediction failed: {str(e)}")
        raise
