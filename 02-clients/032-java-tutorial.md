---
pageTitle: Java Driver tutorial
keywords: typedb, client, java
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: Tutorial for TypeDB Client Java.
---

# Java Driver tutorial

## Prerequisites

Make sure to install the Java Driver as per [Installation](031-java-install.md) page. The TypeDB server is also 
needs to be installed and running.

## Importing Java Driver and connecting to a server

Import the following modules: 

- `com.vaticle.typedb.client.TypeDB`
- `com.vaticle.typedb.client.api.TypeDBClient`
- `com.vaticle.typedb.client.api.TypeDBSession`

Instantiate a TypeDB Core client and open a [session](../0001-typedb/02-dev/01-connect.md#sessions) to a 
[database](../0001-typedb/02-dev/01-connect.md#databases). 

<div class="note">
[Note]
If you don't have a database, you can find how to create one on the 
[Quickstart](../0001-typedb/01-start/03-quickstart.md#create-a-database) page.

The name for the database should be `social_network`.
</div>

<!-- test-example TypeDBQuickstartA.java -->
```java
package com.vaticle.doc.examples;

import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;

public class TypeDBQuickstartA {
    public static void main(String[] args) {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");
        // client is open
        TypeDBSession session = client.session("social_network", TypeDBSession.Type.DATA);
        // session is open
        session.close();
        // session is closed
        client.close();
        // client is closed
    }
}
```

## Creating transactions

Create transactions to use for reading and writing data.

<!-- test-example TypeDBQuickstartB.java -->
```java
package com.vaticle.doc.examples;

import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.TypeDB;

public class TypeDBQuickstartB {
    public static void main(String[] args) {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");

        try (TypeDBSession session = client.session("social_network", TypeDBSession.Type.DATA)) {
            // creating a write transaction
            TypeDBTransaction writeTransaction = session.transaction(TypeDBTransaction.Type.WRITE);
            // write transaction is open
            // write transaction must always be committed (closed)
            writeTransaction.commit();
    
            // creating a read transaction
            TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ);
            // read transaction is open
            // read transaction must always be closed
            readTransaction.close();
        }

        client.close();
    }
}
```

## Sending queries

Running basic retrieval and insertion queries.

<!-- test-example TypeDBQuickstartC.java -->
```java
package com.vaticle.doc.examples;

import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typeql.lang.TypeQL;
import static com.vaticle.typeql.lang.TypeQL.*;
import com.vaticle.typeql.lang.query.TypeQLMatch;
import com.vaticle.typeql.lang.query.TypeQLInsert;
import com.vaticle.typedb.client.api.answer.ConceptMap;

import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Collectors;

public class TypeDBQuickstartC {
    public static void main(String[] args) {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");

        try (TypeDBSession session = client.session("social_network", TypeDBSession.Type.DATA)) {
            
            try (TypeDBTransaction writeTransaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
                // Insert a person using a WRITE transaction
                TypeQLInsert insertQuery = TypeQL.insert(var("x").isa("person").has("email", "x@email.com"));
                List<ConceptMap> insertedId = writeTransaction.query().insert(insertQuery).collect(Collectors.toList());
                System.out.println("Inserted a person with ID: " + insertedId.get(0).get("x").asThing().getIID());
                // to persist changes, a write transaction must always be committed (closed)
                writeTransaction.commit();
            }
            
            try (TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ)) {
                // Read the person using a READ only transaction
                TypeQLMatch.Limited getQuery = TypeQL.match(var("p").isa("person")).get("p").limit(10);
                Stream<ConceptMap> answers = readTransaction.query().match(getQuery);
                answers.forEach(answer -> System.out.println(answer.get("p").asThing().getIID()));
            }
        }

        client.close();
    }
}

```

<div class="note">
[Important]
Remember that transactions always need to be closed. Committing a write transaction closes it. A read transaction, 
however, must be explicitly closed by calling the `close()` method on it.
</div>

## Where to go next

Check out the [Response](033-java-api-ref.md#response) section of API reference page to learn about the available 
methods on the concepts retrieved as the answers to queries.

To view examples of various TypeQL queries, head over to 
[Writing data](../0001-typedb/02-dev/04-write.md) and
[Reading data](../0001-typedb/02-dev/05-read.md) pages.

For some more Java Driver examples — see the 
[Java implementation](../0001-typedb/01-start/05-sample-app.md#java-implementation) on the Sample application page.