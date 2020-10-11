# AtomCRM

Minimalistic CRM system with basic functionality.

[App on Veokit Store](https://veokit.com/store/1-veokit-team/1-atomcrm)

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

Create catalog:
 
```pybabel init -i strings.pot -d flaskr/translations -l en```

Update exist catalog:

```pybabel update -i strings.pot -d flaskr/translations```

Compile catalog:

```pybabel compile -d flaskr/translations```