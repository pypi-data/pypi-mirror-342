import abc

from energoton.base import Id

from ..relation import Alternative, Blocking


class Priority:
    """A work unit priority.

    Priority is used to determine the task value. The higher
    is the priority, the higher is the value, and the more
    chance that the energoton will choose this task for solving.

    Args:
        label (Literal["lowest", "low", "normal", "high", "highest", "must"]):
            Priority label.
    """

    exp_values = {
        "lowest": 1,
        "low": 2,
        "normal": 4,
        "high": 8,
        "highest": 16,
        "must": 1000000,
    }

    def __init__(self, label):
        self.label = label
        self.value = self.exp_values[label]

    def __repr__(self):
        return f"Priority('{self.label}')"


class WorkUnit(Id, metaclass=abc.ABCMeta):
    """Represents a single work unit to do. Can be a task or a pool.

    Args:
        custom_fields (Optional[Dict[str: Any]]):
            Custom fields for the work unit. Can be accessed by keys:
            >>> work_unit['field_name']
        parent (Optional[Pool]):
            Parent pool.
        priority (Optional[Priority]):
            Priority of the work unit. Defaults to "medium" priority.
        id_ (Optional[str | uuid.UUID]):
            Id of the work unit. Generated, if not provided explicitly.
        name (Optional[str]):
            Name of the work unit.
    """

    def __init__(
        self,
        custom_fields=None,
        parent=None,
        priority=Priority("normal"),
        id_=None,
        name=None,
    ):
        super().__init__(id_)

        self.custom_fields = custom_fields or {}
        self.name = name
        self.relations = {}
        self.priority = priority
        self.parent = parent

    @abc.abstractmethod
    def is_solved(self):
        """Check if the work unit is solved.

        Raises:
            NotImplementedError:
                Must be implemented for any work unit.
        """
        raise NotImplementedError(
            "is_solved method must be implemented for any work unit!"
        )

    def __delitem__(self, key):
        """A custom field deletion.

        Args:
            key (str): Field name.
        """
        del self.custom_fields[key]

    def __getitem__(self, key):
        """A custom field access.

        Args:
            key (str): Field name.

        Returns:
            Any: Custom field value.
        """
        return self.custom_fields[key]

    def __setitem__(self, key, value):
        """A custom field setting."

        Args:
            key (str): Field name.
            value (Any): Field value.
        """
        self.custom_fields[key] = value

    @property
    def blocked_by(self):
        """
        Return all relations that prevent this work
        unit from being done.

        Yields:
            work.relation.Blocking: Blocking relations.
        """
        for rel in self.relations.values():
            if (
                isinstance(rel, Blocking)
                and rel.blocked == self
                and not rel.blocker.is_solved
            ):
                yield rel

    @property
    def blocking(self):
        """
        Return all relations where this work unit
        prevents other units from being solved.

        Yields:
            work.relation.Blocking: Blocking relations.
        """
        for rel in self.relations.values():
            if (
                isinstance(rel, Blocking)
                and rel.blocker == self
                and not self.is_solved
            ):
                yield rel

    @property
    def is_actual(self):
        """Check if this unit still needs to be solved.

        Returns:
            bool:
                True if the unit is not solved and its
                alternatives are not solved as well.
        """
        for rel in self.relations.values():
            if isinstance(rel, Alternative) and rel.is_solved:
                return False

        return True

    @property
    def is_blocked(self):
        """Check if this unit is blocked by another unit.

        Returns:
           bool: True if the unit is blocked, False otherwise.
        """
        try:
            next(self.blocked_by)
            return True
        except StopIteration:
            return self.parent.is_blocked if self.parent else False
