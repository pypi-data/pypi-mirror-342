import pandas as pd

class SmartPredictor:
    def __init__(self, model_package):
        self.model = model_package['model']
        self.metadata = model_package['metadata']
        
    def predict(self, user_data):
        """Handle raw user input automatically"""
        df = pd.DataFrame([user_data])
        df = self._sanitize_input(df)
        df = self._process_composites(df)
        df = self._encode_features(df)
        df = self._align_features(df)
        return self.model.predict(df)[0]
    
    def _sanitize_input(self, df):
        """Clean user input columns"""
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        return df
    
    def _process_composites(self, df):
        """Split composite features"""
        for col, info in self.metadata['feature_info']['composite_splits'].items():
            if col in df.columns:
                parts = df[col].astype(str).str.split(info['separator'], expand=True)
                for i, new_col in enumerate(info['new_columns']):
                    df[new_col] = pd.to_numeric(parts[i], errors='coerce')
                df.drop(col, axis=1, inplace=True)
        return df
    
    def _encode_features(self, df):
        """Apply stored encoders"""
        for col in self.metadata['feature_info']['encoders']:
            if col in df.columns:
                le = LabelEncoder()
                le.classes_ = self.metadata['feature_info']['encoders'][col]
                df[col] = le.transform(df[col])
        return df
    
    def _align_features(self, df):
        """Ensure correct feature order"""
        return df[self.metadata['feature_info']['processed_columns']]
    
    def get_class_label(self, prediction):
        return self.metadata['class_mapping'].get(prediction, "Unknown")