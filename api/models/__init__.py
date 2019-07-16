from sqlalchemy import event

from api.utilities.push_id import PushID

from api.models.users import User

def fancy_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    push_id = PushID()
    target.id = push_id.next_id()


# associate the listener function with models, to execute during the
# "before_insert" event
tables = [User]

for table in tables:
    event.listen(table, 'before_insert', fancy_id_generator)
