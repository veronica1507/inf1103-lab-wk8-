from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self._percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self._percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        self._threshold = threshold
        self._amount = amount

    def apply(self, total: float) -> float:
        if total >= self._threshold:
            return total - self._amount
        return total