import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import cv2
import numpy as np
from typing import List, Tuple, Dict

class LayoutCNN(nn.Module):
    """CNN model for understanding UI layout and detecting elements"""
    
    def __init__(self, num_classes=10):  # button, textfield, menu, etc.
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((7, 7))
        )
        self.classifier = nn.Linear(256 * 7 * 7, num_classes)
        
    def forward(self, x):
        features = self.backbone(x)
        features = features.view(features.size(0), -1)
        return self.classifier(features)

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

class VisualProcessor:
    """Process screenshots to extract UI elements"""
    
    def __init__(self):
        self.layout_model = LayoutCNN()
        # In practice, load pre-trained weights
        
    def extract_elements(self, screenshot: np.ndarray) -> List[Dict]:
        """Extract UI elements from screenshot"""
        # Preprocess image
        processed = self._preprocess_image(screenshot)
        
        # Detect text regions using OCR
        text_regions = self._extract_text_regions(screenshot)
        
        # Detect clickable elements using computer vision
        clickable_regions = self._detect_clickable_elements(screenshot)
        
        # Combine and classify all regions
        all_elements = self._combine_and_classify(text_regions, clickable_regions, screenshot)
        
        return all_elements
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Prepare image for model input"""
        resized = cv2.resize(image, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        return normalized
    
    def _extract_text_regions(self, image: np.ndarray) -> List[Dict]:
        """Use OCR to find text regions"""
        # Placeholder - would use Tesseract/EasyOCR
        return []
    
    def _detect_clickable_elements(self, image: np.ndarray) -> List[Dict]:
        """Detect buttons, links, and other clickable elements"""
        # Use computer vision techniques
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect rectangular regions (potential buttons)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        elements = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 50 and h > 20:  # Filter small regions
                elements.append({
                    'bounds': (x, y, w, h),
                    'type': 'clickable',
                    'confidence': 0.8
                })
        
        return elements
    
    def _combine_and_classify(self, text_regions: List[Dict], 
                            clickable_regions: List[Dict], 
                            screenshot: np.ndarray) -> List[Dict]:
        """Combine different detection results and classify elements"""
        all_elements = text_regions + clickable_regions
        
        # Add semantic classification using the CNN model
        for element in all_elements:
            x, y, w, h = element['bounds']
            roi = screenshot[y:y+h, x:x+w]
            
            # Classify the region
            element_type = self._classify_element(roi)
            element['element_type'] = element_type
        
        return all_elements
    
    def _classify_element(self, roi: np.ndarray) -> str:
        """Classify UI element type using CNN"""
        # Placeholder - would use trained model
        return "button"  # Default classification