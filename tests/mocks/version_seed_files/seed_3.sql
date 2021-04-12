ALTER TABLE foods_seed ADD COLUMN user_id int;

ALTER TABLE foods_seed ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES users_seed (id) MATCH FULL;
