# AtomCRM

Minimalistic CRM system with basic functionality.

[App on VeoKit Store](https://veokit.com/store/1-veokit-team/1-atomcrm)

---

# Database

Creating the migration repository: 

`flask db init` | `docker-compose run web flask db init`

Creating the migration:

`flask db migrate` | `docker-compose run web flask db migrate`

Apply the migration to the database:

`flask db upgrade` | `docker-compose run web flask db upgrade`
