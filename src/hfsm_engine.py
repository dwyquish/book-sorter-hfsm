from __future__ import annotations
import re
from typing import Dict, List, Any


class HFSMEngine:
    """
    Deterministic Finite Automaton (DFA) engine operating over token input.
    """

    def __init__(self, rules: Dict[str, Any]):
        if not rules or "start_state" not in rules or "states" not in rules:
            raise ValueError("Invalid rules: must contain 'start_state' and 'states'")

        from .validator import RuleValidator
        # Validate rule structure before using
        RuleValidator.validate(rules)
        self.rules = rules
        self.start_state = rules["start_state"]
        self.states = rules["states"]

    # Tokenization = Input Tape
    def tokenize(self, text: str) -> List[str]:
        """
        Converts raw text into lowercase tokens.
        Σ = set of word tokens (not characters).
        """
        if not text:
            return []
        text = text.lower()
        return re.findall(r"[a-z0-9]+", text)

    # DFA Execution
    def classify(self, title: str) -> Dict[str, Any]:
        """
        Run DFA on a single book title.

        Returns:
        {
          "category": str,
          "trace": str
        }
        """
        tokens = self.tokenize(str(title))
        current_state = self.start_state

        trace: List[str] = [current_state]

        # DFA traversal (single pass, deterministic)
        for token in tokens:
            state_def = self.states.get(current_state, {})
            transitions = state_def.get("transitions", {})

            if token in transitions:
                next_state = transitions[token]
                trace.append(f"δ({current_state}, '{token}') → {next_state}")
                current_state = next_state

                # Accept states are terminal
                if self.states.get(current_state, {}).get("type") == "accept":
                    return {
                        "category": self.states[current_state].get("category", "Unknown"),
                        "trace": " -> ".join(trace),
                    }

        # End of input: acceptance check
        final_def = self.states.get(current_state, {})

        if final_def.get("type") == "accept":
            return {
                "category": final_def.get("category", "Unknown"),
                "trace": " -> ".join(trace),
            }

        # Explicit REJECT state
        trace.append("REJECT")
        return {
            "category": "Unknown",
            "trace": " -> ".join(trace),
        }