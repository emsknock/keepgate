from db import exec, commit
from uuid import uuid4

def new_ticket(event_id, user_id = None, extra_info = None):
    exec(
        """
        INSERT INTO tickets (id, event_id, user_id, extra_info)
        VALUES (:id, :event_id, :user_id, :extra_info)
        """,
        {
            "id": uuid4(),
            "event_id": event_id,
            "user_id": user_id,
            "extra_info": extra_info,
        }
    )
    commit()

def get_ticket_count_for_event(event_id):
    result = exec(
        "SELECT COUNT(*) FROM events WHERE event_id=:event_id",
        {
            "event_id": event_id
        }
    )
    return result.fetchone()[0]