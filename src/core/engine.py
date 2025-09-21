import numpy as np
import time
from typing import List
from .types import WorkflowStep, ActionType
from .automation import LayoutAnalyzer, ElementMatcher, ActionExecutor
from ..ai.gemma import GemmaWorkflowGenerator

class DesktopAutomationEngine:
    def __init__(self):
        self.layout_analyzer = LayoutAnalyzer()
        self.element_matcher = ElementMatcher()
        self.action_executor = ActionExecutor()
        self.workflow_generator = GemmaWorkflowGenerator()
    
    def execute_prompt(self, prompt: str) -> bool:
        """Generate workflow from prompt and execute it"""
        print(f"Generating workflow for: {prompt}")
        workflow = self.workflow_generator.generate_workflow(prompt)
        
        if not workflow:
            print("Failed to generate workflow")
            return False
            
        print(f"Generated {len(workflow)} steps")
        return self.execute_workflow(workflow)
    
    def capture_screen(self) -> np.ndarray:
        import pyautogui
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)
    
    def execute_workflow(self, workflow: List[WorkflowStep]) -> bool:
        """Execute workflow steps using OCR and CNN"""
        for i, step in enumerate(workflow):
            print(f"Step {i+1}: {step.action_type.value} - {step.target_description}")
            
            if step.action_type == ActionType.WAIT:
                time.sleep(step.timeout)
                continue
            
            # Capture screen and analyze UI elements
            screenshot = self.capture_screen()
            ui_elements = self.layout_analyzer.analyze(screenshot)
            
            # Find matching element
            target_element = self.element_matcher.find_match(step.target_description, ui_elements)
            
            if not target_element:
                print(f"Could not find element: {step.target_description}")
                return False
            
            # Execute action
            success = self.action_executor.execute_action(step, target_element)
            if not success:
                print(f"Failed to execute action: {step.action_type.value}")
                return False
            
            time.sleep(0.5)  # Brief pause between actions
        
        print("Workflow completed successfully")
        return True