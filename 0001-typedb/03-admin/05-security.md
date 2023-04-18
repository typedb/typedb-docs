---
pageTitle: Security features
keywords: typedb, security, auth, authentication, encryption, vulnerability
longTailKeywords: TypeDB security, user authentication, data encryption
summary: TypeDB high availability guarantees and solution.
toc: false
---

# Security features

<div class="note">
[Note]
Most of the security features are available only in TypeDB Cloud.
</div>

## Access control

<div class="note">
[Note]
Access control features are a part of TypeDB Cloud.
</div>

TypeDB Cloud has the following security features:

* [Discretionary access control](https://en.wikipedia.org/wiki/Discretionary_access_control),
* User account management,
* User identification and authentication,
* Password hashing with salt,
* Password complexity requirements settings.

### User authentication

All external connections to a cluster of TypeDB Cloud require user account credentials. Not for a user account 
used in the TypeDB Cloud web portal but a user account from the TypeDB Cloud cluster we are connecting to.

Users can use usernames and passwords to identify and authenticate themselves. Passwords are stored only as 
irreversible **password hash + salt**.

Administrators can adjust settings for **password strength requirements** and reset users passwords.

### User management

<div class="note">
[Note]
User management features are a part of TypeDB Cloud.
</div>

Use [TypeDB Console](../../02-clients/02-console.md) or Client API to manage users. To connect to TypeDB with TypeDB 
Console provide a username and password (when prompted):

<!-- test-ignore -->
```bash
typedb console --cluster=<address> --username=<username> --password
```

After issuing this command we will be prompted to provide a password.

<div class="note">
[Important]
Only the administrator account (username `admin`) can perform user management actions.
</div>

Use the following TypeDB Console commands to manage users.

Retrieve a list of all users:

<!-- test-ignore -->
```bash
user list
```

Create a new user:

<!-- test-ignore -->
```bash
user create <username>
```

Set password for a user:

<!-- test-ignore -->
```bash
user set-password <username> 
```

Updating your own password:

<!-- test-ignore -->
```bash
user update-password
```

Delete a user:

<!-- test-ignore -->
```bash
user delete <username>
```

## Encryption

TypeDB Cloud encrypts all network traffic: 

* TLS encryption is used for client/server communication.
* CurveZMQ is used for cluster communication (TypeDB Cloud only).

## Cluster security

TypeDB Cloud cluster accepts external communications only with valid credentials and internal cluster communications 
only from servers that are set to be part of the cluster.

All external and internal communications are [encrypted](#encryption) on the fly. 

Set a CA certificate explicitly to be able to use a self-signed certificate or to avoid using 
default certificates from an operating system.
If no certificate is provided then the default operating system root certificates will be used to establish TLS 
encryption. 
