from db import exec, commit

def new_ticket(event_id, user_id = None, extra_info = None):
    exec(
        """
        INSERT INTO tickets (event_id, user_id, extra_info)
        VALUES (:event_id, :user_id, :extra_info)
        """,
        {
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