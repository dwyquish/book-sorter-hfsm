from typing import Dict, Any


class RuleValidator:

    @staticmethod
    def validate(rules: Dict[str, Any]) -> None:
        if not rules:
            raise ValueError("Rules cannot be empty")

        if "start_state" not in rules or "states" not in rules:
            raise ValueError("Rules must define 'start_state' and 'states'")

        start = rules["start_state"]
        if start not in rules["states"]:
            raise ValueError("start_state must exist in top-level states")

        # Recursively validate HFSM structure
        RuleValidator._validate_state(
            rules["states"][start],
            path=[start]
        )

    @staticmethod
    def _validate_state(state: Dict[str, Any], path):
        # Validate initial state
        if "states" in state:
            if "initial" not in state:
                raise ValueError(
                    f"State {'/'.join(path)} must define an initial substate"
                )

            initial = state["initial"]
            if initial not in state["states"]:
                raise ValueError(
                    f"Initial state '{initial}' not found in {'/'.join(path)}"
                )

            # Validate transitions
            for sub_name, sub_state in state["states"].items():
                RuleValidator._validate_transitions(
                    sub_state,
                    state["states"],
                    path + [sub_name]
                )

                # Recursive descent
                RuleValidator._validate_state(
                    sub_state,
                    path + [sub_name]
                )

    @staticmethod
    def _validate_transitions(state, siblings, path):
        if "transitions" not in state:
            return

        if not isinstance(state["transitions"], dict):
            raise ValueError(
                f"Transitions in {'/'.join(path)} must be a dictionary"
            )

        for symbol, target in state["transitions"].items():
            if target not in siblings:
                raise ValueError(
                    f"Transition on '{symbol}' in {'/'.join(path)} "
                    f"points to undefined sibling state '{target}'"
                )
