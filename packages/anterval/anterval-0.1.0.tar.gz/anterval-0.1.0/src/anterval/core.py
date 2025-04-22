from __future__ import annotations

from typing import Generic, TypeVar, override

T = TypeVar("T")


class Interval(Generic[T]):
    def __init__(
        self,
        start: T,
        end: T,
        left_closed: bool = True,
        right_closed: bool = False,
    ) -> None:
        """Initializes the Interval.

        Args:
            start: Start of the interval.
            end: End of the interval.
            left_closed: True if the interval is closed on the left, False otherwise.
            right_closed: True if the interval is closed on the right, False otherwise.

        Raises:
            ValueError: If the interval boundaries are invalid.

        """
        if start > end or (start == end and (not left_closed or not right_closed)):
            raise ValueError("Invalid interval boundaries.")
        self.start: T = start
        self.end: T = end
        self.left_closed: bool = left_closed
        self.right_closed: bool = right_closed

    @override
    def __repr__(self) -> str:
        """String representation of the interval."""
        left_bracket = "[" if self.left_closed else "("
        right_bracket = "]" if self.right_closed else ")"
        return f"{left_bracket}{self.start}, {self.end}{right_bracket}"

    def contains(self, value: T) -> bool:
        """Checks if a given value is within the interval.

        Args:
            value: The value to check.

        Returns:
            bool: True if the value is within the interval, False otherwise.

        """
        left_check: bool = value > self.start or (
            self.left_closed and value == self.start
        )
        right_check: bool = value < self.end or (
            self.right_closed and value == self.end
        )
        return left_check and right_check

    def intersection(self, other: Interval[T]) -> Interval[T] | None:
        """Returns the intersection of this interval with another.

        Args:
            other: The other interval.

        Returns:
            Optional[Interval[T]]: The intersection interval, or None if they don't overlap.

        """
        new_start = max(
            (self.start, self.left_closed), (other.start, other.left_closed),
        )
        new_end = min((self.end, self.right_closed), (other.end, other.right_closed))
        if new_start[0] < new_end[0] or (
            new_start[0] == new_end[0] and new_start[1] and new_end[1]
        ):
            return Interval(new_start[0], new_end[0], new_start[1], new_end[1])
        return None

    def union(self, other: Interval[T]) -> Interval[T] | None:
        """Returns the union of this interval with another if they overlap or are contiguous.

        Args:
            other: The other interval.

        Returns:
            Optional[Interval[T]]: The union interval, or None if they don't overlap.

        """
        if self.end < other.start or (
            self.end == other.start and not (self.right_closed or other.left_closed)
        ):
            return None  # Non-overlapping
        if other.end < self.start or (
            other.end == self.start and not (other.right_closed or self.left_closed)
        ):
            return None  # Non-overlapping

        new_start = min(
            (self.start, self.left_closed), (other.start, other.left_closed),
        )
        new_end = max((self.end, self.right_closed), (other.end, other.right_closed))
        return Interval(new_start[0], new_end[0], new_start[1], new_end[1])

    def difference(self, other: Interval[T]) -> list[Interval[T]]:
        """Returns the difference of this interval with another.

        Args:
            other: The other interval.

        Returns:
            list[Interval[T]]: A list of intervals after subtracting the other interval.

        """
        if other.start >= self.end or other.end <= self.start:
            # No overlap
            return [self]

        intervals: list[Interval[T]] = []
        if other.start > self.start or (
            other.start == self.start and not other.left_closed
        ):
            intervals.append(
                Interval(
                    self.start, other.start, self.left_closed, not other.left_closed,
                ),
            )
        if other.end < self.end or (other.end == self.end and not other.right_closed):
            intervals.append(
                Interval(other.end, self.end, not other.right_closed, self.right_closed),
            )
        return intervals

    def complement(self, universe_start: T, universe_end: T) -> list[Interval[T]]:
        """Returns the complement of this interval within a specified universe.

        Args:
            universe_start: Start of the universe.
            universe_end: End of the universe.

        Returns:
            list[Interval[T]]: A list of intervals representing the complement.

        Raises:
            ValueError: If the universe boundaries are invalid.

        """
        if universe_start >= universe_end:
            raise ValueError("Universe start must be before universe end.")

        intervals: list[Interval[T]] = []
        if self.start > universe_start or (
            self.start == universe_start and not self.left_closed
        ):
            intervals.append(
                Interval(universe_start, self.start, True, not self.left_closed),
            )
        if self.end < universe_end or (
            self.end == universe_end and not self.right_closed
        ):
            intervals.append(
                Interval(self.end, universe_end, not self.right_closed, True),
            )
        return intervals

    def __lt__(self, other: Interval[T]) -> bool:
        """Lexicographic ordering of intervals.
        """
        return (self.start, self.end, self.left_closed, self.right_closed) < (
            other.start,
            other.end,
            other.left_closed,
            other.right_closed,
        )

    def __le__(self, other: Interval[T]) -> bool:
        return self < other or self == other

    def __ge__(self, other: Interval[T]) -> bool:
        return self > other or self == other

    def __gt__(self, other: Interval[T]) -> bool:
        """Lexicographic ordering of intervals.
        """
        return (self.start, self.end, self.left_closed, self.right_closed) > (
            other.start,
            other.end,
            other.left_closed,
            other.right_closed,
        )

    @override
    def __eq__(self, other: Interval[T]) -> bool:
        return (self.start, self.end, self.left_closed, self.right_closed) == (
            other.start,
            other.end,
            other.left_closed,
            other.right_closed,
        )
