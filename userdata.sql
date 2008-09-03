-- All the tables for user data 

CREATE TABLE users(
    id serial primary key,
    password varchar(256),
    
    prefix varchar(5),
    lname varchar(30),
    fname varchar(30),
    email varchar(320) UNIQUE, -- max allowed email length.
    addr1 varchar(64),
    addr2 varchar(64),
    city varchar(64),
    zip5 varchar(5),
    zip4 varchar(4),
    phone varchar(10),
    
    verified boolean default false, -- done verified activity at least once
);

CREATE TABLE petition(
    id varchar(256) primary key,
    title text,
    description text,
    owner_id int references users,
    created timestamp default now(),
    deleted timestamp 
);

CREATE TABLE signatory(
    id serial primary key, 
    user_id int references users,
    petition_id varchar(256) references petition,
    share_with char(1), -- E=everybody, A=author of petition, N=nobody
    comment text,
    signed timestamp default now(),
    deleted timestamp,
    UNIQUE (user_id, petition_id)
);

CREATE TABLE petition_responses(
    id serial primary key,
    sign_id int references signatory,
    response text,
    category char(1), --S=support, O=oppose, U=undecided, N=No answer
    received timestamp
);

-- save contacts imported from yahoo, google etc.,
-- emails can be 64+1+255 char 
CREATE TABLE contacts(
    user_id int references users,
    uemail VARCHAR(320),
    cemail VARCHAR(320),
    cname VARCHAR(80),
    provider VARCHAR(20),
    UNIQUE(user_id, uemail, cemail)
);

GRANT ALL ON users TO watchdog;
GRANT ALL ON users_id_seq TO watchdog;
GRANT ALL ON petition TO watchdog;
GRANT ALL ON signatory TO watchdog;
GRANT ALL ON contacts TO watchdog;
