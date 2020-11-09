# AtomCRM

Minimalistic CRM system with basic functionality.

[App on Nepkit Store](https://nepkit.com/store/1-nepkit-team/1-atomcrm)

```shell script
python manage.py runserver

# Compile JavaScript code with BabelJS (optional)
python manage.py compile
```

---

## Database

Creating the migration repository: 

`flask db init`

Creating the migration:

`flask db migrate`

Apply the migration to the database:

`flask db upgrade`

## Language localisation

Extract texts:

```pybabel extract -F babel.cfg -k _l -o strings.pot .```

Update exist catalog:

```pybabel update -i strings.pot -d flaskr/translations```

Compile catalog:

```pybabel compile -d flaskr/translations```

Create new catalog:
 
```pybabel init -i strings.pot -d flaskr/translations -l <LANG CODE HERE>```