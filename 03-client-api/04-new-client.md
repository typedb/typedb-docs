---
pageTitle: New Grakn Clients
keywords: grpc, protobuf, client, driver
longTailKeywords: grakn client, grakn driver, client development, new client, client implementation
Summary: Guide to writing clients in new languages
---

## Introduction

Creating a client for our chosen language is straightforward! This page is a guide for the components and
protocols that need to be implemented.

A Grakn client fundamentally is a lightweight frontend to the Grakn server. Almost all operations are actually
handled on the server, and executed via [gRPC](https://grpc.io/). So, to get started, we'll need to confirm
that gRPC and the underlying [protobuf](https://github.com/google/protobuf) messages support our language of choice.
Many languages also have non-official support for these protocols. Finally, we need to double check for compatible language versions.

## Depending on Grakn gRPC and Protobuf Definitions
For development purposes, it may be sufficient to manually compile and copy-paste Grakn's 
[protobuf definitions](https://github.com/graknlabs/grakn/tree/master/protocol). 

A more reliable method is to stay in sync with protocol changes via a package manager.
Grakn's build system is [Bazel](https://bazel.build/), and offers one approach. If we'd would like to use a different package manager, 
the Grakn team may also be able to help by setting up a distribution channel for our chosen language's compiled protobuf files.
In this case, please get in touch!

 
## Architecture

As touched on in the [Overview page](00-overview.md), Grakn clients have the following central components the user interacts with

* `GraknClient`
* `Session`
* `Transaction`
* `Concept`
* `Answer`

To maintain consistency across languages, all Grakn clients should aim to implement this interface.

User interactions flow through these components:

* A `GraknClient` is instantiated with a URI and creates a GRPC channel to the server.
* The `GraknClient` spawns one or more `Session`, which are long-lived connections to a specific keyspace in Grakn.
* The `Session` is used to create short-lived `Transaction` objects which allow interacting with data.
* Queries on `Transaction` generally return lazy iterators of `Answer` types, which can contain `Concept` instances.
* Objects from the `Concept` hierarchy can be thought of client-side representations of instances on the server and expose their own API.

And this is the `Concept` hierarchy that should be implemented - note that it is an extension of the user-facing, simpler hierarchy seen
[here](../04-concept-api/00-overview.md):
```
                             Concept
                            /        \
                          /            \
                        /                \
                      /                    \
         SchemaConcept                      Thing
          /      |    \                    /  |   \
         /       |     \                 /    |     \
        /        |      \              /      |       \
     Rule      Type       Role     Entity   Attribute   Relation
             /  |   \
            /   |     \
           /    |       \
          /     |         \
EntityType  AttributeType  RelationType
```

The API each `Concept` type exposes is documented in the [ConceptAPI](../04-concept-api/00-overview.md). Each method in the ConceptAPI
corresponds to an RPC call to the server. So, the chief remaining concern is understanding the Grakn RPC protocol.

## RPC Protocol

### gRPC Summary
Key advantages of gRPC are:
* Support for bidirectional streaming via HTTP 2.0
* Definition of services and messages using protocol buffer syntax and definitions
* Compilation to a variety of language stubs

Grakn's protocol doesn't use any complex components of gRPC like channel multiplexing. Instead, it takes full advantage
of the ability to create complex and strongly typed messages that are streamed between the client and the server.

### Understanding the Grakn gRPC protocol

The full protocol definition is in Grakn's [git repository](https://github.com/graknlabs/grakn/tree/master/protocol).
To become familiar with the protocol structure, let's look at the following excerpt from `Session.proto`. This section examines 
the process of getting attributes of a specific value from a transaction - the relevant RPC messages are marked with `==>`.

```proto
service SessionService {
    ...
    rpc transaction (stream Transaction.Req) returns (stream Transaction.Res);
}
...

message Transaction {
    message Req {
        map<string, string> metadata = 1000;
        oneof req {
            Open.Req open_req = 1;
            Commit.Req commit_req = 2;
            Query.Req query_req = 3;
==>            Iter.Req iterate_req = 4;
            GetSchemaConcept.Req getSchemaConcept_req = 5;
            GetConcept.Req getConcept_req = 6;
==>            GetAttributes.Req getAttributes_req = 7;
            ...
         }
    }
    message Res {
            oneof res {
                Open.Res open_res = 1;
                Commit.Res commit_res = 2;
==>                Query.Iter query_iter = 3;
                Iter.Res iterate_res = 4;
                GetSchemaConcept.Res getSchemaConcept_res = 5;
                GetConcept.Res getConcept_res = 6;
==>                GetAttributes.Iter getAttributes_iter = 7;
                   ...
            }
    }
    ...
    message Iter {
        message Req {
            int32 id = 1;
        }
        message Res {
            oneof res {
                bool done = 1;
                Query.Iter.Res query_iter_res = 2;
==>                GetAttributes.Iter.Res getAttributes_iter_res = 3;
                Method.Iter.Res conceptMethod_iter_res = 4;
            }
        }
    }
    ...
    message GetAttributes {
        message Req {
            ValueObject value = 1;
        }
        message Iter {
            int32 id = 1;
            message Res {
                Concept attribute = 1;
            }
        }
    }
```

This definition states there is one `transaction` RPC endpoint, which is a bi-directional streams that takes messages
of type `Transaction.Req` and returns messages of type `Transaction.Res`. These types permit a variety of different 
bodies, and one can trace through the definition to determine how to build messages, and what the expected responses are.
To understand what exactly this means, let's look at a detailed example.


### Get Attributes by Value 
Since all Grakn clients are implemented similarly, the following piece of Python is representative:
<!-- test-example social_network_create_new_client_a.py -->
```python
# make sure we've run `pip3 install grakn-client` and have Grakn running
from grakn.client import GraknClient, DataType
client = GraknClient(uri="localhost:48555")
with client.session(keyspace="social_network") as session:
    with session.transaction().read() as read_transaction:   
        answer_iterator = read_transaction.get_attributes_by_value("Canada", DataType.STRING)
client.close()
```

Here, the client attempts to retrieve all the attributes that have string values called `"Canada"` in the keyspace `"social_network"`. 
The first gRPC message created is a a `Transaction.Req` from `Session.proto`, which needs to have the `getAttributes_req` field populated.
This, in turn has the type `GetAttributes.Req`, which has a single field called `value`. `value` is a `ValueObject`, 
which is defined in the `Concept.proto` file (excerpt below):

```proto
message Concept {
    string id = 1;
    BASE_TYPE baseType = 2;

    enum BASE_TYPE {
        ...
        ATTRIBUTE_TYPE = 3;
        ...
    }
    ...
}

message ValueObject {
    oneof value {
        string string = 1;
        bool boolean = 2;
        int32 integer = 3;
        int64 long = 4;
        float float = 5;
        double double = 6;
        int64 date = 7; // time since epoch in milliseconds
    }
}
```

In this case, the `ValueObject` needs to the string field populated with `“Canada”`.

In Python, printing the full constructed message should produce something like this:
```python
{                            # type Transaction.Req
  getAttributes_req {        # type GetAttributes.Req
    value {                  # type ValueObject (from Concept.proto)
      string : "Canada"
    }
  }
}
``` 

gRPC implementations differ in how to compose these messages together, so check the relevant docs
(these [tutorials](https://developers.google.com/protocol-buffers/docs/tutorials) are a good starting point).
In python, each of these compound messages needs to be instantiated and embedded using `CopyFrom` or `MergeFrom` 
([Python Protobuf docs](https://developers.google.com/protocol-buffers/docs/pythontutorial)).


The message that is returned is a `Transaction.Req`. But which field is populated? 
We can get this from the naming conventions: It should be the one with type `GetAttributes.Iter`, with a single field called `id`.

```python
{                            # type Transaction.Res
  getAttributes_iter {       # type GetAttributes.iter
    id: 1
  }
}
```

### Lazy Responses
One key reason for using bidirectional streaming is lazy evaluation of queries. The id returned above represents an iterator on the server,
which can be repeatedly requested to retrieve the actual `Attribute` instances. This can be wrapped up on the client side as a local iterator. 
For instance, in Python, the next element in an iterator is retrieved by calling `next(attribute_iterator)`

<!-- test-example social_network_create_new_client_b.py -->
```python
# make sure we've run `pip3 install grakn-client` and have Grakn running
from grakn.client import GraknClient, DataType
client = GraknClient(uri="localhost:48555")
with client.session(keyspace="social_network") as session:
    with session.transaction().read() as read_transaction:   
        answer_iterator = read_transaction.get_attributes_by_value("Canada", DataType.STRING)
        for attr in answer_iterator:
            print(attr)
client.close()
```

The `next(attribute_iterator)` needs create a new gRPC message with the following format:
```python
{                            # type Transaction.Req
  iterate_req {              # type Iter.Req
    id : 1                   # or whatever the iterator ID is
  }
}
```

Which returns
```python
{                              # type Transaction.Req
  iterate_res {                # type Iter.Res
    getAttributes_iter_res {   # type GetAttributes.Iter.Res
      concept {                # Type Concept (from Concept.proto)
        id : "V...",
        baseType: 3
    }      
  }
}
```

This is the definition of the first Concept! However, it has arrived as a gRPC message, and
should be unpacked into a local object and presented to the user. Specifically, the `baseType` signals which
class from the `Concept` hierarchy should be instantiated - here it should be `Attribute`. The base type mapping
can be defined from the `Concept.BaseType` enum in `Concept.proto`. 

The next time `next(attribute_iterator)` is called, repeat the process of making an `iterate_req`
and unpacking the returned message into a local object.
 
 
### gRPC Definition Structure

Finally, here is the layout of the protocol. Most interactions happen via messages defined in `Session.proto`.
The sub-messages used in later interactions are further defined in `Answer.proto` and `Concept.proto`. `Keyspace.proto`
is separate - operations on keyspaces do not require sessions or transactions to be active.


```
protocol/
├── keyspace
│   └── Keyspace.proto          # RPC endpoint for manually listing, creating, and deleting keyspaces
└── session
    ├── Session.proto           # Entry point for sessions, transactions, and iterating responses
    ├── Answer.proto            # Response messsages, e.g. maps, sets, lists of Concepts, among others
    └── Concept.proto           # Messages implementing the ConceptAPI (methods directly on concepts)
```

## Tests

As the main means of interacting with Grakn, testing is an especially important part of the clients. Luckily, 
although not few, these tests are generally quite short. It's recommend to mirror the testing performed in the
official clients such as [Python](https://github.com/graknlabs/client-python/tree/master/tests/integration) or 
[Node](https://github.com/graknlabs/client-nodejs/tree/master/tests/service). Most of these
should be simple to translate!


## Reach out!
If you're planning on implementing a client for custom language, the Grakn team love to hear about it, and are happy
to help iron out misunderstandings and hopefully, get your work into the official Grakn repositories!