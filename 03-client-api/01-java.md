---
sidebarTitle: Java
pageTitle: Client Java
permalink: /docs/client-api/java
---

## Dependencies

| Client Java | Grakn Core | Grakn KGMS |
| :---------: | :--------: | :--------: |
| 1.5.0       | 1.5.0      | N/A        |
| 1.4.3       | 1.4.3      | 1.4.3      |
| 1.4.2       | 1.4.2      | 1.4.2      |
| 1.4.0       | 1.4.0      | 1.4.0      |
| 1.3.0       | 1.3.0      | 1.3.0      |
| 1.2.0       | 1.2.0      | 1.2.0      |

<div class="tabs dark">

[tab:Grakn Core]
```xml
<dependency>
  <groupId>grakn.core</groupId>
  <artifactId>client</artifactId>
  <version>1.5.0</version>
</dependency>
```
[tab:end]

[tab:Grakn KGMS]
```xml
<dependency>
  <groupId>ai.grakn.kgms</groupId>
  <artifactId>grakn-kgms</artifactId>
  <version>1.4.3</version>
</dependency>
```
[tab:end]

</div>

## Quickstart
First make sure, the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

Import `grakn.core.client.GraknClient`, instantiate a client and open a session to a [keyspace](/docs/management/keyspace).

<!-- test-standalone GraknQuickstartA.java -->
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

[KGMS ONLY] Using Client Java 1.4.3, we can also pass the credentials, as specified when [configuring authentication via Grakn Console](/docs/management/users).

<!-- test-ignore -->
```java
SimpleURI localGrakn = new SimpleURI("localhost", 48555);
Grakn grakn = new ClientFactory(localGrakn, "<username>", "<password>").client();
```

Create transactions to use for reading and writing data.

<!-- test-standalone GraknQuickstartB.java -->
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

<!-- test-standalone GraknQuickstartC.java -->
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