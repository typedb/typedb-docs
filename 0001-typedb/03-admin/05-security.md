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

All external connections to a cluster of TypeDB Cloud require a user account credentials. Not for a user account 
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
Console provide a username and password:

<!-- test-ignore -->
```bash
typedb console --cluster=<address> --username=<username> --password=<password>
```

<div class="note">
[Important]
Use the Administrators account to be able to manage users.
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
user create <username> <password>
```

Delete a user:

<!-- test-ignore -->
```bash
user delete <username>
```

## Encryption

TypeDB and TypeDB Cloud encrypts all network traffic: 

* TLS encryption is used for client/server communication.
* CurveZMQ is used for cluster communication (TypeDB Cloud only).

## Cluster security

TypeDB Cloud cluster accepts external communications only with valid credentials and internal cluster communications 
only from servers that are set to be part of the cluster.

All external and internal communications are [encrypted](#encryption) on the fly. 

Additional connection security is achieved by using a CA certificate in the TLS encryption of Clients connections 
(optional). 

If no certificate is provided then the default operating system root certificates will be used to establish TLS 
encryption. Set the certificate explicitly to be able to use a self-signed certificate or to avoid using 
default certificates from operating system.
