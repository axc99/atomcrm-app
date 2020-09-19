# Create lead

`POST` `https://atomcrm.herokuapp.com/api/<TOKEN HERE>/createLead`

Sample request body:
```json
{
   "statusId": 1,
   "tags": [
      "google_search",
      "form_2"
   ],
   "fields": [
      {
         "fieldId": 1,
         "value": "John"
      },
      {
         "fieldId": 2,
         "value": "john@gmail.com"
      }
   ],
   "utm_source": "google",
   "utm_medium": "cpc",
   "utm_campaign": "spring_sale",
   "utm_term": "running+shoes",
   "utm_content": "textlink"
}
```

Sample response body:
```json
{
   "lead": {
      "id": 1,
      "statusId": 1,
      "addDate": "2020-08-29 13:47:12",
      "updDate": "2020-08-29 13:47:12",
      "tags": [
         "google_search",
         "form_2"
      ],
      "fields": [
         {
            "fieldId": 1,
            "fieldName": "First name",
            "value": "John"
         },
         {
            "fieldId": 2,
            "fieldName": "Email",
            "value": "john@gmail.com"
         }
      ]
   },
   "utm_source": "google",
   "utm_medium": "cpc",
   "utm_campaign": "spring_sale",
   "utm_term": "running+shoes",
   "utm_content": "textlink"
}
```

# Get leads

`POST` `https://atomcrm.herokuapp.com/api/<TOKEN HERE>/getLeads`

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
         "statusId": 1,
         "addDate": "2020-08-29 13:47:12",
         "updDate": "2020-08-30 14:23:00",
         "tags": [
            "google_search",
            "form_2"
         ],
         "fields": [
            {
               "fieldId": 1,
               "fieldName": "First name",
               "value": "John"
            },
            {
               "fieldId": 2,
               "fieldName": "Email",
               "value": "john@gmail.com"
            }
         ],
         "utm_source": "google",
         "utm_medium": "cpc",
         "utm_campaign": "spring_sale",
         "utm_term": "running+shoes",
         "utm_content": "textlink"
      }
   ]
}
```

# Update lead

`POST` `https://atomcrm.herokuapp.com/api/<TOKEN HERE>/updateLead`

Sample request body:
```json
{
   "id": 1,
   "statusId": 2,
   "tags": [],
   "fields": [
      {
         "fieldId": 1,
         "value": "Andrew"
      },
      {
         "fieldId": 2,
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
         "statusId": 2,
         "addDate": "2020-08-29 13:47:12",
         "updDate": "2020-08-30 14:23:00",
         "tags": [],
         "fields": [
            {
               "fieldId": 1,
               "fieldName": "First name",
               "value": "Andrew"
            },
            {
               "fieldId": 2,
               "fieldName": "Email",
               "value": "andrew@gmail.com"
            }
         ]
      }
   ]
}
```
