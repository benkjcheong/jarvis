#!/usr/bin/env python3

import subprocess
import sys

def run_unit_tests():
    """Run pytest unit tests"""
    print("Running unit tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_system.py", "-v"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

def run_integration_test():
    """Test the full pipeline with a simple prompt"""
    print("\nRunning integration test...")
    
    try:
        from tests.test_system import test_screenshot_capture, test_element_detection
        from src.ai.gemma import GemmaWorkflowGenerator
        
        # Test workflow generation
        generator = GemmaWorkflowGenerator()
        workflow = generator.generate_workflow("Play cello music on Spotify")
        print(f"Generated workflow: {len(workflow)} steps")
        
        # Test screenshot and element detection
        test_screenshot_capture()
        test_element_detection()
        print(f"Integration test completed.")
        
    except Exception as e:
        print(f"Integration test failed: {e}")

def test_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    
    required = ['torch', 'cv2', 'PIL', 'pytesseract', 'pyautogui', 'transformers']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"✗ {package}")
    
    if missing:
        print(f"\nInstall missing packages: pip install {' '.join(missing)}")
        return False
    return True

if __name__ == "__main__":
    if test_dependencies():
        run_unit_tests()
        run_integration_test()
    else:
        print("Please install missing dependencies first.")