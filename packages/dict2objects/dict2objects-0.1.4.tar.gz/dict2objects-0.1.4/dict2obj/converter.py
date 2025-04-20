import ast


class Dict2Obj:
    """Convert a dictionary into an object with attribute-style access and provide flattening functionality."""

    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("Input should be a dictionary.")
        for key, value in data.items():
            str_key = str(key)
            if isinstance(value, dict):
                value = Dict2Obj(value)
            elif isinstance(value, list):
                value = [Dict2Obj(v) if isinstance(v, dict) else v for v in value]
            self.__dict__[str_key] = value

    def __getattr__(self, name):
        return None

    def _reverse_key(self, key: str):
        """Try converting stringified keys back to original type."""
        try:
            original = ast.literal_eval(key)
            if isinstance(original, (tuple, int, float)):
                return original
        except (ValueError, SyntaxError):
            pass
        return key

    def to_dict(self):
        """Convert the object back to a dictionary, restoring tuple/int keys if possible."""
        result = {}
        for key, value in self.__dict__.items():
            restored_key = self._reverse_key(key)
            if isinstance(value, Dict2Obj):
                result[restored_key] = value.to_dict()
            elif isinstance(value, list):
                result[restored_key] = [v.to_dict() if isinstance(v, Dict2Obj) else v for v in value]
            else:
                result[restored_key] = value
        return result

    def to_dot_dict(self, parent_key=""):
        """Flatten the dictionary into a dot notation format."""
        dot_dict = {}

        def flatten(obj, parent_key=""):
            if isinstance(obj, Dict2Obj):
                obj = obj.to_dict()
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{parent_key}.{key}" if parent_key else str(key)
                    flatten(value, full_key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    full_key = f"{parent_key}.{i}"
                    flatten(item, full_key)
            else:
                dot_dict[parent_key] = obj

        flatten(self.to_dict(), parent_key)
        return dot_dict
