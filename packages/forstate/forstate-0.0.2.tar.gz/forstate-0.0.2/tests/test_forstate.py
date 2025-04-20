import unittest
from forstate import for_state, ANY_STATE

class MyStatefulObject:
    def __init__(self):
        self._state = "state0"  # Initial state

    @for_state("state1", "state4")
    def action(self):
        return "Action for state 1 or 4"

    @for_state("state2")
    def action_state2(self):
        return "Action for state 2"

    @for_state(ANY_STATE)
    def action_any(self):
        return "Action for any state"

    @for_state("state3")
    def another_action(self):
        return "Action for state 3"


class TestForStateDecorator(unittest.TestCase):
    def setUp(self):
        self.obj = MyStatefulObject()

    def test_action_state1(self):
        self.obj._state = "state1"
        result = self.obj.action()
        self.assertEqual(result, "Action for state 1 or 4")

    def test_action_state4(self):
        self.obj._state = "state4"
        result = self.obj.action()
        self.assertEqual(result, "Action for state 1 or 4")

    def test_action_state2(self):
        self.obj._state = "state2"
        result = self.obj.action_state2()
        self.assertEqual(result, "Action for state 2")

    def test_action_any_state(self):
        self.obj._state = "unknown"
        result = self.obj.action_any()
        self.assertEqual(result, "Action for any state")

    def test_no_method_for_current_state(self):
        self.obj._state = "non_existent_state"
        with self.assertRaises(RuntimeError):
            self.obj.another_action()  # This will fail since there's no method for 'non_existent_state'

    def test_no_state_attribute(self):
        del self.obj._state
        with self.assertRaises(AttributeError):
            self.obj.action_any()

    def test_mixed_for_and_without_state(self):
        with self.assertRaises(RuntimeError):
            class C:
                def foo(self):
                    return 1

                @for_state("state1")
                def foo(self):
                    return 2

if __name__ == '__main__':
    unittest.main()
