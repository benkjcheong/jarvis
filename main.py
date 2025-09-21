#!/usr/bin/env python3

from src.core.engine import DesktopAutomationEngine
from src.ai.language import PromptParser
from src.workflows.library import WorkflowLibrary

def main():
    """Main entry point for Jarvis desktop automation"""
    engine = DesktopAutomationEngine()
    parser = PromptParser()
    
    print("Jarvis Desktop Automation System")
    print("Type 'quit' to exit")
    
    while True:
        prompt = input("\nEnter command: ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            break
        
        if not prompt:
            continue
        
        try:
            # Parse the prompt
            parsed = parser.parse(prompt)
            print(f"Parsed: {parsed}")
            
            # Check for pre-defined workflows
            workflow = WorkflowLibrary.get_workflow(prompt)
            if workflow:
                print(f"Found workflow with {len(workflow)} steps")
                # In practice, would execute the workflow
                # success = engine.execute_workflow(workflow)
                print("Workflow execution simulated")
            else:
                print("No matching workflow found")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()