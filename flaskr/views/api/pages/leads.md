## Create lead

### Sample request:

```
POST https://atomcrm.nepkit.team/api/v1/leads
```

```
Authorization: Basic <YOUR TOKEN>
Content-Type: application/json
```
```json
{
   "statusId": 1,
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
   "tags": ["google_search", "form_2"],
   "amount": 25.45,   
   "utmSource": "google",
   "utmMedium": "cpc",
   "utmCampaign": "spring_sale",
   "utmTerm": "running+shoes",
   "utmContent": "textlink"
}
```

### Sample response:

```json
{
   "lead": {
      "uid": "A1B2C345",
      "statusId": 1,
      "addDate": "2020-08-29 13:47:12",
      "updDate": "2020-08-29 13:47:12",
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
      "tags": ["google_search", "form_2"]
   },
   "amount": 25.45,
   "utmSource": "google",
   "utmMedium": "cpc",
   "utmCampaign": "spring_sale",
   "utmTerm": "running+shoes",
   "utmContent": "textlink"
}
```

---------

## Get leads

### Sample request:

```
GET https://atomcrm.nepkit.team/api/v1/leads/A1B2C345
```

```
Authorization: Basic <YOUR TOKEN>
```

### Sample response:

```json
{
   "leads": [
      {
         "uid": "A1B2C345",
         "statusId": 1,
         "addDate": "2020-08-29 13:47:12",
         "updDate": "2020-08-30 14:23:00",
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
         "tags": ["google_search", "form_2"],
         "completedTasks": [1, 2],
         "amount": 25.45,
         "utmSource": "google",
         "utmMedium": "cpc",
         "utmCampaign": "spring_sale",
         "utmTerm": "running+shoes",
         "utmContent": "textlink"
      }
   ]
}
```

---------

## Update lead

### Sample request:

```
PATCH https://atomcrm.nepkit.team/api/v1/leads/<LEAD ID>
```

```
Authorization: Basic <YOUR TOKEN>
Content-Type: application/json
```

```json
{
   "statusId": 2,
   "fields": [
      {
         "fieldId": 1,
         "value": "Andrew"
      },
      {
         "fieldId": 2,
         "value": "andrew@gmail.com"
      }
   ],
   "tags": [],
   "completedTasks": [2, 3],
   "amount": 105
}
```

### Sample response:

```json
{
   "leads": [
      {
         "uid": "A1B2C345",
         "statusId": 2,
         "addDate": "2020-08-29 13:47:12",
         "updDate": "2020-08-30 14:23:00",
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
         ],
         "tags": [],
         "completedTasks": [2, 3],
         "amount": 105
      }
   ]
}
```
