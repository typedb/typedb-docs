---
pageTitle: Sample Application
keywords: getting started, typedb, typeql, tutorial, quickstart, application, app, example, sample
longTailKeywords: get started with typedb, typedb tutorial, typedb quickstart, learn typedb, sample app, sample application
summary: A simple example with a prototype application to run against a TypeDB database.
toc: false
---

# Sample Application

The following sample app implementations are all designed to connect to the [IAM](04-iam-schema.md) database located at 
the TypeDB server with `0.0.0.0:1729` address. Please make sure you have TypeDB server running with the `iam` database 
created and both **schema** and **data** loaded. Use the [Installation guide](02-installation.md) to prepare the server 
and [Quickstart guide](03-quickstart.md) to prepare such a database.

Sample application have the following implementations:

- [Python](#python-implementation)
- [Java](#java-implementation)

## Python implementation

The following Python script executes 4 simple requests to the `iam` database. 

You can save it locally and run it with the [Python](https://www.python.org/downloads/) v.3.9+. Make sure to install 
[typedb python driver](../../02-clients/04-python.md) with pip.

Use the source code below or the [explanation](#explanation) section to explore 4 requests performed in the sample app.

<!--- #todo Add tabs! -->

<!-- test-ignore -->
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

### Explanation

#### List Names and E-mails for all users that have them

TypeQL query used:

<!-- test-ignore -->
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

Additionally, those having multiple full-names or emails can be mentioned more than once.
</div>

#### List all files that Kevin Morrison has access to

TypeQL query used:

<!-- test-ignore -->
```typeql
match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; 
      $o isa object, has path $fp; $pa($o, $va) isa access; get $fp;
```

Simple explanation: we seek for a `user` (variable `$u`) with attribute `full-name` of value `Kevin Morrison` assigned.
Then we search for a `permission` relation (`$p`) inbetween this user `$u` and potential access `$pa`.
Finally, we state that an `object` (`$o`) with a path `$fp` should be a part of `$pa` `access` relation.
Without even specifying what kind of action `$va` it should be. From all that variables we request to return only the
`path` attributes (`$fp`) of any `object` that the `user` has a `permission` to `access`.

<div class="note">
[Note]
Note that users and files don't have a singular relation that connects them directly. According to the `iam`
[schema](04-iam-schema.md) we need two relations to connect them: `permission` and 
`access`. Both relations must be used to make a decision of whether a user have access to a file.
</div>

#### List all files Kevin have a view_file access to (with inference)

TypeQL query used:

<!-- test-ignore -->
```typeql
match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; 
      $o isa object, has path $fp; $pa($o, $va) isa access;
      $va isa action, has action-name 'view_file'; get $fp; sort $fp asc; offset 0; limit 5;
```

Simple explanation: This is the similar request to the previous one. The difference is we set the type of action (`$va`)
that the user has access to the `view_file`. We still get only `path` (`$fp`) but now sort in ascending order
and get it in two portions: this particular request gets the very first 5 entries. Later one will get another 5, 
starting from #6.

<div class="note">
[Note]
Note that Kevin have been assigned only `modify_file` access and the `view_file` access being inferred by a 
[rule](../02-dev/02-schema.md#rules). To use inference in this query we modify TypeDB options and send modified 
set of options to the transaction call.
</div>

<div class="note">
[Note]
To make things a bit more interesting we split this into two separate queries by using an `offset` keyword: we get 
first 5 results and then 5 more results with an offset of 5. To be able to do that we apply sorting of the 
results by path variable. Otherwise, we can't guarantee the results will be in the same order every time we
send a request.
</div>

#### Insert a new file and then insert an access relation to it

At first, we generate a new value for `filepath` Python variable, consisting of `logs/`prefix, current date and time in
compact format and `.log` ending.

TypeQL query #1:

<!-- test-ignore -->
```typeql
insert $f isa file, has path '" + path + "';
```

Simple explanation: we insert `file` entity that has an attribute `path` with the value we generated before.

TypeQL query #2:

<!-- test-ignore -->
```typeql
match $f isa file, has path '" + path + "'; $vav isa action, has action-name 'view_file'; insert ($vav, $f) isa access;
```

Simple explanation: we seek `file` entity that has an attribute `path` with the value we generated before.
And we find an `action`, that has a `action-name` attribute with the value of `view_file`. Then we insert an `access` 
relation inbetween the `file` and the `action`.

<div class="note">
[Note]
Note that we are creating `file` first. If we try to set `access` to non-existent `file` our request will succeed (if 
don't make any mistakes in the syntax of the query) but will not insert any new data (relation). After both requests 
are done we commit the write transaction. It is important not to forget to commit changes.
</div>

## Java implementation

The following Java code can be built into a sample application that sends 4 simple requests to the `iam` database. 

You can save it locally, build with maven and run it with the Java v.19+.

<!--- #todo Update the link to the repo with some vaticle repo -->
Alternatively, you can clone the full [repository](https://github.com/izmalk/iam-sample-app-java) with maven specs and 
some other quality of life addons.

Use the source code below or the [explanation](#explanation) section to explore 4 requests performed in the sample app.

<!--- #todo Add tabs! -->
<!-- test-ignore -->
```java
package org.example2;

import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBOptions;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typeql.lang.TypeQL;
import static com.vaticle.typeql.lang.TypeQL.*;
import com.vaticle.typeql.lang.query.TypeQLMatch;
import com.vaticle.typeql.lang.query.TypeQLInsert;
import com.vaticle.typedb.client.api.answer.ConceptMap;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Collectors;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {
    public static void main(String[] args) {
        System.out.println("IAM Sample App");

        System.out.println("Connecting to the server");
        TypeDBClient client = TypeDB.coreClient("0.0.0.0:1729"); // client is connected to the server
        System.out.println("Connecting to the `iam` database");
        try (TypeDBSession session = client.session("iam", TypeDBSession.Type.DATA)) { // session is open

            System.out.println("");
            System.out.println("Request #1: User listing");
            try (TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ)) { // READ transaction is open
                List<PersonData> answer = new ArrayList<>(); // create a list for answers
                readTransaction.query().match(
                        "match $u isa user, has full-name $n, has email $e;" // TypeQL query
                ).forEach(result -> answer.add(new PersonData( // Store results as PersonData in the answer list
                        result.get("n").asAttribute().asString().getValue(),
                        result.get("e").asAttribute().asString().getValue())));
                if (answer.isEmpty()) {
                    System.out.println("Response is empty.");
                } else {
                    int k = 0; // create a counter
                    for (PersonData i : answer) {
                        k += 1;
                        System.out.println("User #" + k + ": " + i.fullname + ", has E-mail: " + i.email);
                    }
                    System.out.println("Users found: " + k);
                }
            }

            System.out.println("");
            System.out.println("Request #2: Files that Kevin Morrison has access to");
            try (TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ)) { // READ transaction is open
                 List<String> answer = new ArrayList<>();
                // String getQuery = "match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; " +
                //        "$o isa object, has path $fp; $pa($o, $va) isa access; get $fp;"; // Example of the same TypeQL query
                TypeQLMatch.Filtered getQuery = TypeQL.match(
                        var("u").isa("user").has("full-name", "Kevin Morrison"),
                        var("p").rel("u").rel("pa").isa("permission"),
                        var("o").isa("object").has("path", var("fp")),
                        var("pa").rel("o").rel("va").isa("access")
                ).get("fp");
                Stream<ConceptMap> answers = readTransaction.query().match(getQuery);
                //answers.forEach(answer -> System.out.println(answer.get("fp").asThing().asAttribute().getValue()));
                answers.forEach(result -> answer.add(result.get("fp").asAttribute().asString().getValue()));
                if (answer.isEmpty()) {
                    System.out.println("Response is empty.");
                } else {
                    int k = 0; // create a counter
                    for (String i : answer) {
                        k += 1;
                        System.out.println("File #" + k + ": " + i);
                    }
                    System.out.println("Files found: " + k);
                }
            }

            System.out.println("");
            System.out.println("Request #3: Files that Kevin Morrison has view access to (with inference)");
            try (TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ, TypeDBOptions.core().infer(true))) { // READ transaction is open
                List<String> answer = new ArrayList<>();
                // String getQuery = "match $u isa user, has full-name 'Kevin Morrison';
                // $p($u, $pa) isa permission;
                // $o isa object, has path $fp;
                // $pa($o, $va) isa access;
                // $va isa action, has action-name 'view_file';
                // get $fp; sort $fp asc; offset 0; limit 5;"
                TypeQLMatch.Limited getQuery = TypeQL.match(
                        var("u").isa("user").has("full-name", "Kevin Morrison"),
                        var("p").rel("u").rel("pa").isa("permission"),
                        var("o").isa("object").has("path", var("fp")),
                        var("pa").rel("o").rel("va").isa("access"),
                        var("va").isa("action").has("action-name", "view_file")
                ).get("fp").sort("fp").offset(0).limit(5);
                Stream<ConceptMap> answers = readTransaction.query().match(getQuery);
                answers.forEach(result -> answer.add(result.get("fp").asAttribute().asString().getValue()));
                int k = 0; // create a counter
                if (answer.isEmpty()) {
                    System.out.println("Response is empty.");
                } else {
                    for (String i : answer) {
                        k += 1;
                        System.out.println("File #" + k + ": " + i);
                    }
                    //System.out.println("Files found (first batch): " + k);
                }

                List<String> answer2 = new ArrayList<>();
                TypeQLMatch.Limited getQuery2 = TypeQL.match(
                        var("u").isa("user").has("full-name", "Kevin Morrison"),
                        var("p").rel("u").rel("pa").isa("permission"),
                        var("o").isa("object").has("path", var("fp")),
                        var("pa").rel("o").rel("va").isa("access"),
                        var("va").isa("action").has("action-name", "view_file")
                ).get("fp").sort("fp").offset(5).limit(5);
                Stream<ConceptMap> answers2 = readTransaction.query().match(getQuery2);
                answers2.forEach(result -> answer2.add(result.get("fp").asAttribute().asString().getValue()));
                if (answer2.isEmpty()) {
                    System.out.println("Response is empty for the files #6-10.");
                } else {
                    for (String i : answer2) {
                        k += 1;
                        System.out.println("File #" + k + ": " + i);
                    }
                    System.out.println("Files found: " + k);
                }
            }

            System.out.println("");
            System.out.println("Request #4: Add a new file and a view access to it");
            try (TypeDBTransaction writeTransaction = session.transaction(TypeDBTransaction.Type.WRITE)) { // WRITE transaction is open
                String filepath = "logs/" + DateTime.now() + ".log";
                // "insert $f isa file, has path '" + filepath + "';"
                TypeQLInsert insertQuery = TypeQL.insert(var("f").isa("file").has("path", filepath));
                System.out.println("Inserting file: " + filepath);
                List<ConceptMap> insertedId = writeTransaction.query().insert(insertQuery).collect(Collectors.toList());
                //System.out.println("Inserted a file with iid: " + insertedId.get(0).get("f").asThing().getIID());

                // "match $f isa file, has path '" + filepath + "';
                // $vav isa action, has action-name 'view_file';
                // insert ($vav, $f) isa access;"
                TypeQLInsert matchInsertQuery = TypeQL.match(
                        var("f").isa("file").has("path", filepath),
                        var("vav").isa("action").has("action-name", "view_file")
                                )
                        .insert(var("pa").rel("vav").rel("f").isa("access"));
                System.out.println("Adding view access to the file");
                List<ConceptMap> matchInsertedId = writeTransaction.query().insert(matchInsertQuery).collect(Collectors.toList());
                //System.out.println("Inserted a relation with iid: " + matchInsertedId.get(0).get("pa").asThing().getIID());
                writeTransaction.commit(); // to persist changes, a write transaction must always be committed
            }
        }
        client.close(); // closing server connection
    }
}

class PersonData {
    public PersonData(String fullname, String email) {
        this.fullname = fullname;
        this.email = email;
    }

    public String fullname;
    public String email;
}

class DateTime {
    public static String now() {
        SimpleDateFormat formatter = new SimpleDateFormat("Y-m-d-H-M-S");
        Date date = new Date();
        return(formatter.format(date));
    }
}

```

### Explanation

#### List Names and E-mails for all users that have them

In this most simple request we want to showcase how to use TypeQL syntax. In later requests we will use TypeQL query 
builder syntax.

TypeQL query used:

<!-- test-ignore -->
```java
match $u isa user, has full-name $n, has email $e;
```

Simple explanation: we seek through all entities of `user` subtype (assigning a variable `$u` for those) that have 
`full-name` attribute (variable `$n` assigned for those) and `email` attribute (variable `$e`). Since we don't have 
explicit `get` statement it is assumed that we get all the variables that were assigned in the query.

We use the responses as `result` to add to answer list, which consists of `PersonData` objects. Those objects 
specifically designed to store `fullname` and `email` as strings. So we send variables `n` as first argument for 
`fullname` and `e` as second one for `email`.

After that we check answer list for being empty and proceed to count and publish every result to console.

<div class="note">
[Note]
Note that those users that will not have `full-name` or `email` attributes added to them will not be showed in the 
results of this request. 

Additionally, those having multiple full-names or emails can be mentioned more than once.
</div>

#### List all files that Kevin Morrison has access to

TypeQL query builder clause used:

<!-- test-ignore -->
```java
TypeQLMatch.Filtered getQuery = TypeQL.match(
        var("u").isa("user").has("full-name", "Kevin Morrison"),
        var("p").rel("u").rel("pa").isa("permission"),
        var("o").isa("object").has("path", var("fp")),
        var("pa").rel("o").rel("va").isa("access")
).get("fp");
```

Simple explanation: we seek for a `user` (variable `$u`) with attribute `full-name` of value `Kevin Morrison` assigned.
Then we search for a `permission` relation (`$p`) inbetween this user `$u` and potential access `$pa`.
Finally, we state that an `object` (`$o`) with a path `$fp` should be a part of `$pa` `access` relation.
Without even specifying what kind of action `$va` it should be. From all that variables we request to return only the
`path` attributes (`$fp`) of any `object` that the `user` has a `permission` to `access`.

<div class="note">
[Note]
Note that users and files don't have a singular relation that connects them directly. According to the `iam`
[schema](04-iam-schema.md) we need two relations to connect them: `permission` and 
`access`. Both relations must be used to make a decision of whether a user have access to a file.
</div>

#### List all files Kevin have a view_file access to (with inference)

TypeQL query builder clause #1 used:

<!-- test-ignore -->
```java
TypeQLMatch.Limited getQuery = TypeQL.match(
        var("u").isa("user").has("full-name", "Kevin Morrison"),
        var("p").rel("u").rel("pa").isa("permission"),
        var("o").isa("object").has("path", var("fp")),
        var("pa").rel("o").rel("va").isa("access"),
        var("va").isa("action").has("action-name", "view_file")
).get("fp").sort("fp").offset(0).limit(5);
```

Simple explanation: This is the similar request to the previous one. The difference is we set the type of action (`$va`)
that the user has access to the `view_file`. We still get only `path` (`$fp`) but now sort in ascending order
and get it in two portions: this particular request gets the very first 5 entries. Later one will get another 5, 
starting from #6.

<div class="note">
[Note]
Note that Kevin have been assigned only `modify_file` access and the `view_file` access being inferred by a 
[rule](../02-dev/02-schema.md#rules). To use inference in this query we modify TypeDB options and send modified 
set of options to the transaction call.
</div>

<div class="note">
[Note]
To make things a bit more interesting we split this into two separate queries by using an `offset` keyword: we get 
first 5 results and then 5 more results with an offset of 5. To be able to do that we apply sorting of the 
results by the `path` variable. Otherwise, we can't guarantee the results will be in the same order every time we
send a request.
</div>

#### Insert a new file and then insert an access relation to it

At first, we generate a new value for `filepath` Java string variable, consisting of `logs/`prefix, current date and 
time in compact format and `.log` ending.

TypeQL query builder clause for query #1:

<!-- test-ignore -->
```java
TypeQLInsert insertQuery = TypeQL.insert(var("f").isa("file").has("path", filepath));
```

Simple explanation: we insert `file` entity that has an attribute `path` with the value we generated before.

TypeQL query builder clause for query #2:

<!-- test-ignore -->
```java
TypeQLInsert matchInsertQuery = TypeQL.match(
        var("f").isa("file").has("path", filepath),
        var("vav").isa("action").has("action-name", "view_file")
                )
        .insert(var("pa").rel("vav").rel("f").isa("access"));
```

Simple explanation: we seek `file` entity that has an attribute `path` with the value we generated before.
And we find an `action`, that has a `action-name` attribute with the value of `view_file`. Then we insert an `access` 
relation inbetween the `file` and the `action`.

<div class="note">
[Note]
Note that we are creating `file` first. If we try to set `access` to non-existent `file` our request will succeed (if 
don't make any mistakes in the syntax of the query) but will not insert any new data (relation). After both requests 
are done we commit the write transaction. It is important not to forget to commit changes.
</div>
