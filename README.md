# Weighted Randomizer

A Python utility for weighted random selection of items. Useful for probabilistic distributions, lotteries, and random sampling with custom probabilities.

## Installation

```bash
pip install -e .
```

Or from PyPI (when published):
```bash
pip install weighted-randomizer
```

## Usage

```python
from randomizer import randomizer

# Create a randomizer with weighted items
items = {
    "apple": 35.0,
    "banana": 20.0,
    "cherry": 45.0,
}

r = randomizer(items)

# Get a random item based on weights
selected = r.getRandom()
print(selected)
```

## How It Works

The `randomizer` class normalizes weights to percentages (0-100), then uses cumulative weights to perform weighted random selection. Each item's probability of selection is proportional to its weight.

## Example Output

```
percents sum to over 100, percents have been scaled accordingly.
apple  # or banana, cherry based on weighted probability
```

## License

MIT
