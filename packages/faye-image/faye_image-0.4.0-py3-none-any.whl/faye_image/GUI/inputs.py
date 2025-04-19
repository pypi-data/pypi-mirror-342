# Define input types and decorator
import inspect
from typing import Any, Optional, List, Tuple, Type, Dict, Callable
import dataclasses
from .exceptions import ValidationError

__all__ = [
    'FyInputType',
    'FyINT',
    'FyFLOAT',
    'FySTR',
    'FyBOOL',
    'FyCHOICE',
    'FyPATH',
    'FyIMAGE',
]

# Base class for all Fy input types (optional, for type hinting)
class FyInputType:
    def __init__(self, default: Any):
        self.default = default

    def validate(self, value: Any) -> Any:
        """Validate the input value. Raise ValidationError if invalid."""
        return value # Default implementation: no validation

# --- Concrete Input Types ---

@dataclasses.dataclass
class FyINT(FyInputType):
    min_val: Optional[int] = None
    max_val: Optional[int] = None
    default: int = 0
    step: int = 1

    def __post_init__(self):
        # Ensure default is within range if specified
        self.default = self.validate(self.default)

    def validate(self, value: Any) -> int:
        """Validate integer input, checking type and range."""
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                 raise ValidationError(f"Value must be an integer, got {type(value).__name__}")
        if self.min_val is not None and value < self.min_val:
            raise ValidationError(f"Value {value} is less than minimum {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValidationError(f"Value {value} is greater than maximum {self.max_val}")
        return value

@dataclasses.dataclass
class FyFLOAT(FyInputType):
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    default: float = 0.0
    step: float = 0.01 # Smaller default step for floats

    def __post_init__(self):
        # Ensure default is within range if specified
        self.default = self.validate(self.default)

    def validate(self, value: Any) -> float:
        """Validate float input, checking type and range."""
        if not isinstance(value, (float, int)): # Allow ints to be treated as floats
             try:
                 value = float(value)
             except (ValueError, TypeError):
                 raise ValidationError(f"Value must be a float or integer, got {type(value).__name__}")
        value = float(value) # Ensure it's a float
        if self.min_val is not None and value < self.min_val:
            raise ValidationError(f"Value {value} is less than minimum {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValidationError(f"Value {value} is greater than maximum {self.max_val}")
        return value

@dataclasses.dataclass
class FySTR(FyInputType):
    default: str = ""

    def validate(self, value: Any) -> str:
        """Validate string input, checking type."""
        if not isinstance(value, str):
             # Attempt conversion for common types, raise otherwise
             try:
                 value = str(value)
             except Exception:
                 raise ValidationError(f"Value must be a string, got {type(value).__name__}")
        return value

@dataclasses.dataclass
class FyBOOL(FyInputType):
    default: bool = False

    def validate(self, value: Any) -> bool:
        """Validate boolean input, checking type."""
        if not isinstance(value, bool):
            # Basic truthiness check might be too lenient, require strict bool
            raise ValidationError(f"Value must be a boolean (True/False), got {type(value).__name__}")
        return value

@dataclasses.dataclass
class FyCHOICE(FyInputType):
    choices: List[str] = dataclasses.field(default_factory=list)
    default: Optional[str] = None # Default must be one of the choices

    def __post_init__(self):
        if not self.choices:
            raise ValueError("FyCHOICE must have at least one choice.")
        if self.default is None:
            self.default = self.choices[0] # Default to the first choice if not specified
        elif self.default not in self.choices:
            raise ValueError(f"Default value '{self.default}' is not in the available choices: {self.choices}")
        self.default = self.validate(self.default)


    def validate(self, value: Any) -> str:
        """Validate choice input, checking if it's in the allowed list."""
        if not isinstance(value, str):
            raise ValidationError(f"Choice value must be a string, got {type(value).__name__}")
        if value not in self.choices:
            raise ValidationError(f"Value '{value}' is not a valid choice. Available choices: {self.choices}")
        return value

@dataclasses.dataclass
class FyPATH(FyInputType):
    default: str = ""
    must_exist: bool = False # Option to require the path to exist
    is_dir: Optional[bool] = None # None: either file or dir; True: must be dir; False: must be file

    def __post_init__(self):
        # Basic validation of default path if needed
        try:
            self.validate(self.default)
        except ValidationError as e:
            # Allow invalid default path initially, user needs to select one
            print(f"Warning: Default path '{self.default}' validation failed: {e}")
            pass


    def validate(self, value: Any) -> str:
        """Validate path input."""
        import os
        if not isinstance(value, str):
            raise ValidationError(f"Path value must be a string, got {type(value).__name__}")
        if not value: # Empty path is often invalid unless explicitly allowed
             if self.must_exist:
                 raise ValidationError("Path cannot be empty.")
             else:
                 return "" # Allow empty path if existence not required

        # Expand user and vars for robustness
        path = os.path.expanduser(os.path.expandvars(value))

        if self.must_exist and not os.path.exists(path):
            raise ValidationError(f"Path does not exist: {path}")

        if os.path.exists(path): # Only check type if it exists
            if self.is_dir is True and not os.path.isdir(path):
                raise ValidationError(f"Path must be a directory: {path}")
            if self.is_dir is False and not os.path.isfile(path):
                raise ValidationError(f"Path must be a file: {path}")

        return path # Return the original or validated path string

@dataclasses.dataclass
class FyIMAGE(FyPATH):
    # Inherits from FyPATH, adding image-specific validation/handling
    default: str = ""
    must_exist: bool = True # Images usually need to exist
    is_dir: bool = False # Images must be files

    def __post_init__(self):
        # Call parent's post_init first
        super().__post_init__()
        # Additional image-specific validation for default if needed
        # (e.g., check file extension) - Pillow will handle load errors later

    def validate(self, value: Any) -> str:
        """Validate image path input."""
        # First, perform standard path validation
        path = super().validate(value)

        # Add basic image file checks (e.g., extension) - more robust check happens during loading
        if path and os.path.exists(path) and os.path.isfile(path):
            # Simple extension check (can be improved)
            allowed_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'}
            import os
            ext = os.path.splitext(path)[1].lower()
            if ext not in allowed_extensions:
                 print(f"Warning: File '{path}' might not be a supported image format (extension '{ext}' not recognized).")
                 # Don't raise ValidationError here, allow Pillow to try loading it

        return path


# --- Decorator ---

_input_registry: Dict[Type, Dict[str, FyInputType]] = {}

def FyINPUT(cls: Type) -> Type:
    """
    Decorator to register a class as an input definition.
    It inspects class attributes to find FyInputType instances.
    """
    if not inspect.isclass(cls):
        raise TypeError("@FyINPUT can only decorate classes.")

    input_params: Dict[str, FyInputType] = {}
    annotations = getattr(cls, '__annotations__', {})

    # Iterate over class attributes AND annotations to find FyInputType instances
    potential_attrs = {**annotations, **cls.__dict__}

    for attr_name, attr_value in potential_attrs.items():
        if isinstance(attr_value, FyInputType):
            input_params[attr_name] = attr_value
        # Handle cases where type hint is FyInputType but value is assigned later (less common)
        elif attr_name in annotations and isinstance(annotations[attr_name], type) and issubclass(annotations[attr_name], FyInputType):
             if hasattr(cls, attr_name):
                 instance = getattr(cls, attr_name)
                 if isinstance(instance, FyInputType):
                     input_params[attr_name] = instance


    if not input_params:
        print(f"Warning: Class {cls.__name__} decorated with @FyINPUT has no FyInputType attributes.")

    # Store the collected input parameters associated with the class
    _input_registry[cls] = input_params

    # Optionally, convert the class to a dataclass automatically if not already one?
    # Or just return the original class after registration.
    # Let's keep it simple and just register.
    # We will create an instance of this class later to hold the *values*.

    # Add a helper method to get default values
    def get_defaults(self) -> Dict[str, Any]:
        defaults = {}
        registered_params = _input_registry.get(self.__class__, {})
        for name, fy_input in registered_params.items():
            defaults[name] = fy_input.default
        return defaults

    # Add a helper method to get FyInputType instances
    def get_input_definitions(self) -> Dict[str, FyInputType]:
         return _input_registry.get(self.__class__, {})

    # Add a helper method to validate all fields
    def validate_all(self, current_values: Dict[str, Any]) -> Dict[str, Any]:
        validated_values = {}
        definitions = self.get_input_definitions()
        for name, value in current_values.items():
            if name in definitions:
                try:
                    validated_values[name] = definitions[name].validate(value)
                except ValidationError as e:
                    # Re-raise with attribute name context
                    raise ValidationError(f"Error in field '{name}': {e}") from e
            else:
                # Include values not defined by FyInputType (e.g., methods)
                validated_values[name] = value
        return validated_values


    # Inject helper methods into the decorated class
    cls.get_defaults = get_defaults
    cls.get_input_definitions = get_input_definitions
    # cls.validate_all = validate_all # Maybe instance method is better

    # Create a simple instance class to hold runtime values
    # This avoids modifying the user's original class definition directly
    # and provides a clear separation between definition and state.
    @dataclasses.dataclass
    class InputState:
        pass # We will add fields dynamically in FyGUI based on the decorated class

    # Store a reference to the original definition class
    # setattr(InputState, '_definition_cls', cls) # Not ideal

    # Return the original class, registration is the main goal
    return cls

def get_registered_inputs(cls: Type) -> Dict[str, FyInputType]:
    """Retrieve the registered input definitions for a class decorated with @FyINPUT."""
    if cls not in _input_registry:
        raise TypeError(f"Class {cls.__name__} is not registered with @FyINPUT.")
    return _input_registry[cls]

# Example Usage (for testing)
if __name__ == '__main__':
    @FyINPUT
    class MyInputExample:
        attr1 = FyINT(0, 100, default=1, step=2)
        attr2 = FyFLOAT(0.0, 1.0, default=0.5, step=0.1)
        attr3 = FySTR(default='Hello, World!')
        attr4 = FyBOOL(default=True)
        attr5 = FyCHOICE(['A', 'B', 'C'], default='A')
        attr6 = FyPATH(default='./test.png', must_exist=False)
        attr7 = FyIMAGE(default='./test.png', must_exist=False) # Assuming test.png might not exist initially
        # attr_invalid = FyCHOICE([], default='X') # Example of invalid definition

    print(f"Registered inputs for {MyInputExample.__name__}:")
    registered = get_registered_inputs(MyInputExample)
    for name, definition in registered.items():
        print(f"  {name}: {definition}")

    # Test validation
    test_int = registered['attr1']
    print(f"Validating int 50: {test_int.validate(50)}")
    try:
        test_int.validate(101)
    except ValidationError as e:
        print(f"Validation failed as expected: {e}")
    try:
        test_int.validate("abc")
    except ValidationError as e:
        print(f"Validation failed as expected: {e}")

    test_choice = registered['attr5']
    print(f"Validating choice 'B': {test_choice.validate('B')}")
    try:
        test_choice.validate('D')
    except ValidationError as e:
        print(f"Validation failed as expected: {e}")

    # Create an instance to get defaults
    # Note: The decorator doesn't modify the class structure for instantiation directly
    # We'll handle instance creation and value storage in FyGUI
    # But we can test the injected helper method if we create a dummy instance
    class TempInstance(MyInputExample): pass
    instance = TempInstance()
    print(f"Default values: {instance.get_defaults()}")
    print(f"Input definitions from instance: {instance.get_input_definitions()}")
