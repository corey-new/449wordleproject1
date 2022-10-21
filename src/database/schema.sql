PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS games;
CREATE TABLE games(
    game_id INTEGER PRIMARY KEY NOT NULL,
    user_id VARCHAR NOT NULL,
    guesses_rem INTEGER DEFAULT 6 NOT NULL,
    word VARCHAR NOT NULL,
    guesses VARCHAR,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
DROP TABLE IF EXISTS users;
CREATE TABLE users(
    user_id VARCHAR PRIMARY KEY NOT NULL,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
);
DROP TABLE IF EXISTS guesses;
CREATE TABLE guesses(
    guess_id INTEGER PRIMARY KEY NOT NULL,
    game_id INTEGER NOT NULL,
    guess VARCHAR NOT NULL,
    guess_num INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

INSERT INTO users(user_id, username, password) VALUES(1234, 'user1', 'password');
INSERT INTO games(user_id, word) VALUES(1234, 'ccane');
INSERT INTO games(user_id, word) VALUES(1234, 'crane');
COMMIT;
