---
pageTitle: New TypeDB Clients
keywords: grpc, protobuf, client, driver
longTailKeywords: typedb client, typedb driver, client development, new client, client implementation
Summary: Guide to writing clients in new languages
---

# Developing a new TypeDB Client

## Introduction

Vaticle maintains official TypeDB Clients (TypeDB Studio and Console) and Drivers for Java, Python, and NodeJS. All our 
other TypeDB Clients or Drivers are community-built.

It's possible to build a TypeDB Client for any language. A TypeDB Client fundamentally is a lightweight frontend
to the TypeDB server. This page is a guide for the components and protocols that need to be implemented.

## gRPC

[gRPC](https://grpc.io/) is the network call framework that TypeDB uses. A TypeDB client needs a gRPC client library 
to communicate with the server. Most languages have gRPC libraries.

### Why use gRPC?

Architecturally, gRPC is an alternative to HTTP (say, REST API or websockets). In TypeDB's client-server architecture,
performance is critical, and gRPC fits well with TypeDB's scaling model. It establishes a long-lasting connection,
much like a websocket. Payloads are encoded in the Protocol Buffer format, which is both efficient and strongly typed:

```protobuf
// Example message from typedb-protocol: note that each field has a restricted data type (string, int64 etc.)
message Attribute {
  message Value {
    oneof value {
      string string = 1;
      bool boolean = 2;
      int64 long = 3;
      double double = 4;
      // time since epoch in milliseconds
      int64 date_time = 5;
    }
  }
}
```

## TypeDB protocol

[Protocol Buffers](https://developers.google.com/protocol-buffers) is the encoding used to serialise network messages.
Proto definition files can be compiled into server-side and client-side libraries using a Protobuf Compiler.
In our case, we only need client-side library compilation. Most languages have Protobuf compilers available.

TypeDB's protobuf definitions can be found at https://github.com/vaticle/typedb-protocol.
During development, it's sufficient to manually copy-paste from this repository and do a one-time compilation.
A more reliable method is to import the Protocol repo via a package manager and compile it at build time.
TypeDB's build system, [Bazel](https://bazel.build/), offers one approach. If you'd like to use a different package 
manager, the TypeDB team may also be able to help by setting up a distribution channel for your language's compiled 
protobuf files. If this is the case, please get in touch.

## Client code architecture

TypeDB Clients adhere to a common architecture. This greatly reduces the workload of
maintaining them, so we also recommend community contributions to follow the same basic structure.

The following diagram shows all the packages (directories) in Java Driver and their dependency graph:

![Client Package Structure](../images/client-api/package-structure.png)

The entry point is the root package, in this case named `client-java`.
`api` is where we declare all the available client methods – basically all the interfaces.
`core` holds the basic building blocks: client, session, transaction.
Then we have `query` for querying, `concept` for the API to be able to process concepts, `logic` for reasoning.

There are many places you could start building a client. In this guide, we start by attempting to make a single gRPC 
call to TypeDB, and create a database.

## Tutorial: create a database

Create a `TypeDB` source file in the root of the project, which should expose a function named `coreClient`, 
taking `address` as a parameter.

<div class="note">
[Important]
Import statements are not included in this tutorial, except when importing from external libraries such as the 
TypeDB protobuf definitions.
</div>

<div class="tabs dark">

[tab:Java]
<!-- test-ignore -->
```java
// TypeDB.java
public class TypeDB {
    public static TypeDBClient coreClient(String address) {
        return new CoreClient(address);
    }
}
```
[tab:end]

[tab:Node.js]
```typescript
// TypeDB.ts
export namespace TypeDB {
    export function coreClient(address: string): TypeDBClient {
        return new CoreClient(address);
    }
}
```
[tab:end]

[tab:Python]
```python
# typedb/client.py (named to allow importing from typedb.client)
class TypeDB:
    @staticmethod
    def core_client(address: str, parallelisation: int = 2) -&gt; TypeDBClient:
        return _CoreClient(address, parallelisation)
```
[tab:end]

</div>

`TypeDBClient` is not yet defined. Create a new directory named `api/connection` and create a `TypeDBClient` file there:

<div class="note">
[Note]
if your language doesn't have interfaces or abstract classes, make `TypeDB.coreClient` return `CoreClient` instead, 
and skip this step.
</div>

<div class="tabs dark">

[tab:Java]
<!-- test-ignore -->
```java
// api/connection/TypeDBClient.java
public interface TypeDBClient extends AutoCloseable {
    DatabaseManager databases();
    void close();
}
```
[tab:end]

[tab:Node.js]
```typescript
// api/connection/TypeDBClient.ts
export interface TypeDBClient {
    readonly databases: DatabaseManager;
    close(): Promise&lt;void&gt;;
}
```
[tab:end]

[tab:Python]
```python
# typedb/api/connection/client.py
from abc import ABC, abstractmethod

class TypeDBClient(ABC):
    @abstractmethod
    def databases(self) -&gt; DatabaseManager:
        pass

    @abstractmethod
    def close(self) -&gt; None:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
```
[tab:end]

</div>

The next step is to implement `connection/TypeDBClient` and its subclass `connection/core/CoreClient`.
Create the directory structure: `connection/core` in the root of your project.
Name the classes depending on language conventions: in Java/TypeScript, `TypeDBClientImpl` and `CoreClient`; in Python, 
`_TypeDBClient` and `_CoreClient`.

_Ensure that you've imported gRPC into your project, and refer to the [gRPC docs](https://grpc.io/docs/languages/) to 
learn how to create a Channel - the code varies by language._

<div class="note">
[Note]
In languages with no inheritance, adhere to this project structure as closely as possible, perhaps by writing 
top-level functions in the respective locations.
</div>

<div class="tabs dark">

[tab:Java]
<!-- test-ignore -->
```java
// connection/TypeDBClientImpl.java
public abstract class TypeDBClientImpl implements TypeDBClient {
    private final TypeDBDatabaseManagerImpl databaseMgr;

    protected TypeDBClientImpl() {
        databaseMgr = new TypeDBDatabaseManagerImpl(this);
    }

    @Override
    public TypeDBDatabaseManagerImpl databases() {
        return databaseMgr;
    }

    public abstract ManagedChannel channel();

    public abstract TypeDBStub stub();

    @Override
    public void close() {
        try {
            channel().shutdown().awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

// connection/core/CoreClient.java
public class CoreClient extends TypeDBClientImpl {
    private final ManagedChannel channel;
    private final TypeDBStub stub;

    public CoreClient(String address) {
        super();
        channel = NettyChannelBuilder.forTarget(address).usePlaintext().build();
        stub = CoreStub.create(channel);
    }

    @Override
    public ManagedChannel channel() {
        return channel;
    }

    @Override
    public TypeDBStub stub() {
        return stub;
    }
}
```
[tab:end]

[tab:Node.js]
```typescript
// connection/TypeDBClientImpl.ts
export abstract class TypeDBClientImpl implements TypeDBClient {
    private _isOpen: boolean;

    protected constructor() {
        this._isOpen = true;
    }

    isOpen(): boolean {
        return this._isOpen;
    }

    abstract get databases(): TypeDBDatabaseManagerImpl;

    abstract stub(): TypeDBStub;

    async close(): Promise&lt;void&gt; {
        if (this._isOpen) {
            this._isOpen = false;
        }
    }
}

// connection/core/CoreClient.ts
export class CoreClient extends TypeDBClientImpl {
    private readonly _stub: CoreStub;
    private readonly _databases: TypeDBDatabaseManagerImpl;

    constructor(address: string) {
        super();
        this._stub = new CoreStub(address);
        this._databases = new TypeDBDatabaseManagerImpl(this._stub);
    }

    get databases(): TypeDBDatabaseManagerImpl {
        return this._databases;
    }

    stub(): TypeDBStub {
        return this._stub;
    }

    async close(): Promise&lt;void&gt; {
        await super.close();
        this._stub.close();
    }
}
```
[tab:end]

[tab:Python]
```python
# typedb/connection/client.py
class _TypeDBClientImpl(TypeDBClient):
    def __init__(self):
        pass

    def databases(self) -&gt; _TypeDBDatabaseManagerImpl:
        pass

    def stub(self) -&gt; TypeDBStub:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_tb is not None:
            return False

    def close(self) -&gt; None:
        pass

# typedb/connection/core/client.py
from grpc import Channel, insecure_channel

class _CoreClient(_TypeDBClientImpl):
    def __init__(self, address: str):
        super(_CoreClient, self).__init__()
        self._channel = insecure_channel(address)
        self._stub = _CoreStub(self._channel)
        self._databases = _TypeDBDatabaseManagerImpl(self._stub)

    def databases(self) -&gt; _TypeDBDatabaseManagerImpl:
        return self._databases

    def stub(self) -&gt; _CoreStub:
        return self._stub

    def close(self) -&gt; None:
        super().close()
        self._channel.close()
```
[tab:end]

</div>

Finally, we implement `DatabaseManager`, and `CoreStub` to set up gRPC calls to the server.

<div class="note">
[Important]
You'll need to compile TypeDB's [protocol](https://github.com/vaticle/typedb-protocol) in order to do this.
Most languages have protobuf compilers that you can use to generate a TypeDB protocol library for your language.
</div>

<div class="tabs dark">

[tab:Java]
<!-- test-ignore -->
```java
// api/database/DatabaseManager.java
public interface DatabaseManager {
    void create(String name);
}

// connection/TypeDBDatabaseManagerImpl.java
import com.vaticle.typedb.protocol.CoreDatabaseProto;

public class TypeDBDatabaseManagerImpl implements DatabaseManager {
    private final TypeDBClientImpl client;

    public TypeDBDatabaseManagerImpl(TypeDBClientImpl client) {
        this.client = client;
    }

    @Override
    public void create(String name) {
        stub().databasesCreate(CoreDatabaseProto.CoreDatabaseManager.Create.Req.newBuilder().setName(name).build());
    }

    TypeDBStub stub() {
        return client.stub();
    }
}

// common/rpc/TypeDBStub.java
import com.vaticle.typedb.protocol.CoreDatabaseProto;
import com.vaticle.typedb.protocol.TypeDBGrpc;

public abstract class TypeDBStub {
    public CoreDatabaseProto.CoreDatabaseManager.Create.Res databasesCreate(CoreDatabaseProto.CoreDatabaseManager.Create.Req request) {
        return blockingStub().databasesCreate(request);
    }

    protected abstract TypeDBGrpc.TypeDBBlockingStub blockingStub();
}

// connection/core/CoreStub.java
import com.vaticle.typedb.protocol.TypeDBGrpc;
import io.grpc.ManagedChannel;

public class CoreStub extends TypeDBStub {
    private final ManagedChannel channel;
    private final TypeDBGrpc.TypeDBBlockingStub blockingStub;

    private CoreStub(ManagedChannel channel) {
        super();
        this.channel = channel;
        this.blockingStub = TypeDBGrpc.newBlockingStub(channel);
    }

    public static CoreStub create(ManagedChannel channel) {
        return new CoreStub(channel);
    }

    @Override
    protected TypeDBGrpc.TypeDBBlockingStub blockingStub() {
        return blockingStub;
    }
}
```
[tab:end]

[tab:Node.js]
```typescript
// api/connection/database/TypeDBClient.ts
export interface DatabaseManager {
    create(name: string): Promise&lt;void&gt;;
}

// connection/TypeDBDatabaseManagerImpl.ts
import { CoreDatabaseManager } from "typedb-protocol/core/core_database_pb";

export class TypeDBDatabaseManagerImpl implements DatabaseManager {
    private readonly _stub: TypeDBStub;

    constructor(client: TypeDBStub) {
        this._stub = client;
    }

    public create(name: string): Promise&lt;void&gt; {
        return this._stub.databasesCreate(new CoreDatabaseManager.Create.Req().setName(name));
    }

    stub() {
        return this._stub;
    }
}

// common/rpc/TypeDBStub.ts
import { CoreDatabaseManager } from "typedb-protocol/core/core_database_pb";
import { TypeDBClient } from "typedb-protocol/core/core_service_grpc_pb";

export abstract class TypeDBStub {
    databasesCreate(req: CoreDatabaseManager.Create.Req): Promise&lt;void&gt; {
        return new Promise((resolve, reject) =&gt; {
            this.stub().databases_create(req, (err) =&gt; {
                if (err) reject(new Error(err));
                else resolve();
            })
        });
    }

    abstract stub(): TypeDBClient;
}

// connection/core/CoreStub.ts
import { ChannelCredentials } from "@grpc/grpc-js";
import { TypeDBClient } from "typedb-protocol/core/core_service_grpc_pb";

export class CoreStub extends TypeDBStub {
    private readonly _stub: TypeDBClient;

    constructor(address: string) {
        super();
        this._stub = new TypeDBClient(address, ChannelCredentials.createInsecure());
    }

    stub(): TypeDBClient {
        return this._stub;
    }

    close(): void {
        this._stub.close();
    }
}
```
[tab:end]

[tab:Python]
```python
# typedb/api/connection/database.py
from abc import ABC, abstractmethod

class DatabaseManager(ABC):
    @abstractmethod
    def create(self, name: str) -&gt; None:
        pass

# typedb/connection/database_manager.py
import typedb_protocol.core.core_database_pb2 as core_database_proto

class _TypeDBDatabaseManagerImpl(DatabaseManager):
    def __init__(self, stub: TypeDBStub):
        self._stub = stub

    def create(self, name: str) -&gt; None:
        req = core_database_proto.CoreDatabaseManager.Create.Req()
        req.name = name
        self._stub.databases_create(req)

    def stub(self) -&gt; TypeDBStub:
        return self._stub

# typedb/common/rpc/stub.py
import typedb_protocol.core.core_database_pb2 as core_database_proto
import typedb_protocol.core.core_service_pb2_grpc as core_service_proto

class TypeDBStub(ABC):
    def databases_create(self, req: core_database_proto.CoreDatabaseManager.Create.Req) -&gt; core_database_proto.CoreDatabaseManager.Create.Res:
        return self.stub().databases_create(req)

    def stub(self) -&gt; core_service_proto.TypeDBStub:
        pass

# typedb/connection/core/stub.py
from grpc import Channel
import typedb_protocol.core.core_service_pb2_grpc as core_service_proto

class _CoreStub(TypeDBStub):
    def __init__(self, channel: Channel):
        super(_CoreStub, self).__init__()
        self._channel = channel
        self._stub = core_service_proto.TypeDBStub(channel)

    def stub(self) -&gt; TypeDBStub:
        return self._stub
```
[tab:end]

</div>

At this point, we have all the necessary components to create a database! 
[Run the TypeDB server locally](../0001-typedb/01-start/02-installation.md) and 
create a test function:

<div class="tabs dark">

[tab:Java]
<!-- test-ignore -->
```java
public static void typeDBClientTest() {
    try (TypeDBClient client = TypeDB.coreClient("127.0.0.1:1729")) {
        client.databases().create("typedb");
    }
}
```
[tab:end]

[tab:Node.js]
```typescript
async function typeDBClientTest() {
    try {
        const client = TypeDB.coreClient("127.0.0.1:1729");
        await client.databases().create("typedb");
    } finally {
        client?.close();
    }
}
```
[tab:end]

[tab:Python]
```python
def typedb_client_test():
    with TypeDB.core_client("127.0.0.1:1729") as client:
        client.databases().create("typedb")
```
[tab:end]

</div>

We can verify that the database was created successfully using 
[Console's `database list` command](02-console.md#database-management-commands), or 
by rerunning the test (which will throw an error saying that the database already exists).

That concludes the basics tutorial. The following sections give an overview of the remaining components needed to open 
transactions, run queries, and take the client to 100% completion.

We recommend using one of our existing Clients as a reference, and copying the implementation into your chosen language.

## Session and transaction

To query schema and data, we need to open a Session and Transaction of the appropriate types. For example, you can't 
modify schema in a data session.

A Session is essentially a long-lasting tunnel from client to database. However, we implement that with just simple 
RPC calls - Open and Close. 

Sessions consume server resources, and may hold locks. If a client disconnects (say, by crashing) the server needs a 
way to know. So, we use a pulse mechanism. Every 5 seconds, a TypeDB client sends a Session Pulse to inform the 
server that the client is still alive. If no pulse is received in 30 seconds, the server times out the session, 
freeing up its resources for use elsewhere.

Once a Session is open, we can open a Transaction inside it to read and write to the database. This is implemented 
with a bidirectional streaming RPC. Rather like a websocket, it’s a long-lasting tunnel that allows the client and 
server to talk to each other.

TypeDB clients support multiple layers of concurrency. A Client can have many Sessions, and a Session can have many 
Transactions, and a Transaction can perform many Queries.

![Concurrency Model](../images/client-api/concurrency-model.png)

## Inside a transaction stream

Inside a transaction stream, the client sends requests, and the server is expected to respond to the client's 
requests in a timely manner.

Each request must have the same message type. This is `Transaction.Client`, defined in 
[typedb-protocol](https://github.com/vaticle/typedb-protocol/blob/master/common/transaction.proto):

```protobuf
// typedb-protocol/common/transaction.proto
message Transaction {

  message Client {
    repeated Req reqs = 1;
  }

  message Req {
    bytes req_id = 1;
    map&lt;string, string&gt; metadata = 2;
    oneof req {
      Open.Req open_req = 3;
      Stream.Req stream_req = 4;
      Commit.Req commit_req = 5;
      Rollback.Req rollback_req = 6;
      QueryManager.Req query_manager_req = 7;
      ConceptManager.Req concept_manager_req = 8;
      LogicManager.Req logic_manager_req = 9;
      Rule.Req rule_req = 10;
      typedb.protocol.Type.Req type_req = 11;
      Thing.Req thing_req = 12;
    }
  }
}
```

Each **request message** is suffixed with `.Req`, and has a matching `.Res` (or `.ResPart`) to represent the server's 
response to that message.

Now, there are two basic patterns to the communications; _single_ responses and _streamed_ responses, both of which 
are illustrated below.

![Inside a Transaction Stream](../images/client-api/response-structure.png)

Here, `Define.Req` and `Match.Req` are both types of `QueryManager.Req`, and `Type.Create.Req` and `GetThing.Req` are 
types of `ConceptManager.Req`.

### Handling streamed responses

For requests such as TypeQL Match queries, the responses can be very long, so TypeDB breaks them up into parts.
We issue `Match.Req`, and get back multiple `Match.ResPart`s, which each contain some answers to the query.

Getting all the answers may be costly in terms of server resources, and it can be wasteful if the client exits early.
So we only auto-stream up to a certain limit, called the **prefetch size**, then we send a special message called 
“Continue”.
If the client needs more answers, it should respond with a `Stream.Req`.
That tells the server to continue streaming, and, when there are no answers left, it sends a `Stream.ResPart` 
with `state = DONE`. 

In a client, the Match response is typically represented as a Stream or Iterator. Seeing “DONE” from the server 
signals the end of iteration. The iterator implementation varies a bit by language. In Java, Streams are in-built; 
in Python we use an Iterator, and in NodeJS we use an Async Iterator. Use whatever is most natural in your language.

### Handling concurrent requests

Concurrent queries create a slight complication, since all the responses go down the same gRPC stream. We handle them
by attaching a Request ID (`req_id`) to each request, and, whenever a Request is made, we create a Response 
Collector – essentially a bucket, or queue, that holds responses for this Query.

The queue fills up as answers are received from the server, and it gets emptied as the user iterates over these answers.

### Request batching

Loading bulk data may potentially require millions of INSERT queries, and gRPC can only send so many in a given 
timeframe. To mitigate this, we use request batching - see the `RequestTransmitter` class in any official client.
It collects all requests in a 1ms time window, bundles them into a single gRPC message, and dispatches it. 

## Exploring query answers

The `ConceptMap` objects returned by a TypeQL Match query can contain any type of `Concept`. This `Concept` class 
hierarchy is reflected in TypeDB's client implementation and class structure.

![Concept Hierarchy](../images/client-api/overview_hierarchy.png)

Implementing all concept methods for TypeDB API is not complicated, but it is quite long as there are a 
lot of methods. Concept methods either return single or streamed responses. `ThingType.getInstances` is an example 
of a Streamed Concept method.

## TypeDB Cloud Client

TypeDB Cloud uses clusters of TyperDB servers that run as a distributed network of database servers which communicate 
internally to form a consensus when querying. If one server has an outage, we can recover from the issue by falling 
back to another server. To enable this, TypeDB Client constructs 1 Core client per TypeDB server (cluster node):

![Cluster Client Architecture](../images/client-api/cluster.png)

Suppose we open a Transaction to, say, Node 1, but we don’t get a response.

In TypeDB, that would be a non-recoverable error. In Cluster, the Cluster client simply reroutes the request to a 
different Core client, which sends the request to its linked server. In this way, the client recovers from the 
failure and continues running as normal.

## Rapid testing with BDD

The recommended way to test a TypeDB Client is by using the 
[TypeDB Behaviour spec](https://github.com/vaticle/typedb-behaviour).
It’s written in a language-agnostic syntax named [Gherkin](https://cucumber.io/docs/gherkin/reference/).
Tests consist of named steps. To run the tests in a new client, you just need to implement the steps.
This means you can test your client without having to write a single test!

```gherkin
# To run the test, implement each step: e.g. "connection create database: {name}"
Scenario: commit in a read transaction throws
    When connection create database: typedb
    Given connection open schema session for database: typedb
    When session opens transaction of type: read
    Then transaction commits; throws exception
```

## Conclusion

A client is considered production-ready once it passes all the tests and adheres to the TypeDB architecture.
If you encounter any difficulties along the way, do get in touch with the Vaticle team, preferably on 
[Discord](https://vaticle.com/discord). We're happy to help speed up the development process.
This will also enable us to add your project into the [TypeDB Open Source Initiative](https://typedb.org).
