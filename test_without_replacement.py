import importlib
import unittest
from unittest.mock import patch


class WithoutReplacementTests(unittest.TestCase):
    def test_weighted_draws_and_original_pool_are_independent(self):
        for module_name in ("randomizer", "weighted_randomizer.randomizer"):
            with self.subTest(module=module_name):
                module = importlib.import_module(module_name)
                selector = module.randomizer({"1": 20, "2": 30, "3": 50})
                with patch.object(module.random, "choices", return_value=["2"]) as draw:
                    self.assertEqual(selector.getRandomAndRemove(), "2")
                    draw.assert_called_once_with(
                        ["1", "2", "3"], weights=[20, 30, 50], k=1
                    )

                with patch.object(module.random, "uniform", return_value=25):
                    self.assertEqual(selector.getRandom(), "2")

                with patch.object(module.random, "choices", return_value=["3"]) as draw:
                    self.assertEqual(selector.getRandomAndRemove(), "3")
                    draw.assert_called_once_with(["1", "3"], weights=[20, 50], k=1)

                self.assertEqual(selector.getRandomAndRemove(), "1")
                with self.assertRaisesRegex(ValueError, "No items remaining"):
                    selector.getRandomAndRemove()

                for seed, expected in ((10, "1"), (25, "2"), (75, "3")):
                    with patch.object(module.random, "uniform", return_value=seed):
                        self.assertEqual(selector.getRandom(), expected)

    def test_each_instance_has_an_independent_pool(self):
        for module_name in ("randomizer", "weighted_randomizer.randomizer"):
            with self.subTest(module=module_name):
                module = importlib.import_module(module_name)
                first = module.randomizer({"only": 100})
                second = module.randomizer({"only": 100})
                self.assertEqual(first.getRandomAndRemove(), "only")
                with self.assertRaises(ValueError):
                    first.getRandomAndRemove()
                self.assertEqual(second.getRandomAndRemove(), "only")


if __name__ == "__main__":
    unittest.main()
