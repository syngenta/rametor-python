INSERT INTO "public"."users_seed"("id","user","password")
VALUES
(1,E'paul',E'this-is-it');

INSERT INTO "public"."foods_seed"("id","name","calories","user_id")
VALUES
(1,E'pizza',E'100',1);
