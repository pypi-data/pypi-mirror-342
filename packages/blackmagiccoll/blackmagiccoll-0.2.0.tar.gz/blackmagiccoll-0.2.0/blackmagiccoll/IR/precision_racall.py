def calculate_precision_recall_f1(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    return precision, recall, f1_score

tp = int(input("Enter the value for True Positives (TP): "))
fp = int(input("Enter the value for False Positives (FP): "))
fn = int(input("Enter the value for False Negatives (FN): "))


precision, recall, f1_score = calculate_precision_recall_f1(tp, fp, fn)

print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1_score:.4f}")
