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

def get_detailed_event_list(user_id):
    result = exec(
        """
        SELECT e.id, e.title, e.date, e.extra_info,
               COUNT(t.id) as ticket_count
        FROM events e LEFT JOIN tickets t ON e.id = t.event_id
        WHERE e.user_id = :user_id
        GROUP BY e.id
        """,
        {
            "user_id": user_id
        }
    )
    return result.fetchall()