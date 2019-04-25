# Tietokannan rakenne

Tiedostossa `tietokantakaavio.png` kaavio tietokannan rakenteesta. Tietokanta on normalisoitu.

## Tietokannan taulut

### Account

Kuvaa sovelluksen käyttäjätunnusta.

```
CREATE TABLE Account (
  id INTEGER NOT NULL,
  name VARCHAR(144) NOT NULL,
  username VARCHAR(144) NOT NULL,
  password VARCHAR(144) NOT NULL,
  PRIMARY KEY (id)
)
```

### Role

Kuvaa sovelluksen käyttäjän roolia.

```
CREATE TABLE Role (
  id INTEGER NOT NULL,
  name VARCHAR(144) NOT NULL,
  account_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY (account_id) REFERENCES Account(id)
)
```

### Project

Kuvaa projektia.

```
CREATE TABLE Project (
  id INTEGER NOT NULL,
  name VARCHAR(144) NOT NULL,
  complete BOOLEAN NOT NULL,
  deadline DATE NOT NULL,
  invite_token INTEGER NOT NULL,
  creator INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (creator) REFERENCES Account(id)
)
```


### UserProject

Kuvaa käyttäjän ja projektin välistä yhteyttä.

```
CREATE TABLE UserProject (
  account_id INTEGER NOT NULL,
  project_id INTEGER NOT NULL,
  PRIMARY KEY (account_id, project_id),
  FOREIGN KEY (account_id) REFERENCES Account(id),
  FOREIGN KEY (project_id) REFERENCES Project(id)
)
```

### Category

Kuvaa tehtäväkategoriaa.

```
CREATE TABLE Category (
  id INTEGER NOT NULL,
  name VARCHAR(144) NOT NULL,
  project_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (project_id) REFERENCES Project(id)
)
```

### Task

Kuvaa yksittäistä tehtävää kategoriassa.

```
CREATE TABLE Task (
  id INTEGER NOT NULL,
  name VARCHAR(144) NOT NULL,
  complete BOOLEAN NOT NULL,
  deadline DATE NOT NULL,
  project_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (project_id) REFERENCES Project(id),
  FOREIGN KEY (category_id) REFERENCES Category(id)
)
```

