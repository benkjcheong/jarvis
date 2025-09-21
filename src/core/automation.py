import cv2
import numpy as np
from typing import List, Optional
from .types import UIElement, WorkflowStep, ActionType

class LayoutAnalyzer:
    def __init__(self):
        from ..ai.vision import VisualProcessor
        self.visual_processor = VisualProcessor()
    
    def analyze(self, screenshot: np.ndarray) -> List[UIElement]:
        """Extract UI elements using OCR and CNN"""
        raw_elements = self.visual_processor.extract_elements(screenshot)
        
        ui_elements = []
        for elem in raw_elements:
            ui_element = UIElement(
                bounds=elem['bounds'],
                element_type=elem.get('element_type', elem['type']),
                text_content=elem.get('text', ''),
                confidence=elem['confidence'],
                semantic_tags=[]
            )
            ui_elements.append(ui_element)
        
        return ui_elements

class ElementMatcher:
    def find_match(self, description: str, elements: List[UIElement]) -> Optional[UIElement]:
        # Semantic matching between description and UI elements
        best_match = None
        highest_score = 0
        
        for element in elements:
            score = self._calculate_similarity(description, element)
            if score > highest_score:
                highest_score = score
                best_match = element
        
        return best_match if highest_score > 0.7 else None
    
    def _calculate_similarity(self, description: str, element: UIElement) -> float:
        """Calculate similarity between description and UI element"""
        from ..ai.language import SemanticMatcher
        
        matcher = SemanticMatcher()
        return matcher.calculate_similarity(
            description, 
            element.text_content, 
            element.element_type
        )

class ActionExecutor:
    def execute_action(self, step: WorkflowStep, element: UIElement) -> bool:
        x, y, w, h = element.bounds
        center_x, center_y = x + w//2, y + h//2
        
        if step.action_type == ActionType.CLICK:
            return self._click(center_x, center_y)
        elif step.action_type == ActionType.TYPE:
            return self._type_text(step.value)
        elif step.action_type == ActionType.ENTER:
            return self._press_enter()
        
        return False
    
    def _click(self, x: int, y: int) -> bool:
        """Execute mouse click"""
        try:
            import pyautogui
            pyautogui.click(x, y)
            return True
        except Exception:
            return False
    
    def _type_text(self, text: str) -> bool:
        """Type text using keyboard"""
        try:
            import pyautogui
            pyautogui.typewrite(text)
            return True
        except Exception:
            return False
    
    def _press_enter(self) -> bool:
        """Press enter key"""
        try:
            import pyautogui
            pyautogui.press('enter')
            return True
        except Exception:
            return False