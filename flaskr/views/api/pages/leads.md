# Create lead

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/createLead`

Sample request body:
```json
{
   "status_id": 1,
   "tags": [
      "google_search",
      "form_2"
   ],
   "fields": [
      {
         "field_id": 1,
         "value": "John"
      },
      {
         "field_id": 2,
         "value": "john@gmail.com"
      }
   ]
}
```

Sample response body:
```json
{
   "lead": {
      "id": 1,
      "status_id": 1,
      "add_date": "2020-08-29 13:47:12",
      "upd_date": "2020-08-29 13:47:12",
      "tags": [
         "google_search",
         "form_2"
      ],
      "fields": [
         {
            "field_id": 1,
            "field_name": "First name",
            "value": "John"
         },
         {
            "field_id": 2,
            "field_name": "Email",
            "value": "john@gmail.com"
         }
      ]
   }
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
{
   "leads": [
      {
         "id": 1,
         "status_id": 1,
         "add_date": "2020-08-29 13:47:12",
         "upd_date": "2020-08-30 14:23:00",
         "tags": [
            "google_search",
            "form_2"
         ],
         "fields": [
            {
               "field_id": 1,
               "field_name": "First name",
               "value": "John"
            },
            {
               "field_id": 2,
               "field_name": "Email",
               "value": "john@gmail.com"
            }
         ]
      }
   ]
}
```

# Update lead

`POST` `https://atomcrm.herokuapp.com/api/<YOUR TOKEN HERE>/updateLead`

Sample request body:
```json
{
   "id": 1,
   "status_id": 2,
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

Sample response body:
```json
{
   "leads": [
      {
         "id": 1,
         "status_id": 2,
         "add_date": "2020-08-29 13:47:12",
         "upd_date": "2020-08-30 14:23:00",
         "tags": [],
         "fields": [
            {
               "field_id": 1,
               "field_name": "First name",
               "value": "Andrew"
            },
            {
               "field_id": 2,
               "field_name": "Email",
               "value": "andrew@gmail.com"
            }
         ]
      }
   ]
}
```
