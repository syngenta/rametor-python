ALTER TABLE foods_a ADD COLUMN user_id int;

ALTER TABLE foods_a ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users_a (id) MATCH FULL;
