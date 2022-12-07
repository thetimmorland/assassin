-- name: get-items
select * from item;

-- name: get-item^
select * from item where id == :id;

-- name: create-item<!
insert into item(name)
values (:name);

--name: update-item<!
update item
set
    name = :name
where id = :id;

-- name: delete-item<!
delete from item where id = :id;
