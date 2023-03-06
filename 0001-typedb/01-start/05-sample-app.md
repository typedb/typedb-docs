---
pageTitle: Sample Application
keywords: getting started, typedb, typeql, tutorial, quickstart, application, app, example, sample
longTailKeywords: get started with typedb, typedb tutorial, typedb quickstart, learn typedb, sample app, sample application
summary: A simple example with a prototype application to run against a TypeDB database.
toc: false
---

# Sample Application

Let's create a simple application that interacts with TypeDB database that we created in the 
[Quickstart guide](03-quickstart.md).

The following Python script executes 4 requests to the `iam` database located at the `0.0.0.0:1729` address. 

You can save it locally and run it with the [Python](https://www.python.org/downloads/) v.3.9+.

After the script below you can find [simple explanation](#explanation) of 4 requests performed in the script.

<!--- #todo Add sample app in other languages as tabs! -->

```python
from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from datetime import datetime

print("\nIAM Sample App")

print("Connecting to the server")
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as Session
        print("\nRequest #1: User listing")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name $n, has email $e;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").get_value() + ", has E-Mail: " + item.get("e").get_value())
            print("Users found:", k)  # Print number of results

        print("\nRequest #2: Files that Kevin Morrison has access to")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; " \
                                "$o isa object, has path $fp; $pa($o, $va) isa access; get $fp;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("File #" + str(k) + ": " + item.get("fp").get_value())
            print("Files found:", k)  # Print number of results

        print("\nRequest #3: Files that Kevin Morrison has view access to (with inference and pagination)")
        typedb_options = TypeDBOptions.core()  # Initialising a new set of options
        typedb_options.infer = True  # Enabling inference in this new set of options
        with session.transaction(TransactionType.READ, typedb_options) as transaction:  # Open transaction to read with inference
            typeql_read_query = "match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; " \
                               "$o isa object, has path $fp; $pa($o, $va) isa access; " \
                               "$va isa action, has action-name 'view_file'; get $fp; sort $fp asc; offset 0; limit 5;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("File #" + str(k) + ": " + item.get("fp").get_value())

            typeql_read_query = "match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; " \
                               "$o isa object, has path $fp; $pa($o, $va) isa access; " \
                               "$va isa action, has action-name 'view_file'; get $fp; sort $fp asc; offset 5; limit 5;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("File #" + str(k) + ": " + item.get("fp").get_value())
            print("Files found:", k)  # Print number of results

        print("\nRequest #4: Add a new file and a view access to it")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            path = "logs/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
            typeql_insert_query = "insert $f isa file, has path '" + path + "';"
            print("Inserting file:", path)
            transaction.query().insert(typeql_insert_query)  # runs the query
            typeql_insert_query = "match $f isa file, has path '" + path + "'; " \
                                  "$vav isa action, has action-name 'view_file'; " \
                                  "insert ($vav, $f) isa access;"
            print("Adding view access to the file")
            transaction.query().insert(typeql_insert_query)  # runs the query
            transaction.commit()  # commits the transaction
```

## Explanation

### List Names and E-mails for all users that have them

TypeQL query used:

```typeql
match $u isa user, has full-name $n, has email $e;
```

Simple explanation: we seek through all entities of `user` subtype (assigning a variable `$u` for those) that have 
`full-name` attribute (variable `$n` assigned for those) and `email` attribute (variable `$e`). Since we don't have 
explicit `get` statement it is assumed that we get all the variables that were assigned in the query.

We assign the response to the `iterator` variable and then go through all elements printing the values of the `$n` and
`$e` variables.

<div class="note">
[Note]
Note that those users that will not have `full-name` or `email` attributes added to them will not be showed in the 
results of this request.
</div>

### List all files that Kevin Morrison has access to

TypeQL query used:

```typeql
match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; 
      $o isa object, has path $fp; $pa($o, $va) isa access; get $fp;
```

Simple explanation: we seek for a `user` (variable `$u`) with attribute `name` of value `Kevin Morrison` assigned.
Then we search for a permission relation (`$p`) inbetween this user `$u` and potential access `$pa`.
Finally, we state that an object `$o` with a path `$fp` should be a part of `$pa` potential access relation.
Without even specifying what kind of action `$va` it should be. From all that variables we request to return only the
`path` attribute (`$fp`) of an object that the user has a permission to access.

<div class="note">
[Note]
Note that users and files don't have a singular relation that connects them directly. According to the `iam`
[schema](03-quickstart.md#fifth-step--prepare-a-schema) we need two relations to connect them: `permission` and 
`access`. Both relations must be used to make a decision of whether a user have access to a file.
</div>

### List all files Kevin have a `view_file` access to

TypeQL query used:

```typeql
match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; 
      $o isa object, has path $fp; $pa($o, $va) isa access;
      $va isa action, has action-name 'view_file'; get $fp; sort $fp asc; offset 0; limit 5;
```

Simple explanation: This is the similar request to the previous one. The difference is we set the type of action (`$va`)
that the user has access to the `view_file`. We still get only `path` (`$fp`) but now sort in ascending order
and get it in two portions: this particular request gets the very first 5 entries.

<div class="note">
[Note]
Note that Kevin have been assigned only `modify_file` access and the `view_file` access being inferred by a 
[rule](../02-dev/05-schema.md#rules). To use inference in this query we modify TypeDB options and send modified 
set of options to the transaction call.
</div>

<div class="note">
[Note]
To make things a bit more interesting we split this into two separate queries by using an `offset` keyword: we get 
first 5 results and then 5 more results with an offset of 5. To be able to do that we apply sorting of the 
results by path variable. Otherwise, we can't guarantee the results will be in the same order every time we
send a request.
</div>

### Insert a new file and then insert an access relation to it

At first, we generate a new value for `path` Python variable, consisting of `logs/`prefix, current date and time in
compact format and `.log` ending.

TypeQL query used #1:

```typeql
insert $f isa file, has path '" + path + "';
```

Simple explanation: we insert `file` entity that has an attribute `path` with the value we generated before.

TypeQL query used #2:

```typeql
match $f isa file, has path '" + path + "'; $vav isa action, has action-name 'view_file'; insert ($vav, $f) isa access;
```

Simple explanation: we seek `file` entity that has an attribute `path` with the value we generated before.
And we find an `action`, that has a `action-name` attribute with the value of `view_file`. Then we insert an `access` 
relation inbetween the `file` and the `action`.

<div class="note">
[Note]
Note that we are creating file first. If we try to set access to non-existent file our request will succeed (if 
it's a valid request) but will not insert any new data (relation). After both requests are done we commit the 
write transaction. It is important not to forget to commit changes.
</div>
