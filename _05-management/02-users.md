---
sidebarTitle: Users
pageTitle: Managing Users
summary:
permalink: /docs/management/users
---

## Managing Users [KGMS only]
The ability to manage users and authenticate their access to the [keyspaces](/docs/management/keyspace) of a Grakn Server running on the cloud, is limited to [KGMS](/docs/cloud-deployment/kgms) users only. To do this, we first need to enter the `grakn console start`. We can then use the following commands to manage users and their credentials.

### Creating a new user
```
CREATE USER username WITH PASSWORD user-password
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