A test to automatically rotate service account keys on Google App Engine

Objectives:
- if *GOOGLE_APPLICATION_CREDENTIALS* is provided, use it
- otherwise, use the service account specifically created
to access the key hosted in a predefined folder on GCS
- rotate a key synchronously
- rotate multiple keys with a CRON configuration

#### Synchronous key rotation

HTTP POST @ `/serviceAccounts/{service_account_id}/keys/{key_id}:rotate'

The service account id can either be the email or the unique id of the service account.
