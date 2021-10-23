from db import exec, commit
from utils import events
from flask import session

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

def get_user_organised_events(user_id):
    result = exec(
        """
        SELECT e.id, e.title, e.date,
               (SELECT username FROM users u WHERE u.id = e.user_id) AS username
        FROM organisers o
            LEFT JOIN events e
            ON o.event_id = e.id
        WHERE o.user_id=:user_id
        """,
        {
            "user_id": user_id
        }
    )
    return result.fetchall()

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

def get_organiser(event_id, user_id):
    result = exec(
        """
        SELECT can_create, can_delete,
               can_stamp, can_unstamp,
               can_topup, can_deduct
        FROM organisers
        WHERE event_id=:event_id AND user_id=:user_id
        """,
        {
            "event_id": event_id,
            "user_id": user_id
        }
    )
    return result.fetchone()

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

def get_permissions(event_id):
    if events.does_user_own_event(session["user_id"], event_id):
        return {
            "can_create": True, "can_delete": True,
            "can_stamp": True,   "can_unstamp": True,
            "can_topup": True,   "can_deduct": True
        }
    return get_organiser(event_id, session["user_id"])