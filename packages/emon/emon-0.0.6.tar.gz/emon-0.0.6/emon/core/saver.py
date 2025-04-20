import joblib
import json
import pandas as pd
import numpy as np

class ModelSaver:
    def __init__(self, cleaner):
        self.cleaner = cleaner
        
    def save(self, model, filename, model_type='joblib'):
        """Save model with comprehensive metadata"""
        # Ensure we have the original columns attribute
        if not hasattr(self.cleaner, 'original_columns'):
            self.cleaner.original_columns = getattr(self.cleaner, 'feature_columns', [])
        
        # Ensure we have the composite_splits attribute
        if not hasattr(self.cleaner, 'composite_splits'):
            self.cleaner.composite_splits = {}
        
        package = {
            'model': model,
            'metadata': {
                'class_mapping': self.cleaner.class_map,
                'target_column': self.cleaner.target_col,
                'feature_info': {
                    'original_columns': self.cleaner.original_columns,
                    'processed_columns': self.cleaner.processed_columns if hasattr(self.cleaner, 'processed_columns') else self.cleaner.original_columns,
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
        """Generate user-friendly guide with detailed metadata"""
        # Ensure we have the original columns attribute
        if not hasattr(self.cleaner, 'original_columns'):
            self.cleaner.original_columns = getattr(self.cleaner, 'feature_columns', [])
            
        # Create a more comprehensive guide with metadata
        guide = {
            'input_instructions': {
                'required_features': self.cleaner.original_columns,
                'composite_formats': {}
            },
            'class_labels': self.cleaner.class_map,
            'model_metadata': {
                'target_column': self.cleaner.target_col,
                'feature_encoders': list(self.cleaner.feature_encoders.keys()) if hasattr(self.cleaner, 'feature_encoders') else []
            }
        }
        
        # Add composite format information if available
        if hasattr(self.cleaner, 'composite_splits') and self.cleaner.composite_splits:
            guide['input_instructions']['composite_formats'] = {
                col: f"Use '{info.get('separator', '/')}' separator (e.g. '120{info.get('separator', '/')}80')"
                for col, info in self.cleaner.composite_splits.items()
            }
            
        # Add example input format based on the features
        guide['input_example'] = {
            feature: "<value>" for feature in self.cleaner.original_columns
        }
        
        # Write the guide to a JSON file
        with open(f"{filename}_guide.json", 'w') as f:
            json.dump(guide, f, indent=2)