INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('admin', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('post without image 1', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 2', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 3', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 4', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 5', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 6', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 7', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 8', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 9', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 10', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00'),
  ('post without image 11', 'test' || x'0a' || 'body without image', 1, '2019-01-01 00:00:00');

INSERT INTO tag (name) VALUES 
('test'), ('dhaka'), ('blog'), ('new'), ('python'), ('flask');

INSERT INTO post_tag (tag_id, entity_id) 
VALUES
(1, 1), 
(1, 2), 
(1, 3), 
(2, 1), 
(3, 1), 
(4, 1), 
(5, 4), 
(6, 5), 
(2, 6);