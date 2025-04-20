import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re
import warnings

class DataCleaner:
    def __init__(self, target_col):
        self.target_col = target_col
        self.label_encoder = LabelEncoder()
        self.feature_encoders = {}
        self.class_map = {}
        self.date_columns = []
        self.original_columns = []
        self.processed_columns = []
        self.composite_splits = {}
        
    def clean(self, data_path):
        """Universal data cleaning pipeline"""
        # Handle different input types (file path or DataFrame)
        if isinstance(data_path, str):
            df = pd.read_csv(data_path)
        elif isinstance(data_path, pd.DataFrame):
            df = data_path.copy()
        else:
            raise ValueError("Input must be a file path or a pandas DataFrame")
            
        # Store original column names before any processing
        self.original_columns = [col for col in df.columns if col != self.target_col]
        
        self._validate_input(df)
        df = self._sanitize_data(df)
        df = self._process_features(df)
        self._encode_target(df)
        
        # Store processed column names after all processing
        self.processed_columns = [col for col in df.columns if col != self.target_col]
        
        return df

    def _validate_input(self, df):
        """Initial validation checks"""
        if self.target_col not in df.columns:
            raise ValueError(f"Target column '{self.target_col}' not found")
        if len(df) < 10:
            warnings.warn("Extremely small dataset (<10 rows)", UserWarning)

    def _sanitize_data(self, df):
        """Fix common data issues"""
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        for col in df.select_dtypes(include='object'):
            df[col] = df[col].astype(str).str.strip()
        return df.replace([np.inf, -np.inf], np.nan)

    def _process_features(self, df):
        """Automated feature engineering"""
        df = self._handle_missing(df)
        df = self._split_composite_features(df)
        df = self._process_datetime(df)
        df = self._encode_categoricals(df)
        return df

    def _handle_missing(self, df):
        """Type-aware imputation"""
        for col in df.columns:
            if col == self.target_col: continue
            if df[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0], inplace=True)
        return df

    def _split_composite_features(self, df):
        """Split numeric/numeric patterns like blood pressure (systolic/diastolic)"""
        for col in df.select_dtypes(include='object'):
            if col == self.target_col: continue
            # Look for patterns like '120/80', '120-80', '120:80'
            pattern = r'\d+[/:-]\d+'
            if df[col].str.contains(pattern).any():
                # Identify the separator character
                sample_val = df[col].str.extract(f'({pattern})').dropna().iloc[0, 0] if not df[col].str.extract(f'({pattern})').dropna().empty else None
                if sample_val:
                    separator = '/' if '/' in sample_val else ('-' if '-' in sample_val else ':')
                    
                    # Store the composite split information for metadata
                    self.composite_splits[col] = {'separator': separator}
                    
                    # Split the column into parts
                    parts = df[col].str.split(separator, expand=True)
                    valid = parts.dropna(how='all')
                    
                    if len(valid.columns) > 1:
                        for i in range(valid.shape[1]):
                            df[f"{col}_part_{i+1}"] = pd.to_numeric(parts[i], errors='coerce')
                        df.drop(col, axis=1, inplace=True)
        return df

    def _process_datetime(self, df):
        """Auto-detect and split datetime"""
        for col in df.select_dtypes(include='object'):
            try:
                df[col] = pd.to_datetime(df[col])
                for unit in ['year', 'month', 'day']:
                    df[f"{col}_{unit}"] = getattr(df[col].dt, unit)
                df.drop(col, axis=1, inplace=True)
                self.date_columns.append(col)
            except: pass
        return df

    def _encode_categoricals(self, df):
        """Encode non-target categoricals"""
        for col in df.select_dtypes(include='object'):
            if col == self.target_col: continue
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.feature_encoders[col] = le
        return df

    def _encode_target(self, df):
        """Preserve original label mapping"""
        original = df[self.target_col].unique()
        df[self.target_col] = self.label_encoder.fit_transform(df[self.target_col])
        self.class_map = {i: label for i, label in enumerate(self.label_encoder.classes_)}