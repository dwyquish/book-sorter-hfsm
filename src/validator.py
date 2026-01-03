from typing import Dict, Any


class RuleValidator:
    """
    Validates DFA rule definitions before execution.
    """

    @staticmethod
    def validate(rules: Dict[str, Any]) -> None:
        if not rules:
            raise ValueError("Rules cannot be empty")

        if "start_state" not in rules:
            raise ValueError("Rules must define a 'start_state'")

        if "states" not in rules:
            raise ValueError("Rules must define 'states'")

        states = rules["states"]
        start_state = rules["start_state"]

        if start_state not in states:
            raise ValueError("start_state must exist in states")

        for state_name, state_def in states.items():
            if "transitions" in state_def:
                if not isinstance(state_def["transitions"], dict):
                    raise ValueError(f"Transitions for state '{state_name}' must be a dictionary")

                for symbol, target in state_def["transitions"].items():
                    if target not in states:
                        raise ValueError(
                            f"Transition from '{state_name}' "
                            f"on symbol '{symbol}' points to undefined state '{target}'"
                        )
