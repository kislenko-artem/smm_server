--split
CREATE TABLE IF NOT EXISTS profile_count
(
    id INTEGER
    constraint profile_count_pk
    primary key autoincrement,
    profile_id INTEGER not null,
    dt_create INTEGER default (datetime('now', 'unixepoch')),
    count int not null
    );
--split
CREATE UNIQUE INDEX IF NOT EXISTS profile_count_id_uindex
    on profile_count (id);
--split
CREATE TABLE IF NOT EXISTS "profiles"
(
    id INTEGER
    constraint profiles_pk
    primary key autoincrement,
    name TEXT not null,
    profile_type INTEGER not null,
    ident TEXT not null
);
--split
CREATE TABLE IF NOT EXISTS vk_groups
(
    id INTEGER
    constraint vk_groups_pk
    primary key autoincrement,
    name TEXT not null,
    ident INTEGER not null,
    screen_name TEXT not null,
    photo_50 TEXT
);
--split
CREATE TABLE IF NOT EXISTS business_categories
(
    id INTEGER
        constraint business_categories_pk
            primary key autoincrement,
    name TEXT not null,
    category_type TEXT not null
);
--split
CREATE TABLE IF NOT EXISTS business_clients
(
    id INTEGER
        constraint business_clients_pk
            primary key autoincrement,
    name TEXT not null,
    phone TEXT DEFAULT null,
    email TEXT DEFAULT null,
    comments TEXT DEFAULT null,
    dt_create INTEGER default (datetime('now', 'unixepoch')),
    age INTEGER DEFAULT Null,
    dt_appearance INTEGER DEFAULT Null,
    business_categories_id INTEGER DEFAULT Null,
    note INTEGER DEFAULT Null
);
--split
CREATE TABLE IF NOT EXISTS business_income
(
    id INTEGER
        constraint business_income_pk
            primary key autoincrement,
    price REAL DEFAULT 0,
    business_clients_id INTEGER DEFAULT null,
    business_categories_id INTEGER not null,
    comments TEXT DEFAULT null,
    duration REAL DEFAULT null,
    dt_provision INTEGER default (datetime('now', 'unixepoch')),
    dt_create INTEGER default (datetime('now', 'unixepoch'))
);
ALTER TABLE business_clients RENAME COLUMN note TO business_subcategories_id;
--split
UPDATE business_clients SET business_subcategories_id = NULL;
--split
ALTER TABLE business_income ADD COLUMN business_subcategories_id INTEGER DEFAULT null;
--split
CREATE TABLE IF NOT EXISTS business_subcategories
(
    id INTEGER
        constraint business_subcategories_pk
            primary key autoincrement,
    name TEXT not null,
    business_category_id INTEGER not null
);
--split
CREATE TABLE business_offices (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT
);
--split
INSERT INTO business_offices
(name)
VALUES('Лаборатория');
--split
INSERT INTO business_offices
(name)
VALUES('Витебский');
--start: