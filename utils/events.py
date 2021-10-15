from db import exec, commit

def new_event(user_id, title, extra_info = None, date = None):
    id = exec(
        """
        INSERT INTO events (user_id, title, extra_info, date)
        VALUES (:user_id, :title, :extra_info, :date)
        RETURNING id
        """,
        {
            "user_id": user_id,
            "title": title,
            "extra_info": extra_info,
            "date": date if date else None,
        }
    )
    commit()
    return id.fetchone()[0]

def get_detailed_event_list(user_id):
    result = exec(
        """
        SELECT e.id, e.title, e.date, e.extra_info,
               (SELECT COUNT(*) FROM tickets WHERE event_id = e.id) as ticket_count,
               (SELECT COUNT(*) FROM passes WHERE event_id = e.id) as pass_count,
               (SELECT COUNT(*) FROM organisers WHERE event_id = e.id) as organiser_count
        FROM events e
        WHERE e.user_id = :user_id
        """,
        {
            "user_id": user_id
        }
    )
    return result.fetchall()

def get_event_info(event_id):
    result = exec(
        """
        SELECT id, title, date, extra_info, user_id,
               (SELECT COUNT(*) FROM tickets WHERE event_id = :event_id) as ticket_count,
               (SELECT COUNT(*) FROM passes WHERE event_id = :event_id) as pass_count,
               (SELECT COUNT(*) FROM organisers WHERE event_id = :event_id) as organiser_count
        FROM events
        WHERE id = :event_id
        """,
        {
            "event_id": event_id
        }
    )
    return result.fetchone()

def update_event_data(event_id, title, extra_info = None, date = None):
    exec(
        """
        UPDATE events
        SET title = :title,
            date = :date,
            extra_info = :extra_info
        WHERE id = :event_id
        """,
        {
            "event_id": event_id,
            "title": title,
            "extra_info": extra_info,
            "date": date if date else None,
        }
    )
    commit()

def does_user_own_event(user_id, event_id):
    try:
        return get_event_info(event_id).user_id == user_id
    except:
        return False