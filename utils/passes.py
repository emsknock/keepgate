from db import exec, commit
from uuid import uuid4

def new_pass(event_id, value=0, user_id = None, extra_info = None):
    id = exec(
        """
        INSERT INTO passes (id, event_id, user_id, value, extra_info)
        VALUES (:id, :event_id, :user_id, :value, :extra_info)
        RETURNING id
        """,
        {
            "id": uuid4(),
            "event_id": event_id,
            "user_id": user_id,
            "value": value,
            "extra_info": extra_info,
        }
    )
    commit()
    return id.fetchone()[0]