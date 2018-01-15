CREATE TABLE rpg_users (
    username text PRIMARY KEY, 
    password text, 
    auth_hostmask text, 
    auth_timestamp text,
    xp integer default 0
);

CREATE TABLE rpg_characters (
    character_name text PRIMARY KEY,
    username text REFERENCES rpg_users (username) DEFAULT NULL
);

CREATE TABLE rpg_items (
    item_name text PRIMARY KEY
);

CREATE TABLE rpg_item_ledger (
    ledger_id integer PRIMARY KEY,
    item_name text REFERENCES rpg_items (item_name) NOT NULL,
    previous_ledger_id integer REFERENCES rpg_item_ledger (ledger_id) DEFAULT NULL,
    next_ledger_id integer REFERENCES rpg_item_ledger (ledger_id) DEFAULT NULL,
    character_name text REFERENCES rpg_characters (character_name) NOT NULL
);

