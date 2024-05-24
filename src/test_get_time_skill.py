import unittest
from get_time_skill import GetTimeSkill

class TestGetTimeSkill(unittest.TestCase):
    def test_process(self):
        skill = GetTimeSkill()
        response = skill.process("any input")  # Input doesn't matter for this skill
        self.assertIn("The current time is", response)

if __name__ == "__main__":
    unittest.main()
