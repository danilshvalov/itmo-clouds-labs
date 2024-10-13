from model import create_model
import pandas as pd
import unittest


class TestModel(unittest.TestCase):
    def test_model_initialization(self):
        model = create_model()
        self.assertIsNotNone(model, "Model should be initialized")

    def test_model_type(self):
        model = create_model()
        self.assertEqual(model.__class__.__name__, "LogisticRegression",
                         "Model should be LogisticRegression")

    def test_model_training(self):
        model = create_model()
        data = pd.DataFrame({
            'feature1': [1.0, 2.0, 3.0, 4.0, 5.0],
            'feature2': [2.0, 3.0, 3.5, 5.0, 5.5],
            'target': [0, 0, 1, 1, 1]
        })
        X = data[['feature1', 'feature2']]
        y = data['target']
        model.fit(X, y)
        predictions = model.predict(X)
        self.assertEqual(len(predictions), len(
            y), "Predictions should match the number of samples")


if __name__ == '__main__':
    unittest.main()
