# Weighted Randomizer

A Python utility for weighted random selection of named items, with support for
repeated draws and draws without replacement. Each item's probability is
proportional to its weight.

## Installation

Requires Python 3.8 or newer. From the project directory, install the package in
editable mode:

```bash
python -m pip install -e .
```

## Usage

```python
from weighted_randomizer import randomizer

# Create a randomizer with weighted items
items = {
    "apple": 35.0,
    "banana": 20.0,
    "cherry": 45.0,
}

r = randomizer(items.copy())

# Get a random item based on weights
selected = r.getRandom()
print(selected)
```

This example selects `"apple"` with a 35% probability, `"banana"` with 20%, and
`"cherry"` with 45%. Each call to `getRandom()` uses the full original pool, so
items can be selected more than once.

### Draw without replacement

Use `getRandomAndRemove()` to draw without replacement:

```python
from weighted_randomizer import randomizer

r = randomizer({"1": 1, "2": 1, "3": 1})
selected = r.getRandomAndRemove()  # For example, "2"
next_selected = r.getRandomAndRemove()  # Then only "1" or "3"
original_pool_selection = r.getRandom()  # Still any of "1", "2", or "3"
```

This method keeps its own pool and preserves the relative weights of the
remaining items. Calls to `getRandom()` do not change this pool. After every item
has been removed, `getRandomAndRemove()` raises `ValueError`. Create a new
randomizer to start a fresh pool.

Use `generateRandomOrder()` to return all items in a weighted random order:

```python
r = randomizer({"apple": 60, "banana": 30, "cherry": 10})
order = r.generateRandomOrder()  # For example, ["apple", "cherry", "banana"]
```

Each item appears exactly once. Apple has a 60% chance of being first; each
subsequent position uses the remaining items' relative weights. For example,
after apple is selected, banana has a 75% chance of being next (30 out of 40).
Every call generates a fresh order and leaves both `getRandom()` and
`getRandomAndRemove()` pools unchanged. Zero-weight items are shuffled after
all positive-weight items.

## Weights and behavior

- Pass a nonempty dictionary mapping item names to positive numeric weights.
  Weights do not need to add up to 100: weights of `7`, `4`, and `9` give the same
  probabilities as `35`, `20`, and `45`.
- The constructor normalizes weights to percentages. It modifies the supplied
  dictionary's values, so pass `items.copy()` to preserve your original weights.
- If the original total is below or above 100, the constructor prints a message
  explaining that the weights have been scaled. A total of 100 prints no message.
- `getRandom()` selects using cumulative normalized weights.
  `getRandomAndRemove()` selects using the remaining items' relative weights and
  removes the selected item from its separate pool.
- Inputs are not explicitly validated. Empty dictionaries, negative or non-finite
  weights, and totals of zero are unsupported and may cause errors or unreliable
  results.

## Tests

Run the without-replacement tests from the project directory:

```bash
python -m unittest test_without_replacement.py
```

These tests cover weighted selection, pool exhaustion, independence from
`getRandom()`, and separate pools for separate instances in both the top-level
module and the package.

## License

Licensed under the [MIT License](LICENSE).
