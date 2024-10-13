from model import create_model
import unittest


class TestModel(unittest.TestCase):
    def test_model_initialization(self):
        model = create_model()
        self.assertIsNotNone(model, "Model should be initialized")

    def test_model_type(self):
        model = create_model()
        self.assertEqual(model.__class__.__name__, "LogisticRegression",
                         "Model should be LogisticRegression")


if __name__ == '__main__':
    unittest.main()
