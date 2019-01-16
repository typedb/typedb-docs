---
sidebarTitle: Users
pageTitle: Managing Users
permalink: /docs/management/users
toc: false
---

## Managing Users [KGMS ONLY]
The ability to manage users and authenticate their access to the [keyspaces](/docs/management/keyspace) of a Grakn Server running on the cloud, is limited to [KGMS](/docs/cloud-deployment/kgms) users only. To do this, we first need to enter the `grakn console start`. We can then use the following commands to manage users and their credentials.

### Create a new user
```
CREATE USER username WITH PASSWORD user-password
```

### Update a user
```
UPDATE USER username WITH PASSWORD new-password
```

### Retrieve all users
```
LIST USERS
```

### Retrieve one user
```
GET USER username
```

### Delete a user
```
DELETE USER username
```