---
title: Authentication
keywords:
tags: []
summary:
permalink: /docs/management/authentication
---

## Managing Users and Authenticatin [KGMS only]
The ability to authenticate access to the [keyspaces](/docs/management/keyspace) of a Grakn Server running on the cloud, is limited to [KGMS]() users. To do this, we need to first enter the `grakn console`
We can then use the following commands to manage users and their credentials.

### Creating a new user
```
CREATE USER username WITH PASSWORD user-password WITH ROLE admin
```

### Updating a user
```
UPDATE USER username WITH PASSWORD new-password
```

### Retrieving all users
```
LIST USERS
```

### Retrieving one user
```
GET USER username
```

### Deleing a user
```
DELETE USER username
```