"""Relations between work units."""

from energoton.base import Id


class Alternative(Id):
    """Alternative relation.

    Describes tasks, which can be replaced by each other.
    If one of the alternative tasks is solved, all the others
    are no longer considered by energotons and will not be solved.

    Args:
        alternatives (List[Task | Pool]):
            List of alternative tasks.
        id_ (Optional[str]):
            Id of the relation. Generated, if not provided.
    """

    def __init__(self, *alternatives, id_=None):
        super().__init__(id_)

        if len(alternatives) <= 1:
            raise ValueError(
                "Alternative relation must have at least two alternatives."
            )

        self.alternatives = alternatives

        for unit in alternatives:
            unit.relations[self.id] = self

    @property
    def is_solved(self):
        """Check if the alternative relation is solved.

        Returns:
            bool: True if one of the alternatives is solved, False otherwise.
        """
        return any(unit.is_solved for unit in self.alternatives)


class Blocking(Id):
    """Blocking relation.

    The blocked tasks is not considered by energotons until the
    blocker is solved.

    Args:
        blocker (Task | Pool):
        blocked (Task | Pool):
        id_ (Optional[str]):
            Id of the relation. Generated, if not provided.
    """

    def __init__(self, blocker, blocked, id_=None):
        super().__init__(id_)

        self.blocker = blocker
        self.blocked = blocked

        self.blocker.priority = (
            self.blocked.priority
            if self.blocked.priority.value > self.blocker.priority.value
            else self.blocker.priority
        )

        blocked.relations[self.id] = self
        blocker.relations[self.id] = self

    def drop(self):
        """Drop the blocking relation."""
        del self.blocked.relations[self.id]
        del self.blocker.relations[self.id]
