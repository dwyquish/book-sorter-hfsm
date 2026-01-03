import re

class HFSMEngine:
    """
    Deterministic Finite Automaton (DFA) engine operating over token input.
    """

    def __init__(self, rules):
        # 1. Validation Logic
        if not rules:
            raise ValueError("Rules cannot be empty")
        
        # Check for the NEW structure (Person A's format)
        if "start_state" not in rules or "states" not in rules:
            # Fallback check: Did we use the OLD structure?
            if "START" in rules:
                raise ValueError("Old rule format detected! Please update rules.json to use 'start_state' and 'states'.")
            raise ValueError("Invalid rules: must contain 'start_state' and 'states'")

        self.rules = rules
        self.start_state = rules["start_state"]
        self.states = rules["states"]

    def tokenize(self, text):
        """
        Converts text into a clean list of words.
        Ex: "Intro to Python!" -> ['intro', 'to', 'python']
        """
        if not text:
            return []
        # Lowercase and remove anything that isn't a letter or number
        clean_text = re.sub(r'[^a-z0-9\s]', '', str(text).lower())
        return clean_text.split()

    def classify(self, title):
        """
        Runs the Finite State Machine on a book title.
        """
        tokens = self.tokenize(title)
        current_state = self.start_state
        trace = [current_state]

        # 1. Traversal Loop
        for word in tokens:
            # Get definition of current state
            state_def = self.states.get(current_state, {})
            transitions = state_def.get("transitions", {})
            
            # Check transition
            if word in transitions:
                next_state = transitions[word]
                # Log the math symbol for the Professor (δ = delta)
                trace.append(f"δ({current_state}, '{word}') → {next_state}")
                current_state = next_state
                
                # Check if we hit an ACCEPT state immediately
                if self.states.get(current_state, {}).get("type") == "accept":
                    return {
                        "category": self.states[current_state].get("category", "Unknown"),
                        "trace": " -> ".join(trace),
                        "confidence": 1.0
                    }
            else:
                # No transition found, stay or ignore
                pass

        # 2. End of String Check
        final_state_def = self.states.get(current_state, {})
        
        if final_state_def.get("type") == "accept":
            return {
                "category": final_state_def.get("category", "Unknown"),
                "trace": " -> ".join(trace),
                "confidence": 1.0
            }
        else:
            return {
                "category": "Unknown / Review",
                "trace": " -> ".join(trace) + " -> (Stuck/Rejected)",
                "confidence": 0.0
            }