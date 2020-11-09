## Create lead

`POST https://nepkit.team/atomcrm/api/<TOKEN HERE>/createLead`

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
   "utmSource": "google",
   "utmMedium": "cpc",
   "utmCampaign": "spring_sale",
   "utmTerm": "running+shoes",
   "utmContent": "textlink"
}
```

Sample response body:
```json
{
   "lead": {
      "uid": "A1B2C345",
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
   "utmSource": "google",
   "utmMedium": "cpc",
   "utmCampaign": "spring_sale",
   "utmTerm": "running+shoes",
   "utmContent": "textlink"
}
```

## Get leads

`POST https://nepkit.team/atomcrm/api/<TOKEN HERE>/getLeads`

Sample request body:
```json
{
   "uid": ["A1B2C345"]
}
```

Sample response body:
```json
{
   "leads": [
      {
         "uid": "A1B2C345",
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
         "utmSource": "google",
         "utmMedium": "cpc",
         "utmCampaign": "spring_sale",
         "utmTerm": "running+shoes",
         "utmContent": "textlink"
      }
   ]
}
```

## Update lead

`POST https://nepkit.team/atomcrm/api/<TOKEN HERE>/updateLead`

Sample request body:
```json
{
   "uid": "A1B2C345",
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
         "uid": "A1B2C345",
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
