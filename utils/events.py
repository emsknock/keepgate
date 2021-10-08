from db import exec, commit

def new_event(user_id, title, extra_info = None, date = None):
    exec(
        """
        INSERT INTO events (user_id, title, extra_info, date)
        VALUES (:user_id, :title, :extra_info, :date)
        """,
        {
            "user_id": user_id,
            "title": title,
            "extra_info": extra_info,
            "date": date,
        }
    )
    commit()

def get_events_by_user_id(user_id):
    result = exec(
        "SELECT id, title, date FROM events WHERE user_id=:user_id",
        {
            "user_id": user_id
        }
    )
    return result.fetchall()