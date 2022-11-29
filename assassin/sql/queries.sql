-- name: get-all-users
select * from user;


-- name: get-user^
select * from user where id = :id;


-- name: get-user-by-email^
select * from user where email = :email;


-- name: create-user<!
insert into user (email, name, location)
values (:email, :name, :location);


-- name: set-user-is-active<!
update user
set is_active = :is_active
where id = :id;


-- name: update-targets#
delete from target_ring;

insert into target_ring
    (user_id)
select
    user.id as user_id
from user
where user.is_active
order by random();


-- name: create-assassination<!
insert into assassination
    (hunter_id, prey_id)
select
    hunter_id, prey_id
from target
where target.prey_id == :prey_id;


-- name: get-home-data^
select
    u.is_active,
    case
        when h.id is null then false
        else true end
    as has_hunter,
    p.name as prey_name,
    p.location as prey_location
from
    user as u
left join target as u_to_h
    on u_to_h.prey_id = u.id
left join target as u_to_p
    on u_to_p.hunter_id = u.id
left join user as h
    on u_to_h.hunter_id = h.id
left join user as p
    on u_to_p.prey_id = p.id
where
    u.id = :id;


-- name: get-leaderboard-data
select
    user.name as name,
    user.location as location,
    count(assassination.id) as score
from user
left join assassination
on user.id = assassination.hunter_id
group by user.id
order by score desc;
