INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('admin', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, image_path, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 'test_image.jpg', 1, '2018-01-01 00:00:00');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('post without image', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00');

INSERT INTO reaction (name, user_id, entity_id) 
VALUES 
("like", 1, 1), 
("like", 2, 1), 
("like", 3, 1), 
("unlike", 1, 1), 
("unlike", 2, 1);