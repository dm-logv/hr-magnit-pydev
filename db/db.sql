CREATE TABLE Regions (
  region_id     INTEGER PRIMARY KEY,
  region_name   TEXT
);

INSERT INTO Regions (region_name)
VALUES ('Краснодарский край'),
       ('Ростовская область'),
       ('Ставропольский край');

CREATE TABLE Cities (
  city_id     INTEGER PRIMARY KEY,
  region_id   INTEGER REFERENCES Regions(region_id),
  city_name   TEXT
);

INSERT INTO Cities (region_id, city_name)
VALUES ((SELECT region_id FROM Regions WHERE region_name =  'Краснодарский край'), 'Краснодар'),
       ((SELECT region_id FROM Regions WHERE region_name =  'Краснодарский край'), 'Кропоткин'),
       ((SELECT region_id FROM Regions WHERE region_name =  'Краснодарский край'), 'Славянск'),
       ((SELECT region_id FROM Regions WHERE region_name =  'Ростовская область'), 'Ростов'),
       ((SELECT region_id FROM Regions WHERE region_name =  'Ростовская область'), 'Шахты'),
       ((SELECT region_id FROM Regions WHERE region_name =  'Ростовская область'), 'Батайск'),
       ((SELECT region_id FROM Regions WHERE region_name = 'Ставропольский край'), 'Ставрополь'),
       ((SELECT region_id FROM Regions WHERE region_name = 'Ставропольский край'), 'Пятигорск'),
       ((SELECT region_id FROM Regions WHERE region_name = 'Ставропольский край'), 'Кисловодск');

CREATE TABLE Comments (
  comment_id  INTEGER PRIMARY KEY,
  last_name   TEXT,
  first_name  TEXT,
  patronymic  TEXT,
  region_id   INTEGER REFERENCES Regions(region_id),
  city_id     INTEGER REFERENCES Cities(city_id),
  phone       TEXT,
  email       TEXT,
  comment     TEXT
);