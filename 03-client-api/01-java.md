---
sidebarTitle: Java
pageTitle: Client Java
permalink: /docs/client-api/java
---

## Dependencies
The only dependency for getting started with Grakn Client Java is `Grakn >= 1.3.0` added as a dependency in your Java project.

<div class="tabs dark">

[tab:Grakn Core]
```xml
<dependency>
  <groupId>ai.grakn</groupId>
  <artifactId>client-java</artifactId>
  <version>1.4.3</version>
</dependency>
```
[tab:end]

[tab:Grakn KGMS]
```xml
<dependency>
  <groupId>ai.grakn.kgms</groupId>
  <artifactId>client</artifactId>
  <version>1.4.3</version>
</dependency>
```
[tab:end]

</div>

## Quickstart
First make sure, the [Grakn server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

In the interpreter or in your source, import `grakn`.

Instantiate a client and open a session.

<<<<<<< HEAD
<!-- test-standalone GraknQuickstartA.java -->
=======
<!-- test-ignore -->
>>>>>>> development
```java
package grakn.examples;

import grakn.core.client.GraknClient;

public class GraknQuickstartA {
    public static void main(String[] args) {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");
        // session is open
        session.close();
        // session is closed
    }
}
```

[KGMS ONLY] We can also pass the credentials, as specified when [configuring authentication via Grakn Console](/docs/management/users).

<!-- test-ignore -->
```java
SimpleURI localGrakn = new SimpleURI("localhost", 48555);
Grakn grakn = new ClientFactory(localGrakn, "<username>", "<password>").client();
```

Create transactions to use for reading and writing data.

<<<<<<< HEAD
<!-- test-standalone GraknQuickstartB.java -->
=======
<!-- test-ignore -->
>>>>>>> development
```java
package grakn.examples;

import grakn.core.client.GraknClient;

public class GraknQuickstartB {
    public static void main(String[] args) {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");

        // creating a write transaction
        GraknClient.Transaction writeTransaction = session.transaction().write();
        // write transaction is open
        // write transaction must always be committed (closed)
        writeTransaction.commit();

        // creating a read transaction
        GraknClient.Transaction readTransaction = session.transaction().read();
        // read transaction is open
        // read transaction must always be closed
        readTransaction.close();

        session.close();
    }
}

```

Running basic retrieval and insertion queries.

<<<<<<< HEAD
<!-- test-standalone GraknQuickstartC.java -->
=======
<!-- test-ignore -->
>>>>>>> development
```java
package grakn.examples;

import grakn.core.client.GraknClient;
import graql.lang.Graql;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlGet;
import graql.lang.query.GraqlInsert;
import grakn.core.concept.answer.ConceptMap;

import java.util.List;
import java.util.stream.Stream;

public class GraknQuickstartC {
  public static void main(String[] args) {
    GraknClient client = new GraknClient("localhost:48555");
    GraknClient.Session session = client.session("social_network");

    // Insert a person using a WRITE transaction
    GraknClient.Transaction writeTransaction = session.transaction().write();
    GraqlInsert insertQuery = Graql.insert(var("x").isa("person").has("email", "x@email.com"));
    List<ConceptMap> insertedId = writeTransaction.execute(insertQuery);
    System.out.println("Inserted a person with ID: " + insertedId.get(0).get("x").id());
    // to persist changes, a write transaction must always be committed (closed)
    writeTransaction.commit();

    // Read the person using a READ only transaction
    GraknClient.Transaction readTransaction = session.transaction().read();
    GraqlGet getQuery = Graql.match(var("p").isa("person")).get().limit(10);
    Stream<ConceptMap> answers = readTransaction.stream(getQuery);
    answers.forEach(answer -> System.out.println(answer.get("p").id()));

    // a read transaction and session must always be closed
    readTransaction.close();
    session.close();
  }
}

```
<div class="note">
[Important]
Remember that transactions always need to be closed. Commiting a write transaction closes it. A read transaction, however, must be explicitly clased by calling the `close()` method on it.
</div>

Check out the [Concept API](/docs/concept-api/overview) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Java, head over to their dedicated documentation pages as listed below.

- [Insert](/docs/query/insert-query)
- [Get](/docs/query/get-query)
- [Delete](/docs/query/delete-query)
- [Aggregate](/docs/query/aggregate-query)
- [Compute](/docs/query/compute-query)

{% include client_api.html language = "java" %}