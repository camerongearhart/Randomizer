import importlib
import random
import unittest
from unittest.mock import patch


class RandomOrderTests(unittest.TestCase):
    def test_orders_are_complete_and_leave_draw_pool_unchanged(self):
        for name in ("randomizer", "weighted_randomizer.randomizer"):
            with self.subTest(module=name):
                module = importlib.import_module(name)
                selector = module.randomizer({"apple": 60, "banana": 30, "cherry": 10})
                selector.getRandomAndRemove()
                original = selector.objects.copy()
                remaining = selector._remaining.copy()
                for _ in range(5):
                    order = selector.generateRandomOrder()
                    self.assertCountEqual(order, original)
                self.assertEqual(selector.objects, original)
                self.assertEqual(selector._remaining, remaining)

    def test_first_and_subsequent_positions_follow_relative_weights(self):
        for name in ("randomizer", "weighted_randomizer.randomizer"):
            with self.subTest(module=name):
                module = importlib.import_module(name)
                selector = module.randomizer({"apple": 60, "banana": 30, "cherry": 10})
                rng = random.Random(42)
                with patch.object(module.random, "choices", side_effect=rng.choices):
                    orders = [selector.generateRandomOrder() for _ in range(20000)]
                apple_first = [order for order in orders if order[0] == "apple"]
                self.assertAlmostEqual(len(apple_first) / len(orders), 0.6, delta=0.02)
                self.assertAlmostEqual(
                    sum(order[1] == "banana" for order in apple_first) / len(apple_first),
                    0.75, delta=0.02,
                )

    def test_empty_singleton_and_zero_weight_items(self):
        for name in ("randomizer", "weighted_randomizer.randomizer"):
            with self.subTest(module=name):
                module = importlib.import_module(name)
                self.assertEqual(module.randomizer({}).generateRandomOrder(), [])
                self.assertEqual(module.randomizer({"only": 100}).generateRandomOrder(), ["only"])
                order = module.randomizer({"zero": 0, "also_zero": 0, "positive": 100}).generateRandomOrder()
                self.assertEqual(order[0], "positive")
                self.assertCountEqual(order, ["zero", "also_zero", "positive"])


if __name__ == "__main__":
    unittest.main()
