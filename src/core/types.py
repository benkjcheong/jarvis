from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum

class ActionType(Enum):
    CLICK = "click"
    TYPE = "type"
    ENTER = "enter"
    WAIT = "wait"
    SCROLL = "scroll"

@dataclass
class UIElement:
    bounds: Tuple[int, int, int, int]  # x, y, width, height
    element_type: str  # button, textfield, menu, etc.
    text_content: str
    confidence: float
    semantic_tags: List[str]

@dataclass
class WorkflowStep:
    action_type: ActionType
    target_description: str
    value: Optional[str] = None
    coordinates: Optional[Tuple[int, int]] = None
    timeout: int = 5