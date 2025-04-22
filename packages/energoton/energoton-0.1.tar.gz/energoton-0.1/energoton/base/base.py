"""Basic functionality classes."""

import uuid


class Id:
    """
    Object id functionality. Used by energotons,
    pools, relations and tasks.

    Args:
        id_ (Optional[Union[str, uuid.UUID]]):
            The object id. If not provided,
            a UUID is generated.
    """

    def __init__(self, id_=None):
        self.id = id_ or uuid.uuid4()

    def __eq__(self, other):
        """Equality operator.

        Args:
            other (Any): Object to compare.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        return self.id == other.id
