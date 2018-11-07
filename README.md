A test to automatically rotate service account keys on Google App Engine

Objectives:
- if *GOOGLE_APPLICATION_CREDENTIALS* is provided, use it
- otherwise, use the service account specifically created
to access the key hosted in a predefined folder on GCS
- rotate the key with a CRON configuration
