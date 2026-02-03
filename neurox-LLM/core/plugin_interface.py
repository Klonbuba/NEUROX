from abc import ABC, abstractmethod

class NeuroxPlugin(ABC):
    def __init__(self):
        self.name = "Unknown Plugin"
        self.description = "No description provided."
        self.version = "0.0.1"
        self.order = 50 # Default execution order (Lower runs first)

    @abstractmethod
    def execute(self, context: dict) -> dict:
        """
        Execute the plugin logic with the given context.
        Returns a dictionary of updates to the context.
        """
        pass

    def on_load(self):
        """Called when the plugin is loaded."""
        pass
