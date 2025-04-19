import joblib
import json

class ModelSaver:
    def __init__(self, cleaner):
        self.cleaner = cleaner
        
    def save(self, model, filename, model_type='joblib'):
        """Save model with comprehensive metadata"""
        package = {
            'model': model,
            'metadata': {
                'class_mapping': self.cleaner.class_map,
                'target_column': self.cleaner.target_col,
                'feature_info': {
                    'original_columns': self.cleaner.original_columns,
                    'processed_columns': self.cleaner.original_columns,
                    'composite_splits': self.cleaner.composite_splits,
                    'encoders': list(self.cleaner.feature_encoders.keys())
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
        """Generate user-friendly guide"""
        guide = {
            'input_instructions': {
                'required_features': self.cleaner.original_columns,
                'composite_formats': {
                    col: f"Use '{info['separator']}' separator (e.g. '120{info['separator']}80')"
                    for col, info in self.cleaner.composite_splits.items()
                }
            },
            'class_labels': self.cleaner.class_map
        }
        with open(f"{filename}_guide.json", 'w') as f:
            json.dump(guide, f, indent=2)