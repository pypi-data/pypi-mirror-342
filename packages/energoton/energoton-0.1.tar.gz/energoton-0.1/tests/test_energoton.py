import unittest

from energoton import (
    Alternative,
    Blocking,
    Pool,
    Task,
    DeterministicEnergoton,
    NonDeterministicEnergoton,
)
from energoton.planner import Plan


class TestEnergoton(unittest.TestCase):
    def test_build_plans_deterministic(self):
        pool = Pool()
        t1 = Task(5, id_=1)
        t2 = Task(2, id_=2)
        t3 = Task(4, id_=3)
        t4 = Task(2, id_=4)
        t5 = Task(6, id_=5)

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        e = DeterministicEnergoton(8)
        e.pool = pool
        plans = e.build_plans(pool.dry)

        p = Plan(
            [
                {"task": t2, "amount": 2, "assignee": e, "dry": (t2.id, 2)},
                {"task": t3, "amount": 4, "assignee": e, "dry": (t3.id, 4)},
                {"task": t4, "amount": 2, "assignee": e, "dry": (t4.id, 2)},
            ]
        )
        p.commit(0, ())

        self.assertEqual(plans, [p])

    def test_build_plans_non_deterministic(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)

        e = NonDeterministicEnergoton(8)
        e.pool = pool
        plans = e.build_plans(pool.dry)

        p1 = Plan(
            [
                {"task": t1, "amount": 2, "assignee": e, "dry": (t1.id, 2)},
                {"task": t2, "amount": 2, "assignee": e, "dry": (t2.id, 2)},
                {"task": t3, "amount": 4, "assignee": e, "dry": (t3.id, 4)},
            ]
        )
        p1.commit(0, ())

        self.assertEqual(plans, [p1])

    def test_build_plans_blocked(self):
        pool = Pool()
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        Blocking(t5, t3)

        e = DeterministicEnergoton(8)
        e.pool = pool
        plans = e.build_plans(pool.dry)

        p1 = Plan(
            [
                {"task": t2, "amount": 2, "assignee": e, "dry": (t2.id, 2)},
                {"task": t4, "amount": 2, "assignee": e, "dry": (t4.id, 2)},
            ]
        )
        p2 = Plan(
            [
                {"task": t1, "amount": 5, "assignee": e, "dry": (t1.id, 5)},
                {"task": t2, "amount": 2, "assignee": e, "dry": (t2.id, 2)},
            ]
        )
        p3 = Plan(
            [
                {"task": t2, "amount": 2, "assignee": e, "dry": (t2.id, 2)},
                {"task": t5, "amount": 6, "assignee": e, "dry": (t5.id, 6)},
            ]
        )
        p4 = Plan(
            [
                {"task": t1, "amount": 5, "assignee": e, "dry": (t1.id, 5)},
                {"task": t4, "amount": 2, "assignee": e, "dry": (t4.id, 2)},
            ]
        )
        p5 = Plan(
            [
                {"task": t4, "amount": 2, "assignee": e, "dry": (t4.id, 2)},
                {"task": t5, "amount": 6, "assignee": e, "dry": (t5.id, 6)},
            ]
        )
        p1.commit(0, ())
        p2.commit(0, ())
        p3.commit(0, ())
        p4.commit(0, ())
        p5.commit(0, ())

        self.assertEqual(
            plans,
            [p1, p2, p3, p4, p5],
        )

    def test_build_plans_alternative(self):
        pool = Pool(name="Pool")
        t1 = Task(5, id_="1")
        t2 = Task(2, id_="2")
        t3 = Task(4, id_="3")
        t4 = Task(2, id_="4")
        t5 = Task(6, id_="5")

        pool.add(t1)
        pool.add(t2)
        pool.add(t3)
        pool.add(t4)
        pool.add(t5)

        Alternative(t1, t2)

        e = DeterministicEnergoton(8)
        e.pool = pool
        plans = list(e.build_plans(pool.dry))

        p = Plan(
            [
                {"task": t2, "amount": 2, "assignee": e, "dry": (t2.id, 2)},
                {"task": t3, "amount": 4, "assignee": e, "dry": (t3.id, 4)},
                {"task": t4, "amount": 2, "assignee": e, "dry": (t4.id, 2)},
            ]
        )
        p.commit(0, ())

        self.assertEqual(plans, [p])

    def test_charges(self):
        charge = 5
        e = DeterministicEnergoton(charge)
        self.assertEqual(e.energy_left, charge)
        self.assertEqual(e.next_charge, charge)

        e = DeterministicEnergoton([5, 3, 2])
        self.assertEqual(e.energy_left, 5)
        e.recharge()

        self.assertEqual(e.energy_left, 3)
        e.recharge()

        self.assertEqual(e.energy_left, 2)
        e.recharge()

        self.assertEqual(e.energy_left, 0)
