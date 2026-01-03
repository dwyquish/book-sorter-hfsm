import unittest
from src.hfsm_engine import HFSMEngine

class TestHFSMEngine(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "start_state": "s0",
            "states": {
                "s0": {"transitions": {"python": "s_py"}},
                "s_py": {"type": "accept", "category": "Computer Science"}
            }
        }
        self.engine = HFSMEngine(self.rules)

    def test_python_title(self):
        result = self.engine.classify('Learning Python')
        self.assertEqual(result['category'], 'Computer Science')

    def test_non_python_title(self):
        result = self.engine.classify('History of Rome')
        self.assertEqual(result['category'], 'Unknown')

if __name__ == '__main__':
    unittest.main()