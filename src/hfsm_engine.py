import re

class HFSMEngine:
    def __init__(self, rules):
        """
        Initialize the HFSM with a dictionary of rules.
        """
        self.rules = rules
        # Ensure we have a valid start state
        if "START" not in self.rules:
            raise ValueError("Rules must contain a 'START' state.")

    def tokenize(self, text):
        """
        Converts text into a clean list of words.
        Ex: "Intro to Python!" -> ['intro', 'to', 'python']
        """
        if not isinstance(text, str):
            return []
        # Lowercase and remove anything that isn't a letter or space
        clean_text = re.sub(r'[^a-z\s]', '', text.lower())
        return clean_text.split()

    def classify(self, title):
        """
        Runs the Finite State Machine on a book title.
        Returns: {category, confidence, trace}
        """
        tokens = self.tokenize(title)
        current_state = "START"
        trace = ["START"]
        
        # 1. Traversal Loop (The "Input Tape")
        for word in tokens:
            state_def = self.rules.get(current_state)
            
            # Check if current state has transitions
            if not state_def or "transitions" not in state_def:
                break
            
            # Check if the word triggers a transition
            transitions = state_def["transitions"]
            if word in transitions:
                next_state = transitions[word]
                current_state = next_state
                trace.append(f"matched('{word}') -> {current_state}")
            else:
                # No transition found for this word, stay in current state (or ignore word)
                pass

        # 2. Check Result (Did we land on an Accept state?)
        final_state_def = self.rules.get(current_state)
        
        if final_state_def and final_state_def.get("type") == "accept":
            return {
                "category": final_state_def.get("category", "Unknown"),
                "confidence": 1.0,
                "trace": " -> ".join(trace)
            }
        else:
            return {
                "category": "Unknown / Review",
                "confidence": 0.0,
                "trace": " -> ".join(trace) + " -> (Stuck)"
            }