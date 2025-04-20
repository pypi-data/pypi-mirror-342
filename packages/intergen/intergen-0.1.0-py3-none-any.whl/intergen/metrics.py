import numpy as np
from sklearn.metrics import r2_score

def evaluate_model(model, X_train, y_train, X_test, y_test):
    train_preds = model.predict(X_train).flatten()
    test_preds = model.predict(X_test).flatten()
    return {
        "train_loss": np.mean((y_train - train_preds)**2),
        "test_loss": np.mean((y_test - test_preds)**2),
        "train_mae": np.mean(np.abs(y_train - train_preds)),
        "test_mae": np.mean(np.abs(y_test - test_preds)),
        "r2": r2_score(y_test, test_preds)
    }