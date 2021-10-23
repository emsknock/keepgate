from uuid import uuid4
from db import exec, commit

def delete_ticket(ticket_id):
    exec(
        "DELETE FROM tickets WHERE id=:ticket_id",
        {
            "ticket_id": ticket_id
        }
    )
    commit()

def new_tickets(event_id, count):
    for _ in range(0, count):
        exec(
            """
            INSERT INTO tickets (id, event_id)
            VALUES (:id, :event_id)
            """,
            {
                "id": uuid4(),
                "event_id": event_id
            }
        )
    commit()

def get_ticket(id):
    result = exec(
        """
        SELECT id,
               event_id,
               user_id,
               extra_info,
               stamped,
               stamped_at,
               stamped_by,
               (SELECT username FROM users WHERE id = stamped_by) AS stamped_by_username
        FROM tickets
        WHERE id = :id
        """,
        {
            "id": id
        }
    )
    return result.fetchone()

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

def update_ticket_data(ticket_id, extra_info = None):
    exec(
        """
        UPDATE tickets
        SET extra_info = :extra_info
        WHERE id = :ticket_id
        """,
        {
            "ticket_id": ticket_id,
            "extra_info": extra_info
        }
    )
    commit()