from dataclasses import dataclass

class StepTracker:
    def __init__(self, steps: list, on_complete):
        self.steps = {step: False for step in steps}
        self.on_complete = on_complete
        self.competed = False
        self.nextState = ""

    def reset(self):
        self.steps = {step: False for step in self.steps}
        self.competed = False
        self.nextState = ""
    
    def set_state(self, state: str):
        self.nextState = state

    def complete(self, step: str):
        if step in self.steps:
            self.steps[step] = True
            print(f"Step completed: {step}")
            if all(self.steps.values()):
                print("all completed")
                self.on_complete(self.nextState)
                self.competed = True
    
    def is_completed(self):
        return self.competed
    
    def pending_steps(self) -> list[str]:
        return [step for step, done in self.steps.items() if not done]
    
@dataclass
class Trackers:
    grained: StepTracker
    grouped: StepTracker
    def reset(self):
        self.grained.reset()
        self.grouped.reset()
    def set_state(self, state: str):
        self.grained.set_state(state)
        self.grouped.set_state(state)