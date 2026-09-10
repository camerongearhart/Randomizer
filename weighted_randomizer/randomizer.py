from typing import Dict, List
import random


class randomizer:
    """Weighted random selector for probabilistic item selection."""
    
    objects: Dict[str, float]
    
    def __init__(self, items: Dict[str, float]):
        """Initialize with items and their weights.
        
        Args:
            items: Dictionary mapping item names to weights (can be any positive numbers)
        """
        self.objects = items

        percentTotal: float = 0
        for key, value in self.objects.items():
            percentTotal += value
    
        for key, value in self.objects.items():
            self.objects[key] = self.objects[key] * 100.0 / percentTotal

        self.objects = dict(sorted(self.objects.items(), key=lambda item: item[1], reverse=False))
        self._remaining = self.objects.copy()

        if (percentTotal < 100):
            print("percents sum to less than 100%, percents have been scaled up.")
        elif (percentTotal > 100):
            print("percents sum to over 100, percents have been scaled accordingly.")

    def getRandom(self) -> str:
        """Select a random item based on weighted probabilities.
        
        Returns:
            The selected item name with probability proportional to its weight.
        """
        seed = random.uniform(0, 100)
        cumulative = 0
        for key, value in self.objects.items():
            cumulative += value
            if seed < cumulative:
                return key
        raise ValueError("error")

    def generateRandomOrder(self) -> List[str]:
        """Return every item once, drawing by remaining relative weights.

        Each call uses a fresh pool without changing the selector's state.
        Zero-weight items follow positive-weight items in shuffled order.
        """
        remaining = self.objects.copy()
        order = []
        while remaining:
            if not any(remaining.values()):
                tail = list(remaining)
                random.shuffle(tail)
                order.extend(tail)
                break
            selected = random.choices(
                list(remaining), weights=list(remaining.values()), k=1
            )[0]
            order.append(selected)
            del remaining[selected]
        return order

    def getRandomAndRemove(self) -> str:
        """Draw by weight without replacement, independently of getRandom().

        Raises:
            ValueError: If all items have already been drawn.
        """
        if not self._remaining:
            raise ValueError("No items remaining to select.")
        selected = random.choices(
            list(self._remaining), weights=list(self._remaining.values()), k=1
        )[0]
        del self._remaining[selected]
        return selected
