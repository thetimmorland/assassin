create table item (
    id integer primary key,
    name text not null,
    date text not null default current_timestamp
);
