from db import exec, commit

def delete_organiser(event_id, user_id):
    exec(
        """
        DELETE FROM organisers
        WHERE event_id=:event_id AND user_id=:user_id
        """,
        {
            "event_id": event_id,
            "user_id": user_id
        }
    )
    commit()

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

def update_organiser(user_id,
                     can_create = False, can_delete = False,
                     can_stamp = False, can_unstamp = False,
                     can_topup = False, can_deduct = False):
    exec(
        """
        UPDATE organisers
        SET can_create=:can_create, can_delete=:can_delete,
            can_stamp=:can_stamp,   can_unstamp=:can_unstamp,
            can_topup=:can_topup,   can_deduct=:can_deduct
        WHERE id=:user_id
        """,
        {
            "user_id": user_id,
            "can_create": can_create, "can_delete": can_delete,
            "can_stamp": can_stamp,   "can_unstamp": can_unstamp,
            "can_topup": can_topup,   "can_deduct": can_deduct
        }
    )
    commit()