from ..core.types import WorkflowStep, ActionType

# Example workflows for common tasks

SPOTIFY_PLAY_MUSIC = [
    WorkflowStep(ActionType.CLICK, "Spotify app icon"),
    WorkflowStep(ActionType.WAIT, "app to load", timeout=3),
    WorkflowStep(ActionType.CLICK, "search bar"),
    WorkflowStep(ActionType.TYPE, "search input", value="cello music"),
    WorkflowStep(ActionType.ENTER, "submit search"),
    WorkflowStep(ActionType.CLICK, "first search result play button")
]

OPEN_BROWSER_SEARCH = [
    WorkflowStep(ActionType.CLICK, "browser icon"),
    WorkflowStep(ActionType.WAIT, "browser to load", timeout=2),
    WorkflowStep(ActionType.CLICK, "address bar"),
    WorkflowStep(ActionType.TYPE, "search query", value="python tutorials"),
    WorkflowStep(ActionType.ENTER, "navigate")
]

SEND_EMAIL = [
    WorkflowStep(ActionType.CLICK, "email app"),
    WorkflowStep(ActionType.CLICK, "compose button"),
    WorkflowStep(ActionType.CLICK, "to field"),
    WorkflowStep(ActionType.TYPE, "recipient", value="example@email.com"),
    WorkflowStep(ActionType.CLICK, "subject field"),
    WorkflowStep(ActionType.TYPE, "subject", value="Meeting reminder"),
    WorkflowStep(ActionType.CLICK, "message body"),
    WorkflowStep(ActionType.TYPE, "message", value="Don't forget our meeting at 3pm"),
    WorkflowStep(ActionType.CLICK, "send button")
]

class WorkflowLibrary:
    """Pre-defined workflows for common tasks"""
    
    workflows = {
        "play music on spotify": SPOTIFY_PLAY_MUSIC,
        "search web": OPEN_BROWSER_SEARCH,
        "send email": SEND_EMAIL
    }
    
    @classmethod
    def get_workflow(cls, task_description: str) -> list:
        # Simple keyword matching for now
        for key, workflow in cls.workflows.items():
            if key in task_description.lower():
                return workflow
        return []
    
    @classmethod
    def customize_workflow(cls, workflow: list, parameters: dict) -> list:
        """Replace placeholders in workflow with actual values"""
        customized = []
        for step in workflow:
            new_step = WorkflowStep(
                action_type=step.action_type,
                target_description=step.target_description,
                value=parameters.get(step.value, step.value) if step.value else None,
                timeout=step.timeout
            )
            customized.append(new_step)
        return customized