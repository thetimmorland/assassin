insert into user (id, is_active, email, name, location) values
    (1, true, 'user1@example.com', 'User 1', '1A'),
    (2, false, 'user2@example.com', 'User 2', '2A'),
    (3, true, 'user3@example.com', 'User 3', '3A'),
    (4, true, 'user4@example.com', 'User 4', '4A'),
    (5, false, 'user5@example.com', 'User 5', '5A');


insert into assassination (hunter_id, prey_id) values
    (1, 2),
    (1, 3),
    (3, 4);


insert into target_ring (user_id) values
    (1), (2), (3);
