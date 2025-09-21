#!/usr/bin/env python3

from src.core.engine import DesktopAutomationEngine

def main():
    """Main entry point for Jarvis desktop automation"""
    print("Jarvis Desktop Automation System")
    print("Uses Gemma model to generate workflows from natural language")
    print("Type 'quit' to exit")
    
    engine = DesktopAutomationEngine()
    
    while True:
        prompt = input("\nEnter command: ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            break
        
        if not prompt:
            continue
        
        try:
            # Generate and execute workflow using Gemma
            success = engine.execute_prompt(prompt)
            
            if success:
                print("✓ Command executed successfully")
            else:
                print("✗ Command execution failed")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()