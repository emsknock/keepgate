from db import exec, commit

def add_organiser(event_id, user_id):
    exec(
        """
        INSERT INTO organisers (event_id, user_id)
        VALUES (:event_id, :user_id)
        """,
        {
            "event_id": event_id,
            "user_id": user_id,
        }
    )
    commit()