import os
import shutil
import unittest
from dataflow.ml_logic.registry.local_registry import LocalModelRegistry
from dataflow.ml_logic.registry.singleton import SingletonABCMeta

class TestLocalModelRegistry(unittest.TestCase):
    TEST_DIR = os.path.join(os.getcwd(), "model_registry")

    def setUp(self):
        # Clear singleton instances to ensure fresh instance for each test
        SingletonABCMeta._instances.clear()

        print(f"📁 Using test directory: {self.TEST_DIR}")
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        self.registry = LocalModelRegistry(storage_dir=self.TEST_DIR)

    def tearDown(self):
        if os.path.exists(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
            SingletonABCMeta._instances.clear()

    def test_register_and_get_model(self):
        obj = {"a": 1, "b": 2}
        self.registry.register_model("foo", obj)
        loaded = self.registry.get_model("foo")
        self.assertEqual(obj, loaded)

    def test_list_models(self):
        self.registry.register_model("foo", 1)
        self.registry.register_model("bar", 2)
        models = self.registry.list_models()
        self.assertIn("foo", models)
        self.assertIn("bar", models)

    def test_delete_model(self):
        self.registry.register_model("foo", 1)
        self.registry.delete_model("foo")
        self.assertNotIn("foo", self.registry.list_models())
        with self.assertRaises(FileNotFoundError):
            self.registry.get_model("foo")

    def test_update_model(self):
        self.registry.register_model("foo", 1)
        self.registry.update_model("foo", 2)
        self.assertEqual(self.registry.get_model("foo"), 2)

    def test_get_missing_model(self):
        with self.assertRaises(FileNotFoundError):
            self.registry.get_model("missing")

    def test_delete_missing_model(self):
        with self.assertRaises(FileNotFoundError):
            self.registry.delete_model("missing")
