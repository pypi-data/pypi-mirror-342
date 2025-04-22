import unittest
from unittest import mock

from energoton import Task, Priority
from energoton.planner import Plan


class TestPlan(unittest.TestCase):
    def test_value(self):
        tasks = (
            Task(5, priority=Priority("lowest")),
            Task(5, priority=Priority("low")),
            Task(5, priority=Priority("normal")),
            Task(5, priority=Priority("high")),
            Task(5, priority=Priority("highest")),
        )

        work_done = [
            {"task": t, "amount": 5, "assignee": mock.Mock(), "dry": (t.id, 5)}
            for t in tasks
        ]
        plan = Plan(work_done)
        plan.commit(31, ())

        self.assertEqual(plan.value, 31)
