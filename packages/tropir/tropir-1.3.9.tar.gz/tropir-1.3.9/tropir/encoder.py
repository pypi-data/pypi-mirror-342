import json
class GrammarEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        # Handle frozendict objects
        if hasattr(obj, "keys") and not isinstance(obj, dict):
            return dict(obj)
        return super().default(obj)
