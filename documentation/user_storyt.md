# Valmis toiminnallisuus

- Käyttäjä pystyy luomaan tunnuksen (`INSERT INTO Account (name, username, password) VALUES (:name, :username, :password)`)
- Käyttäjä pystyy kirjautumaan sisään (`SELECT * FROM Account WHERE Account.username = :username AND Account.password = :password`)
- Käyttäjä pystyy näkemään profiilinsa tiedot (`SELECT * FROM Account WHERE Account.id = :account_id`)
- Käyttäjä pystyy muokkaamaan profiilinsa tietoja (`UPDATE Account SET name = :name, username = :username, password = :password WHERE Account.id = :account_id`)
- Käyttäjä pystyy näkemään listan projekteistaan (`SELECT * FROM Project, UserProject WHERE UserProject.account_id = :account_id AND UserProject.project_id = Project.id`)
- Käyttäjä pystyy luomaan uuden projektin (`INSERT INTO Project (name, complete, deadline, invite_token, creator) VALUES (:name, :complete, :deadline, :invite_token, :account_id)`)
- Käyttäjä pystyy näkemään projektin tiedot (`SELECT * FROM Project WHERE Project.id = :project_id`)
- Käyttäjä pystyy muokkaamaan projektia (`UPDATE Project SET name = :name, deadline = :deadline WHERE Project.id = :project_id`)
- Käyttäjä pystyy poistamaan projektin (`DELETE FROM Task WHERE Task.project_id = :project_id`, `DELETE FROM Category WHERE Category.project_id = :project_id`, `DELETE FROM Project WHERE Project.id = :project_id`)
- Käyttäjä pystyy luomaan projektille kategorian (`INSERT INTO Category (name, project_id) VALUES (:name, :project_id)`)
- Käyttäjä pystyy muokkaamaan kategoriaa (`UPDATE Category SET name = :name WHERE Category.id = :category_id`)
- Käyttäjä pystyy poistamaan kategorian (`DELETE FROM Task WHERE Task.category_id = :category_id`, `DELETE FROM Category WHERE Category.id = :category_id`)
- Käyttäjä pystyy luomaan kategoriaan tehtävän (`INSERT INTO Task (name, complete, deadline, project_id, category_id) VALUES (:name, :complete, :deadline, :project_id, :category_id)`)
- Käyttäjä pystyy merkitsemään tehtävän tehdyksi / ei-tehdyksi (`UPDATE Task SET Complete = :complete WHERE Task.id = :task_id`)
- Käyttäjä pystyy muokkaamaan tehtäviä (`UPDATE Task SET name = :name, deadline = :deadline WHERE Task.id = :task_id`)
- Käyttäjä pystyy poistamaan tehtävän (`DELETE FROM Task WHERE Task.id = :task_id`)
- Käyttäjä pystyy näkemään listan luomistaan projekteista, joiden deadline on tänään (`SELECT * FROM Project WHERE Project.creator = :account_id AND Project.complete = 0 AND Project.deadline = :today_date`)
- Käyttäjä pystyy näkemään listan luomistaan projekteista, joiden yhdenkin tehtävän deadline on tänään (`SELECT * FROM Project LEFT JOIN Task ON Task.project_id = Project.id WHERE (Task.deadline = :today_date AND Project.creator = :account_id AND NOT Task.complete) GROUP BY Project.id`)
- Käyttäjä pystyy liittymään projektiin kutsulinkillä (`SELECT Project.id FROM Project WHERE Project.invite_token = :invite_token`, `INSERT INTO UserProject (account_id, project_id) VALUES (:account_id, :project_id)`)

