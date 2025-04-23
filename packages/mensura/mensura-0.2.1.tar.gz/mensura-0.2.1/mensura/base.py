from typing import DefaultDict
from collections import defaultdict, deque

from mensura.conversions import CONVERSIONS, ABBREVIATIONS, Conversion
from mensura.exceptions import ConversionException, UnitNotFoundException


class Converter:
    """Converter class for units. Handles the graph building
    logic as well as the algorithm to find shortest path between
    units.
    """

    def __init__(self) -> None:
        self.graph: DefaultDict[str, dict[str, float]] = defaultdict(dict)
        self._register_conversions()

    def _register_conversions(self):
        """Register defined conversions"""
        for conversion in CONVERSIONS:
            self.add_conversion(conversion)

    def _resolve_unit(self, unit: str) -> str:
        unit = unit.lower()
        return ABBREVIATIONS.get(unit, unit)

    def add_conversion(self, conversion: Conversion):
        """Add bidirectional conversion to graph.

        Parameters
        ----------
        conversion : Conversion
            A conversion object that holds (from_unit, to_unit, conversion_factor)
        """
        src_unit = self._resolve_unit(conversion.src_unit)
        dest_unit = self._resolve_unit(conversion.dest_unit)

        self.graph[src_unit][dest_unit] = conversion.factor
        self.graph[dest_unit][src_unit] = 1 / conversion.factor

    def convert(
        self,
        value: str | int | float,
        from_unit: str,
        to_unit: str,
    ) -> int | float:
        """Apply BFS algorithm to convert units using shortest path.

        Parameters
        ----------
        value : str | int | float
            The value of the quantity to be converted.
        from_unit : str
            The source unit of the conversion.
        to_unit : str
            The destination unit of the conversion.

        Returns
        -------
        value in destination unit : int | float
        """
        if isinstance(value, str):
            value = float(value)

        from_unit = self._resolve_unit(from_unit)
        to_unit = self._resolve_unit(to_unit)

        if from_unit not in self.graph or to_unit not in self.graph:
            raise UnitNotFoundException(
                f"Conversion from {from_unit} to {to_unit} not possible..."
            )

        queue = deque([(1.0, from_unit)])
        visited: set[str] = set()

        while queue:
            current_factor, current_unit = queue.popleft()

            if current_unit == to_unit:
                return value * current_factor

            visited.add(current_unit)

            for neighbour, factor in self.graph[current_unit].items():
                if neighbour not in visited:
                    queue.append((current_factor * factor, neighbour))

        raise ConversionException(f"Conversion from {from_unit} to {to_unit} failed.")
