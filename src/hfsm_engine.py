import re

class HFSMEngine:

    def __init__(self, rules):
        if not rules:
            raise ValueError("Rules cannot be empty")
        if "start_state" not in rules or "states" not in rules:
            raise ValueError("Rules must contain 'start_state' and 'states'")
        
        self.rules = rules
        self.start_state = rules["start_state"]
        self.root = rules["states"][self.start_state]

    def tokenize(self, text):
        """Convert text into lowercase words, remove non-alphanumeric characters."""
        if not text:
            return []
        clean = re.sub(r'[^a-z0-9\s]', '', str(text).lower())
        return clean.split()

    def classify(self, text):
        # ------------------------------
        # Run HFSM classification on a title.
        # Implements maximal acceptance:
        # Once a stable accept state is reached, remaining tokens do not invalidate it.
        # ------------------------------
        tokens = self.tokenize(text)
        state_stack = []  # Stack of active states
        trace = []

        # Start at root
        current = self.root
        state_stack.append(("root", current))

        # Enter initial substate recursively
        current, path = self._enter_initial(current, "root", state_stack)
        trace.extend(path)

        for token in tokens:
            next_state = self._try_transition(current, token, state_stack, trace)

            if next_state:
                current = next_state
            else:
                # MAXIMAL ACCEPTANCE: stop if current state is accepting
                if current.get("type") == "accept":
                    trace.append(f"(Stopped at accepting state '{current.get('category')}')")
                    break
                # Try parent states
                parent = self._find_parent_accepting_state(state_stack)
                if parent:
                    current = parent
                    state_stack.append(("fallback", parent))
                else:
                    # No transition, no parent, continue to next token (ignore)
                    trace.append(f"(No transition for '{token}', staying in '{current.get('category', 'Unknown')}')")
                    pass

        # Determine final category
        final_category = self._find_final_accepting_category(state_stack)
        confidence = 1.0 if final_category != "Unknown / Review" else 0.0

        return {
            "category": final_category,
            "trace": " -> ".join(trace),
            "confidence": confidence
        }

    # -----------------------------
    # Helper Methods
    # -----------------------------

    def _enter_initial(self, state, name, stack):
        """
        Recursively enter initial states to reach the deepest starting state.
        """
        path_trace = [name]
        while "initial" in state and "states" in state:
            init_name = state["initial"]
            if init_name not in state["states"]:
                raise ValueError(f"Initial state '{init_name}' not found in '{name}'")
            state = state["states"][init_name]
            stack.append((init_name, state))
            path_trace.append(init_name)
            name = init_name
        return state, path_trace

    def _try_transition(self, current, token, stack, trace):
        # ------------------------------
        # Try to find a transition from current state or parent states.
        # Returns the next state or None.
        # ------------------------------
        # Current state transitions
        if "transitions" in current and token in current["transitions"]:
            next_name = current["transitions"][token]

            # Check in siblings (current's parent's states)
            parent = stack[-2][1] if len(stack) > 1 else self.root
            if "states" not in parent or next_name not in parent["states"]:
                raise ValueError(f"Transition '{token}' points to undefined state '{next_name}'")

            next_state = parent["states"][next_name]
            stack.append((next_name, next_state))
            trace.append(f"δ({next_name}, '{token}') → {next_state.get('category', next_name)}")

            # Enter initial states recursively
            next_state, path = self._enter_initial(next_state, next_name, stack)
            trace.extend(path[1:])  # Skip duplicate initial
            return next_state

        # No transition at current level
        return None

    def _find_parent_accepting_state(self, stack):
        """
        Returns the nearest parent accepting state from the stack.
        """
        for name, state in reversed(stack[:-1]):
            if state.get("type") == "accept":
                return state
        return None

    def _find_final_accepting_category(self, stack):
        # ------------------------------
        # Look from deepest to root for the nearest accepting state.
        # ------------------------------
        for _, state in reversed(stack):
            if state.get("type") == "accept":
                return state.get("category", "Unknown")
        return "Unknown / Review"
