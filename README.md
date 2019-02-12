A test to automatically rotate service account keys on Google App Engine

Objectives:
- if *GOOGLE_APPLICATION_CREDENTIALS* is provided, use it
- otherwise, use the service account specifically created
to access the key hosted in a predefined folder on GCS
- ~~rotate a key synchronously~~
- ~~rotate multiple keys with a CRON configuration~~
- (cron) create a new key and set it as the default one (GCS)
- (cron) delete keys older than x days

### Required APIs
- IAM Service Account Credentials API: access token creation for service account to service account delegation
- Cloud Storage JSON API: get service account key stored on GCS
- Identity and Access Management (IAM) API: key rotation

### GCS access
read/write/delete on bucket

#### Initiate a global key rotation

HTTP GET @ `/tasks:initiateKeyRotation`

#### Initiate a global key cleanup

HTTP GET @ `/tasks:initiateKeyCleanup`

#### Synchronous key rotation

HTTP POST @ `/serviceAccounts/{service_account_id}/keys`

The service account id can either be the email or the unique id of the service account.

#### Synchronous key cleanup

HTTP POST @ `/serviceAccounts/{service_account_id}/keys:deleteObsoleteKeys`

The service account id can either be the email or the unique id of the service account.
