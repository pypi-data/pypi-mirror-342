from collections import Counter
import warnings

def validate_dataset(df, target):
    if df.shape[0] < 50:
        warnings.warn("Dataset has less than 50 rows. Accuracy may be unreliable.")

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")

    class_counts = Counter(df[target])
    if len(class_counts) < 2:
        raise ValueError("Target must have at least 2 unique classes.")

    print(f"[emon.validate] Class distribution: {class_counts}")
    if min(class_counts.values()) / max(class_counts.values()) < 0.2:
        warnings.warn("Target classes are imbalanced.")
