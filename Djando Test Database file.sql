
"""Here Created Database Tables """
CREATE TABLE client (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    name VARCHAR(100),
    description TEXT,
    FOREIGN KEY (client_id) REFERENCES client(id)
);

CREATE TABLE project_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
