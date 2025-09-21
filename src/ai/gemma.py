import requests
import json
from typing import List
from ..core.types import WorkflowStep, ActionType

class GemmaWorkflowGenerator:
    """Uses local Ollama Gemma model to generate workflows from natural language prompts"""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        
    def generate_workflow(self, prompt: str) -> List[WorkflowStep]:
        """Generate structured workflow from user prompt"""
        system_prompt = """You are a desktop automation assistant. Convert user requests into JSON workflows for UI automation.

Rules:
- Use ONLY these action_types: "click", "type", "enter", "wait"
- target_description must describe visible UI elements (buttons, text fields, icons)
- For "type" actions, include "value" field with text to type
- For "wait" actions, include "timeout" field (1-5 seconds)
- Be specific about UI elements ("search button", "username field", etc.)
- Return ONLY valid JSON array, no other text

Example:
User: "Open Spotify and play music"
[
  {"action_type": "click", "target_description": "Spotify"},
  {"action_type": "wait", "timeout": 2},
  {"action_type": "click", "target_description": "search"},
  {"action_type": "type", "value": "music"},
  {"action_type": "enter"},
  {"action_type": "click", "target_description": "play"}
]

User request:"""

        full_prompt = f"{system_prompt} {prompt}\n\nJSON:"
        
        response = self._call_ollama(full_prompt)
        workflow_json = self._extract_json(response)
        
        return self._parse_workflow(workflow_json)
    
    def _call_ollama(self, prompt: str) -> str:
        """Call local Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "gemma2:2b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 200
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                print(f"Ollama API error: {response.status_code}")
                return ""
        except Exception as e:
            print(f"Failed to connect to Ollama: {e}")
            return ""
    
    def _extract_json(self, response: str) -> str:
        """Extract JSON from model response"""
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end != 0:
            return response[start:end]
        return "[]"
    
    def _parse_workflow(self, workflow_json: str) -> List[WorkflowStep]:
        """Parse JSON workflow into WorkflowStep objects"""
        try:
            steps_data = json.loads(workflow_json)
            steps = []
            
            for step_data in steps_data:
                action_type = ActionType(step_data['action_type'])
                step = WorkflowStep(
                    action_type=action_type,
                    target_description=step_data['target_description'],
                    value=step_data.get('value'),
                    timeout=step_data.get('timeout', 5)
                )
                steps.append(step)
            
            return steps
        except (json.JSONDecodeError, KeyError, ValueError):
            return []