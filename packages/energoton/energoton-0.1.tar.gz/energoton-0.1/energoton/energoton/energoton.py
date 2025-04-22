"""Energoton classes."""

from ..base import Id
from ..relation import Blocking
from ..planner import Plan


class Energoton(Id):
    """Base class for energotons.

    Walks through the given pool of tasks, building all possible plans,
    chooses the best ones and returns them to the user.

    Args:
        capacity (Union[int, List[int]]):
            The amount of energy the energoton has to solve tasks.
            If it's an `int`, on every recharge, energoton's capacity
            will be restored to this value. If it's a `list`, energoton's
            capacity will be taken from the list, cycle by cycle until
            the list is empty.
        id_ (Optional[Union[str, uuid.UUID]]):
            The ID of the energoton. Will be generated if not provided.
        name (Optional[str]):
            The name of the energoton.
    """

    def __init__(self, capacity, id_=None, name=None):
        self.name = name
        self._capacity = capacity
        self.energy_left = self.next_charge

        self.pool = None
        self._dry_pool = None

        self._max_plan_value = 0
        self._cur_plan_value = 0

        self.is_dtrm = isinstance(self, DeterministicEnergoton)

        super().__init__(id_)

    def __eq__(self, other):
        """Equality operator.

        Args:
            other (Energoton): The other energoton to compare with.

        Returns:
            bool: True if the energotons are equal, False otherwise.
        """
        return self.id == other.id

    @property
    def capacity(self):
        """The energoton's capacity.

        Returns:
            Union[int, List[int]]: The energoton's capacity.
        """
        return self._capacity

    @property
    def next_charge(self):
        """Get the next energoton's charge.

        Returns:
            int: The energoton's charge for the next cycle.
        """
        if isinstance(self._capacity, int):
            return self._capacity

        if isinstance(self._capacity, list):
            if len(self._capacity) == 0:
                return 0

            return self._capacity.pop(0)

    def recharge(self):
        """Recharge the energoton."""
        self.energy_left = self.next_charge

    def _commit_plan(self, plan, plans, tasks):
        """Commit the given plan.

        If the plan has a lower value than the current best plan,
        it'll be discarded from further considerations. If the plan
        has a higher value, all the currently stored plans will be
        discarded.

        Args:
            plan (Plan): The plan to commit.
            plans (List[Plan]): Currently considered plans.
            tasks (List[Dict]): The current pool state.
        """
        if plans:
            if self._cur_plan_value < plans[0].value:
                return

            sorted_plan = Plan(sorted(plan, key=sort_key))
            sorted_plan.commit(self._cur_plan_value, tasks)

            if sorted_plan.value > plans[0].value:
                plans.clear()
                self._max_plan_value = sorted_plan.value
            elif sorted_plan in plans:
                return
        else:
            sorted_plan = Plan(sorted(plan, key=sort_key))
            sorted_plan.commit(self._cur_plan_value, tasks)

        plans.append(sorted_plan)

    def _build_plans(self, task, plan, tasks, plans, cycle, ind=0):
        """Recursively build plans with depth-first search.

        Args:
            task (Optional[Dict]): The current task to work on.
            plan (Plan): The current plan being built.
            tasks (List[Dict]): The list of tasks to work on.
            plans (List[Plan]): The list of plans being built.
            cycle (int): The current cycle number.
            ind (int): The index of the current task in the list.
        """
        if task:
            # work on a task
            energy_spent = (
                task["left"]
                if task["left"] <= self.energy_left
                else self.energy_left
            )

            self.energy_left -= energy_spent
            task["left"] -= energy_spent

            or_task = self.pool.children[task["id"]]
            plan.append(
                {
                    "task": or_task,
                    "amount": energy_spent,
                    "assignee": self,
                    "cycle": cycle,
                }
            )
            if self.is_dtrm:
                self._cur_plan_value += or_task.priority.value
            else:
                self._cur_plan_value += or_task.priority.value * (
                    energy_spent / or_task.cost
                )

            if not task["left"]:
                del tasks[ind]

        if not self.energy_left:
            if self._cur_plan_value >= self._max_plan_value:
                self._commit_plan(plan, plans, tasks)
        else:
            # see if it's possible to continue working
            # on the tasks that left
            can_continue = False
            for i, t in enumerate(tasks):
                if self.energy_left < t["left"] and self.is_dtrm:
                    break

                if self.pool.children[t["id"]].relations:
                    if self._is_actual(t["id"]):
                        self._build_plans(t, plan, tasks, plans, cycle, i)
                        can_continue = True
                else:
                    self._build_plans(t, plan, tasks, plans, cycle, i)
                    can_continue = True

            if not can_continue:
                if self._cur_plan_value >= self._max_plan_value:
                    self._commit_plan(plan, plans, tasks)

        if task:
            # reverse all the changes to the pool one step back
            if not task["left"]:
                tasks.insert(ind, task)

            del plan[-1]

            self.energy_left += energy_spent
            task["left"] += energy_spent
            self._cur_plan_value -= or_task.priority.value

    def build_plans(self, dry_pool, cycle=1, plan=None):
        """The main method to build plans.

        Args:
            dry_pool (Dict): The pool of tasks to work on.
            cycle (int): The current cycle number.
            plan (Optional[Plan]):
                The current plan being built. Can include tasks from
                the previous work cycle.
        """
        self._dry_pool = dry_pool
        self._cur_plan_value = plan.value if plan else 0

        plans = []
        self._build_plans(
            task=None,
            plan=plan or Plan(),
            tasks=list(dry_pool.values()),
            plans=plans,
            cycle=cycle,
        )
        return plans

    def _is_actual(self, task_id):
        """Check the given task's relations.

        Args:
            task_id (str): The ID of the task to check.

        Returns:
            bool:
                False if the task is blocked by another task,
                or its alternative is already solved. True otherwise.
        """
        for rel in self.pool.children[task_id].relations.values():
            if isinstance(rel, Blocking):
                if rel.blocked.id == task_id:
                    if rel.blocker.id not in self._dry_pool:
                        continue

                    dry = self._dry_pool[rel.blocker.id]
                    if dry["left"]:
                        return False
            else:
                for alt in rel.alternatives:
                    dry = self._dry_pool[alt.id]
                    if dry["left"] == 0:
                        return False

        return True


class DeterministicEnergoton(Energoton):
    """Transactional type of worker.

    It solves a task, only if it has enough energy to finish it.
    """

    pass


class NonDeterministicEnergoton(Energoton):
    """Partial type of worker.

    It can on a task, even if it doesn't have enough energy to finish it.
    """

    pass


def sort_key(w):
    """Sort key for work logs in a plan.

    Args:
        w (Dict): The work log to sort.

    Returns:
        str: The ID of the task in the work log.
    """
    return w["task"].id
