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
    "valueType": "string"
  },
  {
    "id": 2,
    "name": "Mobile phone",
    "valueType": "number"
  }
]
```