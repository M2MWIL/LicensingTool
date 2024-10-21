from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import accuracy_score, classification_report
class ModelHandler:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train_model(self, X_train, y_train):
        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        return self.model, accuracy, report

    def predict(self, X_test):
        return self.model.predict(X_test)

    def save_model(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self.model, file)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        with open(filepath, 'rb') as file:
            self.model = pickle.load(file)
        print(f"Model loaded from {filepath}")