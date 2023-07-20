CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    account_type VARCHAR(20) NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(80) NOT NULL UNIQUE,
    pw_hash VARCHAR(80) NOT NULL
);


INSERT INTO users (account_type, username, email, pw_hash) VALUES (
    'producer',
    'alex the producer',
    'alex@alex.com',
    'fdafsd89f7asd98f7'
),
(
    'producer',
    'peter the producer',
    'peter@peter.com',
    '897asdf897asdf789asdf'
),
(
    'emcee',
    'jenny the emcee',
    'jenny@jenny.com',
    'asdfjkhasdfkjlhasdf88'
);

CREATE TABLE Beats (
    id SERIAL PRIMARY KEY,
    track_name VARCHAR(100) NOT NULL,
    uploaded_time TEXT NOT NULL,
    sc_id VARCHAR(50) NOT NULL,
    likes INTEGER NOT NULL,
    CONSTRAINT fk_user_id
        FOREIGN KEY(user_id)
        REFERENCES users(id)
);

/**------------------------------------------------------------------------
 *                           INITIALIZE DATA
 *------------------------------------------------------------------------**/

 INSERT INTO users (account_type, username, email, pw_hash) VALUES (
    'producer',
    'alex the producer',
    'alex@alex.com',
    'fdafsd89f7asd98f7'
),
(
    'producer',
    'peter the producer',
    'peter@peter.com',
    '897asdf897asdf789asdf'
),
(
    'emcee',
    'jenny the emcee',
    'jenny@jenny.com',
    'asdfjkhasdfkjlhasdf88'
);