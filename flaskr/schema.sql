-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS test_plan;
DROP TABLE IF EXISTS test_case;
DROP TABLE IF EXISTS test_procedure;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

create table test_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);

create table test_case (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_plan_id integer not null,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    qualification_criteria TEXT NOT NULL,
    FOREIGN KEY (test_plan_id) REFERENCES test_plan (id)
);

create table test_procedure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_case_id integer not null,
    content TEXT NOT NULL,
    foreign key (test_case_id) REFERENCES test_case (id)
);

create table test_result (
    id INTEGER PRIMARY KEY AUTOINCREMENT,


    confirmed integer not null,
    filepath text not null,
    foreign key (test_procedure_id) references test_procedure(id)
)