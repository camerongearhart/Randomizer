# Randomizer

A simple Python weighted random selection utility.

This class takes a dictionary of items and their associated weights/percentages, normalizes the values so they add up to `100`, and then randomly selects an item based on those weights.

## Example

```python
from randomizer import randomizer

items = {
    "common": 70,
    "rare": 25,
    "legendary": 5
}

r = randomizer(items)

print(r.getRandom())
```

Possible output:

```text
rare
```

## How It Works

The input dictionary should map item names to numeric weights:

```python
{
    "apple": 50,
    "banana": 30,
    "orange": 20
}
```

These values are treated as relative chances. They do **not** need to add up to exactly `100`.

For example:

```python
{
    "apple": 5,
    "banana": 3,
    "orange": 2
}
```

is equivalent to:

```python
{
    "apple": 50,
    "banana": 30,
    "orange": 20
}
```

The constructor automatically rescales the values so that the total is `100`.

## Class

### `randomizer`

```python
class randomizer:
    def __init__(self, items: Dict[str, float]):
        ...
```

Creates a weighted randomizer object.

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `items` | `Dict[str, float]` | A dictionary where each key is an item name and each value is that item's relative chance/weight. |

## Methods

### `getRandom`

```python
def getRandom(self) -> str:
    ...
```

Returns one randomly selected key from the dictionary based on the normalized weights.

### Returns

| Type | Description |
|---|---|
| `str` | The selected item name. |

## Example With Uneven Weights

```python
items = {
    "sword": 10,
    "shield": 30,
    "potion": 60
}

loot_table = randomizer(items)

for _ in range(10):
    print(loot_table.getRandom())
```

Since `"potion"` has the largest weight, it is the most likely result.

