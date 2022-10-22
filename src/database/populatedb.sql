BEGIN TRANSACTION;
INSERT INTO users(user_id, username, password) VALUES('123abc', 'user1', 'password');   --user_id shortened for ease of use.  actual application will use longer user_ids
INSERT INTO games(user_id, word) VALUES('123abc', 'abbey'); --double letter example
INSERT INTO games(user_id, word) VALUES('123abc', 'crane'); --second game added. 
COMMIT;