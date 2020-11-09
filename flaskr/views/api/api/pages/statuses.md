## Get statuses

For getting all statuses do not pass `id` field.

`POST https://nepkit.team/atomcrm/api/<TOKEN HERE>/getStatuses`

Sample request body:
```json
{
  "id": [1, 2, 3]
}
```

Sample response body:
```json
[
  {
    "id": 1,
    "index": 0,
    "name": "To Do"
  },
  {
    "id": 2,
    "index": 1,
    "name": "Doing"
  },
  {
    "id": 3,
    "index": 2,
    "name": "Done"
  }
]
```