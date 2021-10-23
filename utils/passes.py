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

def pass_modify_value(pass_id, value, user_id):
    new_value = exec(
        """
        INSERT INTO pass_transactions (pass_id, user_id, value)
        VALUES (:pass_id, :user_id, :value)
        ;
        UPDATE passes
        SET value = value + :value
        WHERE id = :pass_id
        RETURNING value
        """,
        {
            "pass_id": pass_id,
            "user_id": user_id,
            "value": value
        }
    )
    commit()
    return new_value.fetchone()[0]

def get_pass_transactions(pass_id):
    result = exec(
        """
        SELECT t.value,
               t.time,
               u.username
        FROM pass_transactions t
            LEFT JOIN users u
            ON t.user_id = u.id
        WHERE t.pass_id = :pass_id
        """,
        {
            "pass_id": pass_id
        }
    )
    commit()
    return result.fetchall();