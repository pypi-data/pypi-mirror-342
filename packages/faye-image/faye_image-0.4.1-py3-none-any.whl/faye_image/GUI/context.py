# Define FyContext class

from collections.abc import MutableMapping
from typing import Any, Dict, Iterator, Optional

class FyContext(MutableMapping):
    """
    A dictionary-like object to store shared variables for the GUI callback.
    Allows attribute access for fixed members and dictionary access for user variables.
    """
    def __init__(self, initial_data: Optional[Dict[str, Any]] = None, **kwargs):
        # Internal storage for user-defined key-value pairs
        self._user_data: Dict[str, Any] = {}
        if initial_data:
            self._user_data.update(initial_data)
        self._user_data.update(kwargs)

        # --- Fixed Members (Example) ---
        # These could store meta-information provided by FyGUI
        # For now, let's keep it simple. Add fixed members as needed.
        # self.window_width: Optional[int] = None
        # self.window_height: Optional[int] = None
        # self.frame_count: int = 0
        # --------------------------------

    # --- Dictionary Interface Implementation ---

    def __setitem__(self, key: str, value: Any) -> None:
        # Prevent overwriting fixed members if they exist
        # if hasattr(self, key) and key not in self._user_data:
        #    raise AttributeError(f"Cannot overwrite fixed context attribute '{key}'")
        self._user_data[key] = value

    def __getitem__(self, key: str) -> Any:
        # Prioritize fixed members if accessed via dict notation? Or keep separate?
        # Let's keep them separate for clarity. Dict access is only for user data.
        if key in self._user_data:
            return self._user_data[key]
        else:
            # If you want attribute access to fall back to dict:
            # if hasattr(self, key):
            #     return getattr(self, key)
            raise KeyError(f"Key '{key}' not found in FyContext user data.")

    def __delitem__(self, key: str) -> None:
        if key in self._user_data:
            del self._user_data[key]
        else:
            raise KeyError(f"Key '{key}' not found in FyContext user data.")

    def __iter__(self) -> Iterator[str]:
        return iter(self._user_data)

    def __len__(self) -> int:
        return len(self._user_data)

    # --- Optional: Attribute Access for User Data (can be risky) ---
    # Uncomment if you want context['key'] and context.key to be interchangeable
    # def __getattr__(self, name: str) -> Any:
    #     try:
    #         # Check fixed attributes first (if any defined)
    #         # return super().__getattribute__(name) # If inheriting from object
    #         return self._user_data[name]
    #     except KeyError:
    #         raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}' and key not in user data")

    # def __setattr__(self, name: str, value: Any) -> None:
    #     # Check if it's a predefined attribute or internal variable
    #     if name.startswith('_') or hasattr(self.__class__, name):
    #          super().__setattr__(name, value)
    #     else:
    #         # Treat as user data
    #         self._user_data[name] = value

    # def __delattr__(self, name: str) -> None:
    #      if name in self._user_data:
    #          del self._user_data[name]
    #      else:
    #          # Handle deletion of fixed attributes if necessary
    #          super().__delattr__(name)


    def __repr__(self) -> str:
        # Combine fixed attrs (if any) and user data for representation
        fixed_attrs = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return f"{type(self).__name__}(user_data={self._user_data}, fixed_attrs={fixed_attrs})"

    def update(self, *args, **kwargs) -> None:
        """Update the context with new key-value pairs, similar to dict.update()."""
        self._user_data.update(*args, **kwargs)

    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from user data, returning default if key not found."""
        return self._user_data.get(key, default)

    def clear(self) -> None:
        """Remove all items from user data."""
        self._user_data.clear()

# Example Usage
if __name__ == '__main__':
    context = FyContext(initial_data={'learning_rate': 0.01}, user_id=123)
    context['batch_size'] = 32

    print(context)
    print(f"Learning Rate: {context['learning_rate']}")
    print(f"User ID: {context.get('user_id')}")
    print(f"Batch Size: {context['batch_size']}")

    context['learning_rate'] = 0.005
    print(f"Updated Learning Rate: {context['learning_rate']}")

    del context['user_id']
    print("After deleting user_id:")
    print(context)

    print("Iterating through context:")
    for key, value in context.items():
        print(f"  {key}: {value}")

    print(f"Length: {len(context)}")
