import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import Dict

class SemanticMatcher:
    """Matches semantic descriptions to UI elements using embeddings"""
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    
    def encode_text(self, text: str) -> np.ndarray:
        """Convert text to embedding vector"""
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy().flatten()
    
    def calculate_similarity(self, description: str, element_text: str, element_type: str) -> float:
        """Calculate semantic similarity between description and UI element"""
        desc_embedding = self.encode_text(description)
        
        # Combine element text and type for better matching
        element_context = f"{element_type} {element_text}".strip()
        element_embedding = self.encode_text(element_context)
        
        # Cosine similarity
        similarity = np.dot(desc_embedding, element_embedding) / (
            np.linalg.norm(desc_embedding) * np.linalg.norm(element_embedding)
        )
        return float(similarity)

class PromptParser:
    """Parse natural language prompts into structured workflows"""
    
    def __init__(self):
        self.semantic_matcher = SemanticMatcher()
        self.action_keywords = {
            'click': ['click', 'tap', 'press', 'select'],
            'type': ['type', 'enter', 'input', 'write'],
            'search': ['search', 'find', 'look for'],
            'open': ['open', 'launch', 'start']
        }
    
    def parse(self, prompt: str) -> Dict:
        """Extract intent, target app, and actions from prompt"""
        prompt_lower = prompt.lower()
        
        # Extract target application
        app_keywords = ['spotify', 'chrome', 'safari', 'mail', 'finder', 'calculator']
        target_app = None
        for app in app_keywords:
            if app in prompt_lower:
                target_app = app
                break
        
        # Extract main action
        main_action = None
        for action, keywords in self.action_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                main_action = action
                break
        
        # Extract search query or content
        content = self._extract_content(prompt)
        
        return {
            'target_app': target_app,
            'main_action': main_action,
            'content': content,
            'original_prompt': prompt
        }
    
    def _extract_content(self, prompt: str) -> str:
        """Extract the main content/query from the prompt"""
        # Simple extraction - in practice would use NER
        words = prompt.split()
        
        # Look for quoted content first
        if '"' in prompt:
            start = prompt.find('"')
            end = prompt.find('"', start + 1)
            if end > start:
                return prompt[start+1:end]
        
        # Extract content after common prepositions
        prepositions = ['for', 'about', 'on']
        for prep in prepositions:
            if prep in prompt.lower():
                idx = prompt.lower().find(prep)
                remaining = prompt[idx + len(prep):].strip()
                return remaining if remaining else ""
        
        return ""