#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.ai.vision import VisualProcessor
from src.ai.gemma import GemmaWorkflowGenerator
from src.core.engine import DesktopAutomationEngine

def test_screenshot_capture():
    """Test screenshot capture functionality"""
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot_array = np.array(screenshot)
        
        assert screenshot_array.shape[2] == 3, "Screenshot should have 3 color channels"
        assert screenshot_array.dtype == np.uint8, "Screenshot should be uint8"
        print("✓ Screenshot capture working")
        return True
    except Exception as e:
        print(f"✗ Screenshot capture failed: {e}")
        return False

def test_element_detection():
    """Test UI element detection"""
    try:
        processor = VisualProcessor()
        
        # Create a dummy screenshot
        dummy_screenshot = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        elements = processor.extract_elements(dummy_screenshot)
        
        assert isinstance(elements, list), "Should return a list of elements"
        print("✓ Element detection working")
        return True
    except Exception as e:
        print(f"✗ Element detection failed: {e}")
        return False

def test_workflow_generation():
    """Test Gemma workflow generation"""
    try:
        generator = GemmaWorkflowGenerator()
        
        test_prompts = [
            "Play music on Spotify",
            "Open browser and search for Python"
        ]
        
        for prompt in test_prompts:
            workflow = generator.generate_workflow(prompt)
            assert isinstance(workflow, list), "Should return workflow list"
            print(f"✓ Generated workflow for: {prompt} ({len(workflow)} steps)")
        
        return True
    except Exception as e:
        print(f"✗ Workflow generation failed: {e}")
        return False

def test_automation_engine():
    """Test the main automation engine"""
    try:
        engine = DesktopAutomationEngine()
        
        # Test screen capture
        screenshot = engine.capture_screen()
        assert isinstance(screenshot, np.ndarray), "Should return numpy array"
        
        print("✓ Automation engine initialized")
        return True
    except Exception as e:
        print(f"✗ Automation engine failed: {e}")
        return False

if __name__ == "__main__":
    print("Running system tests...")
    
    tests = [
        test_screenshot_capture,
        test_element_detection,
        test_workflow_generation,
        test_automation_engine
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("All tests passed! ✓")
    else:
        print("Some tests failed! ✗")