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
&lt;dependency&gt;
  &lt;groupId&gt;ai.grakn&lt;/groupId&gt;
  &lt;artifactId&gt;client-java&lt;/artifactId&gt;
  &lt;version&gt;1.4.3&lt;/version&gt;
&lt;/dependency&gt;
```
[tab:end]

[tab:Grakn KGMS]
```xml
&lt;dependency&gt;
  &lt;groupId&gt;ai.grakn.kgms&lt;/groupId&gt;
  &lt;artifactId&gt;client&lt;/artifactId&gt;
  &lt;version&gt;1.4.3&lt;/version&gt;
&lt;/dependency&gt;
```
[tab:end]

</div>

## Quickstart
First make sure, the [Grakn server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

In the interpreter or in your source, import `grakn`.

Instantiate a client and open a session.

<!-- ignore-test -->
```java
import ai.grakn.Keyspace;
import ai.grakn.client.Grakn;
import ai.grakn.util.SimpleURI;

public class GraknQuickstart {
    public static void main(String[] args) {
        SimpleURI localGrakn = new SimpleURI("localhost", 48555);
        Keyspace keyspace = Keyspace.of("genealogy");
        Grakn grakn = new Grakn(localGrakn);
        Grakn.Session session = grakn.session(keyspace);
        // session is open
        session.close();
        // session is closed
    }
}
```

[KGMS ONLY] We can also pass the credentials, as specified when [configuring authentication via Grakn Console](/docs/management/users).

<!-- ignore-test -->
```java
SimpleURI localGrakn = new SimpleURI("localhost", 48555);
Grakn grakn = new ClientFactory(localGrakn, "<username>", "<password>").client();
```

Create transactions to use for reading and writing data.

<!-- ignore-test -->
```java
import ai.grakn.GraknTxType;
import ai.grakn.Keyspace;
import ai.grakn.client.Grakn;
import ai.grakn.util.SimpleURI;

public class GraknQuickstart {
    public static void main(String[] args) {
        SimpleURI localGrakn = new SimpleURI("localhost", 48555);
        Keyspace keyspace = Keyspace.of("genealogy");
        Grakn grakn = new Grakn(localGrakn);
        Grakn.Session session = grakn.session(keyspace);

        // creating a write transaction
        Grakn.Transaction writeTransaction = session.transaction(GraknTxType.WRITE);
        // write transaction is open
        // write transaction must always be committed (closed)
        writeTransaction.commit();

        // creating a read transaction
        Grakn.Transaction readTransaction = session.transaction(GraknTxType.READ);
        // read transaction is open
        // read transaction must always be closed
        readTransaction.close();

        session.close();
    }
}
```

Running basic retrieval and insertion queries.

<!-- ignore-test -->
```java
import ai.grakn.GraknTxType;
import ai.grakn.Keyspace;
import ai.grakn.client.Grakn;
import ai.grakn.graql.GetQuery;
import ai.grakn.graql.Graql;
import ai.grakn.graql.InsertQuery;
import ai.grakn.graql.answer.ConceptMap;
import ai.grakn.util.SimpleURI;
import java.util.List;
import java.util.stream.Stream;

public class GraknQuickstart {
  public static void main(String[] args) {
    SimpleURI localGrakn = new SimpleURI("localhost", 48555);
    Keyspace keyspace = Keyspace.of("phone_calls");
    Grakn grakn = new Grakn(localGrakn);
    Grakn.Session session = grakn.session(keyspace);

    // Insert a person using a WRITE transaction
    Grakn.Transaction writeTransaction = session.transaction(GraknTxType.WRITE);
    InsertQuery insertQuery = Graql.insert(var("p").isa("person").has("first-name", "Elizabeth"));
    List<ConceptMap> insertedId = insertQuery.withTx(writeTransaction).execute();
    System.out.println("Inserted a person with ID: " + insertedId.get(0).get("p").id());
    // to persist changes, a write transaction must always be committed (closed)
    writeTransaction.commit();

    // Read the person using a READ only transaction
    Grakn.Transaction readTransaction = session.transaction(GraknTxType.READ);
    GetQuery query = Graql.match(var("p").isa("person")).limit(10).get();
    Stream<ConceptMap> answers = query.withTx(readTransaction).stream();
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