import inspect

class AnySentinel:
    def __repr__(self):
        return "<ANY_STATE>"
ANY_STATE = AnySentinel()

import inspect

class AnySentinel:
    def __repr__(self):
        return "<ANY_STATE>"
ANY_STATE = AnySentinel()

def for_state(state_name, *more_names):
    """A decorator to associate methods with specific states for stateful objects.

    This decorator allows you to define multiple methods with the same name,
    each associated with a specific state. When a method is called, the state
    of the object determines which version of the method is executed.

    To use the `for_state` decorator, you can define a class with
    methods decorated with `for_state` and specify the state
    names. Use the reserved `ANY_STATE` to indicate a fallback method

    The object state is obtained from the attribute `_state`.

    Example:
        class MyStatefulObject:
            def __init__(self):
                self._state = "state0"  # Initial state

            @for_state("state1")
            def action(self):
                print("Action for state 1")

            @for_state("state2")
            def action(self):
                print("Action for state 2")

            @for_state(ANY_STATE)
            def action(self):
                print("Action for any state")

        obj = MyStatefulObject()
        obj._state = "state1"
        obj.action()  # Output: Action for state 1

        obj._state = "state2"
        obj.action()  # Output: Action for state 2

        obj._state = "unknown"
        obj.action()  # Output: Action for any state

    Raises:
        AttributeError: If the object does not have a "_state" attribute.
        RuntimeError: If no method is found for the current state.

    """

    def decorator(func):
        # Look for the frame containing the methods defined so far in the class:
        current = inspect.currentframe()
        f = current.f_back
        while f:
            if '__module__' in f.f_locals and '__qualname__' in f.f_locals:
                break
        else:
            raise RuntimeError("No valid frame found for the decorator @for_state.")

        method_name = func.__name__
        if (wrapper := f.f_locals.get(method_name)) is None:
            dispatch_table = {}
            def wrapper(self, *args, **kwargs):
                try:
                    method = dispatch_table[self._state]
                except AttributeError:
                    raise AttributeError(f"Object {self} does not have a '_state' attribute.")
                except KeyError:
                    try:
                        method = dispatch_table[ANY_STATE]
                    except KeyError:
                        raise RuntimeError(f"Method '{method_name}' not found for state '{state_name}'.")
                return method(self, *args, **kwargs)

            wrapper.__for_state__dispatch_table__ = dispatch_table
            wrapper.__name__ = method_name
            wrapper.__doc__ = func.__doc__
            wrapper.__module__ = func.__module__
        else:
            try:
                dispatch_table = wrapper.__for_state__dispatch_table__
            except AttributeError:
                previous_location = ""
                try:
                    previous_location = f" at {func.__code__.co_filename}:{func.__code__.co_firstlineno}"
                except:
                    pass
                raise RuntimeError(f"Method {method_name} previously declared without @for_state decorator{previous_location}.")
        dispatch_table[state_name] = func
        for state in more_names:
            dispatch_table[state] = func
        return wrapper
    return decorator
