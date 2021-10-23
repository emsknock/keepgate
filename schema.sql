CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    username    TEXT UNIQUE NOT NULL,
    passhash    TEXT NOT NULL,
    ON DELETE CASCADE
);

CREATE TABLE events (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users NOT NULL,
    title       TEXT NOT NULL, -- Title of the event shown on all tickets
    extra_info  TEXT, -- Extra info shown on all tickets
    date        TIMESTAMP WITH TIME ZONE -- Date shown on all tickets,
    ON DELETE CASCADE
);

CREATE TABLE tickets (
    id          UUID PRIMARY KEY,
    event_id    INTEGER REFERENCES events NOT NULL,
    user_id     INTEGER REFERENCES users, -- Only set if requires login to display
    extra_info  TEXT, -- Extra info shown only for specific ticket
    stamped     BOOLEAN NOT NULL DEFAULT FALSE, -- Set true on first scan
    stamped_at  TIMESTAMP WITH TIME ZONE,
    stamped_by  INTEGER REFERENCES users,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE passes (
    id          UUID PRIMARY KEY,
    event_id    INTEGER REFERENCES events NOT NULL,
    user_id     INTEGER REFERENCES users, -- Only set if requires login to display
    value       INTEGER DEFAULT 0,
    extra_info  TEXT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ON DELETE CASCADE
);

CREATE TABLE organisers (
    id          SERIAL PRIMARY KEY,
    event_id    INTEGER REFERENCES events,
    user_id     INTEGER REFERENCES users,
    UNIQUE (event_id, user_id),
    --can_create  BOOLEAN, -- Can create tickets and passes
    --can_delete  BOOLEAN, -- Can remove tickets and passes
    can_stamp   BOOLEAN,   -- Can mark tickets as stamped
    --can_unstamp BOOLEAN, -- Can undo stamps on tickets
    can_topup   BOOLEAN,   -- Can add value to passes
    can_deduct  BOOLEAN    -- Can reduce value from passes
);

CREATE TABLE pass_transactions (
    id          SERIAL PRIMARY KEY,
    pass_id     UUID REFERENCES passes,
    user_id     INTEGER REFERENCES users,
    value       INTEGER,
    time        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);