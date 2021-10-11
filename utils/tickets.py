from db import exec, commit
from uuid import uuid4

def new_ticket(event_id, user_id = None, extra_info = None):
    id = exec(
        """
        INSERT INTO tickets (id, event_id, user_id, extra_info)
        VALUES (:id, :event_id, :user_id, :extra_info)
        RETURNING id
        """,
        {
            "id": uuid4(),
            "event_id": event_id,
            "user_id": user_id,
            "extra_info": extra_info,
        }
    )
    commit()
    return id.fetchone()[0]

def stamp_ticket(id, user_id):
    exec(
        """
        UPDATE tickets
        SET stamped = 'true',
            stamped_at = CURRENT_TIMESTAMP,
            stamped_by = :user_id
        WHERE id = :id
        """,
        {
            "id": id,
            "user_id": user_id
        }
    )
    commit()

def unstamp_ticket(id):
    exec(
        """
        UPDATE tickets
        SET stamped = 'false',
            stamped_at = NULL,
            stamped_by = NULL
        WHERE id = :id
        """,
        {
            "id": id
        }
    )
    commit()