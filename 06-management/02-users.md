---
pageTitle: Managing Users
keywords: grakn, management, authentication, users
longTailKeywords: grakn managing users, grakn authentication, grakn users
Summary: User authentication in Grakn Cluster.
toc: false
---

## Managing Users [Grakn Cluster ONLY]
The ability to manage users and authenticate their access to [keyspaces](../06-management/01-keyspace.md) is limited to Grakn Cluster and is not available in Grakn Core.

In order to manage users, we first need to enter the Grakn User Management Console by running `grakn user-management`. We can then use the following commands to manage user authentication.

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
