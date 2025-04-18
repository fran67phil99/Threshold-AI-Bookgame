import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import Callback
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

class TestEvalCallback(Callback):
    def __init__(self, X_test, y_test):
        super().__init__()
        self.X_test = X_test
        self.y_test = y_test
        self.test_loss = []
        self.test_acc = []

    def on_epoch_end(self, epoch, logs=None):
        loss, acc = self.model.evaluate(self.X_test, self.y_test, verbose=0)
        self.test_loss.append(loss)
        self.test_acc.append(acc)

class AgentBrain:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.label_binarizer = LabelBinarizer()
        self.model = None
        self.texts = []
        self.labels = []

    def train(self, texts, labels, test_size=0.2):
        self.texts = list(texts)
        self.labels = list(labels)
        X = self.vectorizer.fit_transform(self.texts).toarray()
        y = self.label_binarizer.fit_transform(self.labels)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        self.model = Sequential([
            Dense(16, activation='relu', input_shape=(X.shape[1],)),
            Dropout(0.3),
            Dense(8, activation='relu'),
            Dropout(0.3),
            Dense(y.shape[1], activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        test_callback = TestEvalCallback(X_test, y_test)
        history = self.model.fit(
            X_train, y_train,
            epochs=100,
            verbose=0,
            validation_split=0.2,
            callbacks=[test_callback]
        )

        # Visualizza i grafici
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Val Loss')
        plt.plot(test_callback.test_loss, label='Test Loss', linestyle='dashed', color='red')
        plt.legend()
        plt.title('Loss')
        plt.subplot(1, 2, 2)
        plt.plot(history.history['accuracy'], label='Train Acc')
        plt.plot(history.history['val_accuracy'], label='Val Acc')
        plt.plot(test_callback.test_acc, label='Test Acc', linestyle='dashed', color='red')
        plt.legend()
        plt.title('Accuracy')
        plt.show()

        # Valutazione sul training set
        train_pred = self.model.predict(X_train)
        train_pred_labels = self.label_binarizer.inverse_transform(train_pred)
        train_labels = self.label_binarizer.inverse_transform(y_train)
        train_acc = accuracy_score(train_labels, train_pred_labels)
        print(f"Train accuracy: {train_acc:.2f}")
        # Valutazione sul test set
        if len(X_test) > 0:
            y_pred = self.model.predict(X_test)
            y_pred_labels = self.label_binarizer.inverse_transform(y_pred)
            y_test_labels = self.label_binarizer.inverse_transform(y_test)
            acc = accuracy_score(y_test_labels, y_pred_labels)
            print(f"Test accuracy: {acc:.2f}")

    def learn(self, new_text, new_label):
        self.texts.append(new_text)
        self.labels.append(new_label)
        self.train(self.texts, self.labels)

    def predict_intent(self, text):
        X = self.vectorizer.transform([text]).toarray()
        pred = self.model.predict(X)
        label = self.label_binarizer.inverse_transform(pred)[0]
        return label