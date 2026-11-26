class WorkflowConflict(Exception):
    """A command cannot replace a newer or differently keyed operation."""
