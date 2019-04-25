# Asennusohje

## Sovelluksen asentaminen paikallisesti

Ennen sovelluksen käynnistämistä on siirryttävä venv-tilaan suorittamalla pääkansiossa komento `source venv/bin/activate`. Tämän jälkeen sovellus käynnistyy suorittamalla pääkansiossa `python run.py`. Tietokanta luodaan automaattisesti ja sovellus aukeaa osoitteeseen `localhost:5000`. Luodaksesi ensimmäisen käyttäjän valitse sovelluksen yläpalkista Login ja klikkaa avautuvalta sivulta "Register here!". Saat adminoikeudet luomalla käyttäjän jonka username on "admin", kaikki pienellä (name- ja password-kenttien sisällöillä ei ole väliä).

## Sovelluksen asentaminen Herokuun

Luo Heroku-repositorio, lisää sinne PostgreSQL-tietokanta komennolla `heroku addons:add heroku-postgresql:hobby-dev`, aseta ympäristömuuttuja HEROKU (`heroku config:set HEROKU=1`), ja committaa sovellus herokuun. Jatka avaamalla sovellus Herokussa ja luomalla sinne admin-tunnus kuten paikallisessa asennuksessa.

