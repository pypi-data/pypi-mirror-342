import joblib
import json

class ModelSaver:
    def __init__(self, cleaner):
        self.cleaner = cleaner
        
    def save(self, model, filename, model_type='joblib'):
        """Universal model saving with metadata"""
        package = {
            'model': model,
            'metadata': {
                'class_mapping': self.cleaner.class_map,
                'target_column': self.cleaner.target_col,
                'feature_encoders': {
                    col: encoder.classes_.tolist()
                    for col, encoder in self.cleaner.feature_encoders.items()
                }
            }
        }
        
        if model_type == 'joblib':
            filename = filename.removesuffix('.joblib') + '.joblib'
            joblib.dump(package, filename)
        else:
            raise ValueError("Only joblib format supported")
        
        self._save_human_readable(filename)
        
    def _save_human_readable(self, filename):
        """Save metadata as JSON"""
        with open(f"{filename}.metadata.json", 'w') as f:
            json.dump(self.cleaner.class_map, f)