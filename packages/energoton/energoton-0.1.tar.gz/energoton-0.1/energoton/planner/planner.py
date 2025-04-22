"""Planning related classes."""

import copy


class Plan(list):
    """A single work plan.

    Represents a possible work plan. Consists of dicts, each of which
    represents a piece of work done by some energoton on some task.
    """

    def commit(self, value, dry_pool):
        """Commit the plan and finalize its statistics.

        Args:
            value (int): The value of the plan.
            dry_pool (list): The dry pool after the plan.
        """
        self.value = value
        self.energy_spent = 0
        dry = []

        self.dry_pool_after_plan = {t["id"]: t for t in dry_pool}

        for w in self:
            self.energy_spent += w["amount"]
            dry.append((w["task"].id, w["amount"]))

        self.dry = tuple(dry)

    def __eq__(self, other):
        """Equality operator.

        Returns:
            bool: True if the plans are equal, False otherwise.
        """
        return self.dry == other.dry


class Planner:
    """
    Planner builds plans for the given pool
    and provides methods to analyze them.

    NOTE: On init, Planner makes a deep copy
    of the given pool. It sticks the planner
    to the pool, and allows to re-use the pool
    in multiple planners (e.g. you have 2 teams and
    you want to compare how they'll handle the same
    pool of tasks, running planners in parallel).

    Args:
        pool (work.pool.Pool):
            The pool of tasks to be solved.
    """

    def __init__(self, pool):
        if len(pool) == 0:
            raise ValueError(
                f"The given pool {pool.id} - {pool.name} is empty."
            )

        self._pool = copy.deepcopy(pool)
        self._dry_pool = self._pool.dry

        self._plans = [Plan()]

    def build_plans(self, energotons, cycles=1):
        """Build plans for the given energotons and amount of cycles.

        Energotons are copied on the method call, so they can be
        safely reused in multiple planners.

        Args:
            energotons (List[Energoton]):
                List of energotons to be used for planning.
            cycles (int):
                Number of work cycles to be performed.

        Return:
            tuple[Plan]: The best plans found.
        """
        if len(energotons) == 0:
            raise ValueError("No energotons provided for planning.")

        if cycles < 1:
            raise ValueError(
                "The number of work cycles must be greater than 0."
            )

        energotons = copy.deepcopy(energotons)
        for e in energotons:
            e.pool = self._pool

        self._plans = (Plan(),)

        for c in range(1, cycles + 1):
            for e in energotons:
                new_plans = []
                for plan in self._plans:
                    for new_plan in e.build_plans(
                        (
                            plan.dry_pool_after_plan
                            if getattr(plan, "dry_pool_after_plan", None)
                            else self.dry_pool_after_plan(plan)
                        ),
                        c,
                        plan,
                    ):
                        if new_plans:
                            if new_plan.value < new_plans[0].value:
                                continue

                            if new_plan.value > new_plans[0].value:
                                new_plans.clear()

                        if new_plan not in new_plans:
                            new_plans.append(new_plan)

                self._plans = tuple(new_plans)
                e.recharge()

        return self._plans

    def pool_after_plan(self, plan):
        """Return the pool state after the given plan.

        Args:
            plan (Plan): The plan to be applied.

        Returns:
            Pool: The pool state after the plan is executed.
        """
        pool = copy.deepcopy(self._pool)

        for work_done in plan:
            pool.children[work_done["task"].id].work_done.append(work_done)

        return pool

    def dry_pool_after_plan(self, plan):
        """Return the dry pool state after the given plan.

        Used for plan calculations.

        Args:
            plan (Plan): The plan to be applied.

        Returns:
            Dict[str, Dict[str, Any]]:
                The dry pool state after the plan is executed.
        """
        pool = copy.deepcopy(self._dry_pool)

        for work_done in plan:
            task = pool[work_done["task"].id]
            task["left"] -= work_done["amount"]
            if task["left"] == 0:
                del pool[work_done["task"].id]

        return pool

    @staticmethod
    def by_cycles(plans):
        """Group plans by cycles.

        Args:
            plans (List[Plan]): The plans to be grouped.

        Returns:
            List[Dict[str, List[Dict[str, Any]]]]:
                The plans grouped by cycles.
        """
        by_cycles = []
        for plan in plans:
            new_plan = {}
            for work_done in plan:
                if work_done["cycle"] not in new_plan:
                    new_plan[work_done["cycle"]] = []

                new_plan[work_done["cycle"]].append(work_done)

            by_cycles.append(new_plan)

        return by_cycles

    @staticmethod
    def by_assignees(plans):
        """Group plans by assignees.

        Args:
            plans (List[Plan]): The plans to be grouped.

        Returns:
            List[Dict[str, List[Dict[str, Any]]]]:
                The plans grouped by assignees.
        """
        by_assignees = []
        for plan in plans:
            new_plan = {}
            for work_done in plan:
                as_id = work_done["assignee"].id

                if as_id not in new_plan:
                    new_plan[as_id] = []

                new_plan[as_id].append(work_done)

            by_assignees.append(new_plan)

        return by_assignees
