---
pageTitle: Managing Users
keywords: typedb, management, authentication, users
longTailKeywords: typedb managing users, typedb authentication, typedb users
Summary: User authentication in TypeDB Cluster.
toc: false
---

## Managing Users [TypeDB Cluster ONLY]
The ability to manage users and authenticate their access to [databases](../06-management/01-database.md) is limited to TypeDB Cluster and is not available in TypeDB.

In order to manage users, we first need to enter the TypeDB User Management Console by running `typedb user-management`. We can then use the following commands to manage user authentication.

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
