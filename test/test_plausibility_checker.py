import unittest
from src.validation.plausibility_checker import PlausibilityChecker


class TestStatsGenerator(unittest.TestCase):
    def setUp(self):
        self.pc = PlausibilityChecker()

    def test_validate_valid_report(self):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "15:47",
                "breaks": ["08:12", "09:43"],
                "comment": "qweqwe",
            }
        }
        result, errors = self.pc.validate(report)
        self.assertTrue(result)
        self.assertEqual(len(errors), 0)

    def test_validate_start_after_end(self):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "02:47",
                "breaks": [],
                "comment": "",
            }
        }
        result, errors = self.pc.validate(report)
        self.assertFalse(result)
        self.assertEqual(len(errors), 1)

    def test_validate_uneven_amount_of_breaks(self):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "12:47",
                "breaks": ["10:20"],
                "comment": "",
            }
        }
        result, errors = self.pc.validate(report)
        self.assertFalse(result)
        self.assertEqual(len(errors), 1)

    def test_validate_break_start_after_break_end(self):
        report = {
            "01.02.2023": {
                "start": "07:11",
                "end": "12:47",
                "breaks": ["10:20", "08:11"],
                "comment": "",
            }
        }
        result, errors = self.pc.validate(report)
        self.assertFalse(result)
        self.assertEqual(len(errors), 1)

    def test_skip_check_start_end(self):
        report = {
            "01.02.2023": {
                "start": "15:11",
                "end": "12:47",
                "breaks": ["08:12", "09:12"],
                "comment": "",
            }
        }
        result, errors = self.pc.validate(report, check_start_end=False)
        self.assertTrue(result)
        self.assertEqual(len(errors), 0)

    def test_skip_breaks(self):
        report = {
            "01.02.2023": {
                "start": "10:11",
                "end": "12:47",
                "breaks": ["08:12"],
                "comment": "",
            }
        }
        result, errors = self.pc.validate(report, check_breaks=False)
        self.assertTrue(result)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
