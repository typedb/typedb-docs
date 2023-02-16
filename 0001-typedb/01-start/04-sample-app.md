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

The following Python script executes 4 requests to the `iam` database located at the `0.0.0.0:1729` address:

1. List Names and E-mails for all users that have them.

    <div class="note">
    [Note]
    Note that those users that will not have name or e-mail added to them will not be showed in the results of this 
    request.
    </div>

2. List all files that Kevin Morrison has access to.
    
    <div class="note">
    [Note]
    Note that users and files don't have a singular relation that connects them directly. According to the `iam`
    [schema](03-quickstart.md#fifth-step--prepare-a-schema) we need two relations to connect them: `permission` and 
    `access`. Both relations must be used to make an decision of whether a user have access to a file.
    </div>

3. List all files Kevin have a `view_file` access to.
   
    <div class="note">
    [Note]
    Note that Kevin have been assigned only `modify_file` access and the `view_file` access being inferred by a 
    [rule](../02-dev/05-schema.md#rules). To use inference in this query we modify TypeDB options and send modified 
    set of options to the transaction call.
    </div>

    <div class="note">
    [Note]
    To make things a bit more interesting we split this into two separate queries by using an offset: we get 
    first 5 results and then 5 more results with an offset of 5. To be able to do that we apply sorting of the 
    results by filepath variable. Otherwise, we can't guarantee the results will be in the same order every time we
    send a request.
    </div>
 
4. Insert a new file and then insert an access relation to it.

    <div class="note">
    [Note]
    Note that we are creating file first. If we try to set access to non-existent file our request will succeed (if 
    it's a valid request) but will not insert any new data (relation). After both requests are done we commit the 
    write transaction. It is important not to forget to commit changes.
    </div>

<!--- #todo Add sample app in other languages as tabs! -->

```python
from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions
from datetime import datetime

print("IAM Sample App")

print("Connecting to the server")
with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    print("Connecting to the `iam` database")
    with client.session("iam", SessionType.DATA) as session:  # Access data in the `iam` database as Session
        print("Request #1: User listing")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has name $n, has email $e;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("User #" + str(k) + ": " + item.get("n").get_value() + ", has E-Mail: " + item.get("e").get_value())
            print("Users found:", k)  # Print number of results

        print("\nRequest #2: Files that Kevin Morrison has access to")
        with session.transaction(TransactionType.READ) as transaction:  # Open transaction to read
            typeql_read_query = "match $u isa user, has name 'Kevin Morrison'; $p($u, $pa) isa permission; " \
                                "$o isa object, has filepath $fp; $pa($o, $va) isa access; get $fp;"
            iterator = transaction.query().match(typeql_read_query)  # Executing query
            k = 0
            for item in iterator:  # Iterating through results
                k += 1  # Counter
                print("File #" + str(k) + ": " + item.get("fp").get_value())
            print("Files found:", k)  # Print number of results

        print("\nRequest #3: Files that Kevin Morrison has view access to (with inference)")
        typedb_options = TypeDBOptions.core()  # Initialising a new set of options
        typedb_options.infer = True  # Enabling inference in this new set of options
        with session.transaction(TransactionType.READ, typedb_options) as transaction:  # Open transaction to read with inference
           typeql_read_query = "match $u isa user, has name 'Kevin Morrison'; $p($u, $pa) isa permission; "
                               "$o isa object, has filepath $fp; $pa($o, $va) isa access; "
                               "$va isa action, has name 'view_file'; get $fp; sort $fp asc; offset 0; limit 5;"
           iterator = transaction.query().match(typeql_read_query)  # Executing query
           k = 0
           for item in iterator:  # Iterating through results
              k += 1  # Counter
              print("File #" + str(k) + ": " + item.get("fp").get_value())

           typeql_read_query = "match $u isa user, has name 'Kevin Morrison'; $p($u, $pa) isa permission; "
                               "$o isa object, has filepath $fp; $pa($o, $va) isa access; "
                               "$va isa action, has name 'view_file'; get $fp; sort $fp asc; offset 5; limit 5;"
           iterator = transaction.query().match(typeql_read_query)  # Executing query
           for item in iterator:  # Iterating through results
              k += 1  # Counter
              print("File #" + str(k) + ": " + item.get("fp").get_value())
           print("Files found:", k)  # Print number of results

        print("\nRequest #4: Add a new file and a view access to it")
        with session.transaction(TransactionType.WRITE) as transaction:  # Open transaction to write
            filepath = "logs/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
            typeql_insert_query = "insert $f isa file, has filepath '" + filepath + "';"
            transaction.query().insert(typeql_insert_query)  # runs the query
            print("Inserting file:", filepath)
            typeql_insert_query = "match $f isa file, has filepath '" + filepath + "'; " \
                                  "$vav isa action, has name 'view_file'; " \
                                  "insert ($vav, $f) isa access;"
            print("Adding view access to the file")
            transaction.query().insert(typeql_insert_query)  # runs the query
            transaction.commit()  # commits the transaction
```
