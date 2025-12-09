import uuid
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from pathlib import Path

from .puzzle import AOCPuzzle

"""
Template for puzzle solution implementation
Solutions for https://adventofcode.com/2025/day/8
"""


@dataclass
class Circuit:
    boxes: set[tuple[int, int, int]]
    uid: str = ""

    def __post_init__(self):
        if not self.uid:
            self.uid = str(uuid.uuid4())


@cache
def distance(box1: tuple[int, int, int], box2: tuple[int, int, int]) -> int:
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return ((x1 - x2) ** 2) + ((y1 - y2) ** 2) + ((z1 - z2) ** 2)


class D08Puzzle(AOCPuzzle):
    def __init__(self, input_file: Path):
        # Initialize attributes
        self._boxes: set[tuple[int, int, int]] = set()

        # Go with input file parsing
        super().__init__(input_file)
        self._logger.info(f"Found {len(self._boxes)} boxes")

        # Iterate on all combinations
        comb_count = 0
        self._all_distances: dict[int, set[tuple[tuple[int, int, int], tuple[int, int, int]]]] = defaultdict(set)
        for box1, box2 in combinations(self._boxes, 2):
            comb_count += 1
            d = distance(box1, box2)
            self._all_distances[d].add((box1, box2))
        self._logger.info(f"handled all {comb_count} combinations distances")

    def parse_line(self, index: int, line: str) -> str:
        # Parse boxes positions
        parsed_line = super().parse_line(index, line)
        self._boxes.add(tuple([int(p) for p in parsed_line.split(",", 3)]))  # type: ignore
        return parsed_line

    def build_circuits(self, boxes_sample_max: int | None) -> dict[str, Circuit] | tuple[tuple[int, int, int], tuple[int, int, int]]:
        boxes_sample = 0
        circuits_per_boxes: dict[tuple[int, int, int], str] = {}
        all_circuits: dict[str, Circuit] = {}
        for d in sorted(self._all_distances.keys()):
            if boxes_sample_max and (boxes_sample >= boxes_sample_max):
                return all_circuits
            self._logger.info(f">>> Processing distance {d} boxes")
            for box1, box2 in self._all_distances[d]:
                self._logger.info(f">>>>>> Processing {box1} and {box2} boxes")
                if boxes_sample_max and (boxes_sample >= boxes_sample_max):
                    return all_circuits
                boxes_sample += 1

                # Connect boxes pair to a circuit
                matching_circuits = 0
                for box, otherbox in ((box1, box2), (box2, box1)):
                    if box in self._boxes:
                        # Box is now processed at least once, forget it
                        self._boxes.remove(box)

                    if box in circuits_per_boxes:
                        # Add otherbox to existing circuit
                        circuit = all_circuits[circuits_per_boxes[box]]
                        circuit.boxes.add(otherbox)
                        if otherbox not in circuits_per_boxes:
                            # Just add otherbox to circuit if not in any circuit yet
                            circuits_per_boxes[otherbox] = circuit.uid
                        matching_circuits += 1
                if matching_circuits == 0:
                    # Create new circuit
                    new_circuit = Circuit({box1, box2})
                    all_circuits[new_circuit.uid] = new_circuit
                    circuits_per_boxes[box1] = new_circuit.uid
                    circuits_per_boxes[box2] = new_circuit.uid
                elif matching_circuits > 1:
                    # Merge circuits
                    circuit1 = all_circuits[circuits_per_boxes[box1]]
                    circuit2 = all_circuits[circuits_per_boxes[box2]]
                    circuit1.boxes.update(circuit2.boxes)
                    if circuit1.uid != circuit2.uid:
                        del all_circuits[circuit2.uid]
                    for box in circuit1.boxes:
                        circuits_per_boxes[box] = circuit1.uid

                # If there is only one matching circuit
                if (len(all_circuits) == 1) and (len(self._boxes) == 0):
                    self._logger.info(f"All circuits merged at iteration {boxes_sample}, with boxes {box1} and {box2}!")
                    return (box1, box2)

                # self._logger.info(
                #    f"Found circuits on iteration {boxes_sample}:\n"
                #    + "\n".join(
                #        [f" - key: {key}, size {len(all_circuits[circuit].boxes)}: {all_circuits[circuit]}" for key, circuit in circuits_per_boxes.items()]
                #    )
                # )
        return all_circuits


class D08Step1Puzzle(D08Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate on required shortest distances
        assert some_arg is not None and isinstance(some_arg, int)
        boxes_sample_max = some_arg
        all_circuits = self.build_circuits(boxes_sample_max)
        assert isinstance(all_circuits, dict)

        # Get the 3 largest circuits sizes product
        result = 1
        for s in sorted([len(circuit.boxes) for circuit in all_circuits.values()], reverse=True)[:3]:
            result *= s

        return result


class D08Step2Puzzle(D08Puzzle):
    def solve(self, some_arg: int | str | None = None) -> int:
        # Iterate until getting only one big circuit
        last_boxes = self.build_circuits(None)
        assert isinstance(last_boxes, tuple)

        # Just multiply the coordinates of the two boxes returned
        box1, box2 = last_boxes
        return box1[0] * box2[0]
