CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
);
