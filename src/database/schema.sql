PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS games;
CREATE TABLE games(
    game_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    guesses_rem INTEGER DEFAULT 6 NOT NULL,
    word VARCHAR NOT NULL,
    guesses VARCHAR
);
DROP TABLE IF EXISTS users;
CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    UNIQUE(email)
);
INSERT INTO users(user_id, email, password) VALUES(1234, 'csuf.gmail.com', 'password');
INSERT INTO games(user_id, word, guesses) VALUES(1234, 'ccane', 'stray,mouse,chace');
INSERT INTO games(user_id, word, guesses) VALUES(1234, 'crane', 'ghoul,steer,debug,crane');
COMMIT;