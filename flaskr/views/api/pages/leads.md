# Create lead

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/createLead`

Sample request body:
```json
{
  "status_id": 1,
  "tags": ["google_search", "form_2"],
  "fields": [
    {
      "field_id": 1,
      "value": "John"
    },
    {
      "field_id": 2,
      "value": "john@gmail.com"
    },
    {
      "field_id": 3,
      "value": "+1 (123) 123-45-67"
    }
  ]
}
```

Sample response body:
```json
{
  "id": 1
}
```

# Get leads

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/getLeads`

Sample request body:
```json
{
  "id": [1]
}
```

Sample response body:
```json
[
    {
        "id": 1,
        "status_id": 1,
        "tags": ["google_search", "form_2"],
        "fields": [
            {
                "field_id": 1,
                "value": "John"
            },
            {
                "field_id": 2,
                "value": "john@gmail.com"
            },
            {
                "field_id": 3,
                "value": "+1 (123) 123-45-67"
            }
        ]    
    }
]
```

# Update lead

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/updateLead`

Sample request body:
```json
{
  "id": 1,
  "tags": [],
  "fields": [
    {
      "field_id": 1,
      "value": "Andrew"
    },
    {
      "field_id": 2,
      "value": "andrew@gmail.com"
    }
  ]
}
```

# Archive lead (delete)

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/archiveLead`

Sample request body:
```json
{
  "id": 3
}
```