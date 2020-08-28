# Get fields

For getting all fields do not pass `id` field.

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/getFields`

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
    "as_title": true,
    "primary": false
  },
  {
    "id": 2,
    "name": "Mobile phone",
    "min": 0,
    "max": 50,
    "as_title": false,
    "primary": false
  }
]
```