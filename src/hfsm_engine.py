import re

class HFSMEngine:

    def __init__(self, rules):
        self.rules = rules
        self.root = rules["states"][rules["start_state"]]

    def tokenize(self, text):
        if not text:
            return []
        clean = re.sub(r'[^a-z0-9\s]', '', text.lower())
        return clean.split()

    def classify(self, text):
        tokens = self.tokenize(text)
        state_stack = []
        trace = []

        # Enter root
        current = self.root
        state_stack.append("root")

        # Enter initial state
        current = current["states"][current["initial"]]
        state_stack.append(current)

        for token in tokens:
            transitioned = self._try_transition(current, token, state_stack, trace)
            if transitioned:
                current = transitioned

        # Find deepest accepting state
        for state in reversed(state_stack):
            if isinstance(state, dict) and state.get("type") == "accept":
                return {
                    "category": state.get("category"),
                    "trace": " → ".join(trace),
                    "confidence": 1.0
                }

        return {
            "category": "Unknown / Review",
            "trace": " → ".join(trace),
            "confidence": 0.0
        }

    def _try_transition(self, state, token, stack, trace):
        # Local transition
        if "transitions" in state and token in state["transitions"]:
            next_name = state["transitions"][token]
            parent = stack[-2] if len(stack) > 1 else None

            if parent and "states" in parent:
                next_state = parent["states"][next_name]
                stack.append(next_state)
                trace.append(f"δ({next_name}, '{token}')")
                return next_state

        # Inherit transition from parent
        if len(stack) > 1:
            return self._try_transition(stack[-2], token, stack, trace)

        return None
