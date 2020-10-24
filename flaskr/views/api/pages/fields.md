## Get fields

For getting all fields do not pass `id` field.

`POST https://veokit.team/atomcrm/api/<TOKEN HERE>/getFields`

Sample request body:
```json
{
  "id": [1, 2]
}
```

Sample response body:
```json
[
  {
    "id": 1,
    "name": "First name",
    "min": 0,
    "max": 30,
    "asTitle": true,
    "primary": false
  },
  {
    "id": 2,
    "name": "Mobile phone",
    "min": 0,
    "max": 50,
    "asTitle": false,
    "primary": false
  }
]
```