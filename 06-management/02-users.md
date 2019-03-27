---
pageTitle: Managing Users
keywords: grakn, management, authentication, users
longTailKeywords: grakn managing users, grakn authentication, grakn users
Summary: User authentication in Grakn KGMS.
toc: false
---

## Managing Users [KGMS ONLY]
The ability to manage users and authenticate their access to the [keyspaces](../06-management/01-keyspace.md) of a Grakn Server running on the cloud, is limited to [KGMS](../05-cloud-deployment/01-kgms.md) users only. To do this, we first need to enter the `grakn console start`. We can then use the following commands to manage users and their credentials.

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