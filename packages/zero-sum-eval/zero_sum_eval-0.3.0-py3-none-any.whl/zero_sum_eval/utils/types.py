# Copyright (c) Meta Platforms, Inc. and affiliates.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Iterable, Optional
from dspy import Prediction, Example

@dataclass
class ActionConfig:
    name: str
    module_path: Optional[str] = None
    optimize: Optional[bool] = False
    dataset: Optional[str] = None
    dataset_args: Optional[dict] = None
    optimizer: Optional[str] = None
    optimizer_args: Optional[dict] = None
    metric: Optional[str] = None

@dataclass
class Move:
    value: str
    time: float
    trace: Optional[Prediction] = None

@dataclass
class Action:
    """
    Action class for a player to take in a game

    Args:
        name: The name of the action
        player_key: The key of the player taking the action
        inputs: The inputs to the function implementing the action
    """
    name: str
    player_key: str
    inputs: Dict


class Dataset(ABC):
    def __init__(self, output_key: str) -> None:
        # the key of the output field for each example
        self.output_key = output_key

    @abstractmethod
    def get_dataset(self) -> Iterable[Example]:
        pass

class InvalidMoveError(Exception):
    pass

class MoveParseError(Exception):
    pass
