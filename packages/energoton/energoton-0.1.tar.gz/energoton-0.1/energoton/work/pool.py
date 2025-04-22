from .work_unit import Priority, WorkUnit
from .task import Task


class Pool(WorkUnit):
    """A group of tasks. Can be embedded into another pool.

    A pool doesn't represent a task by itself. It's only
    a container for tasks.

    Args:
        custom_fields (Optional[Dict[str, Any]):
            Custom fields for the pool. Not used in plan calculations.
            Can be accessed by keys:
            >>> pool['field_name']
        parent (Optional[Pool]):
            Parent pool.
        priority (Optional[Priority]):
            The pool's priority. Defaults to "normal".
        children (Optional[List[Task | Pool]]):
            List of child tasks and pools, embedded into this pool.
        id_ (Optional[str]):
            Unique identifier for the pool. Generated if not provided.
        name (Optional[str]):
            Name of the pool.
    """

    def __init__(
        self,
        custom_fields=None,
        parent=None,
        priority=Priority("normal"),
        children=[],
        id_=None,
        name=None,
    ):
        self.children = {}
        self._indexate_pool(children)

        super().__init__(custom_fields, parent, priority, id_, name)

    def _indexate_pool(self, pool):
        """Indexate the given pool's children into a dict for fast access.

        Args:
            pool (Pool):
                A pool to indexate.
        """
        for c in pool:
            if c.id in self.children:
                raise ValueError(
                    (
                        f"Child '{c.name}' with id '{c.id}' already"
                        " exists in the pool {self.name}."
                    )
                )

            if isinstance(c, Pool):
                self._indexate_pool(c)

            if not c.parent:
                c.parent = self

            self.children[c.id] = c

    def __iter__(self):
        """Iterate over the pool's children.

        Returns:
            Iterator[Task | Pool]:
                An iterator over this pool's children.
        """
        return iter(filter(lambda c: c.parent == self, self.children.values()))

    def __len__(self):
        """This pool's length.

        Returns:
            int: The number of children in this pool.
        """
        return len(self.children)

    def __repr__(self):
        """String representation of the pool.

        Returns:
            str:
        """
        return f"Pool(id={self.id}, name={self.name})"

    @property
    def dry(self):
        """A minified version of the pool.

        Used during plans calculation to reduce the amount of data
        to process.

        Returns:
            Dict[str, Dict[str, Any]]:
                A dictionary with the pool's children dry versions.
        """
        todo = list(
            filter(
                lambda c: not c.is_solved and isinstance(c, Task),
                self.children.values(),
            )
        )
        todo.sort(key=lambda t: t.cost)

        dry = {t.id: t.dry for t in todo}
        return dry

    @property
    def done(self):
        """Tasks from this pool that are done.

        Returns:
            Iterator[Task]:
        """
        for t in filter(
            lambda c: c.is_solved and c.parent == self, self.children.values()
        ):
            yield t

    @property
    def is_solved(self):
        """This pool solved status.

        Returns:
            bool: True if all tasks in this pool are solved, False otherwise.
        """
        for c in self.children.values():
            if not c.is_solved:
                return False

        return True

    @property
    def todo(self):
        """Tasks from this pool that are not done.

        Returns:
            Iterator[Task]:
        """
        for t in filter(
            lambda c: not c.is_solved and c.parent == self,
            self.children.values(),
        ):
            yield t

    def add(self, child):
        """Add a task or pool into this pool.

        Args:
            child (Task | Pool):
                A task or pool to add into this pool.
        """
        if child.id in self.children:
            raise ValueError(
                (
                    f"Child with id '{child.id}' already exists "
                    "in the pool {self.id}."
                )
            )

        child.parent = self
        self.children[child.id] = child

        if isinstance(child, Pool):
            self._indexate_pool(child)

    def get(self, child_id):
        """Return a child from this pool by its id.

        Can return children of the embedded pools.

        Args:
            child_id (uuid.UUID | str):
                The id of the child to return.

        Returns:
            Task | Pool:
        """
        return self.children[child_id]

    def pop(self, child_id):
        """Remove a child from this pool by its id.

        Can remove children of the embedded pools.

        Args:
            child_id (uuid.UUID | str):
                The id of the child to remove.

        Returns:
            Task | Pool:
                The removed child.
        """
        child = self.children[child_id]
        child.parent._pop(child_id)

        child.parent = None
        return child

    def _pop(self, child_id):
        """
        Convenience method to recursively remove a child
        from this and the parent pools.

        Args:
            child_id (uuid.UUID | str):
                The id of the child to remove.
        """
        del self.children[child_id]
        if self.parent:
            self.parent._pop(child_id)
