from db import exec, commit
from uuid import uuid4

def new_passes(event_id, count):
    for _ in range(0, count):
        exec(
            """
            INSERT INTO passes (id, event_id)
            VALUES (:id, :event_id)
            """,
            {
                "id": uuid4(),
                "event_id": event_id
            }
        )
    commit()

def get_pass(id):
    result = exec(
        """
        SELECT id,
               event_id,
               user_id,
               extra_info,
               value
        FROM passes
        WHERE id = :id
        """,
        {
            "id": id
        }
    )
    return result.fetchone()

def update_pass_data(pass_id, extra_info = None):
    exec(
        """
        UPDATE passes
        SET extra_info = :extra_info
        WHERE id = :pass_id
        """,
        {
            "pass_id": pass_id,
            "extra_info": extra_info
        }
    )
    commit()

def pass_modify_value(pass_id, value):
    exec(
        """
        UPDATE passes
        SET value = value + :value
        WHERE id = :pass_id
        """,
        {
            "pass_id": pass_id
        }
    )
    commit()