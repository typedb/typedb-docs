---
pageTitle: New TypeDB Clients
keywords: grpc, protobuf, client, driver
longTailKeywords: typedb client, typedb driver, client development, new client, client implementation
Summary: Guide to writing clients in new languages
---

## Introduction

Vaticle maintains a small number of official client drivers: Java, Python, and NodeJS. All our other client drivers are community-built.

It's possible to build a client for any language! A TypeDB client fundamentally is a lightweight frontend
to the TypeDB server. This page is a guide for the components and protocols that need to be implemented.

## gRPC

[gRPC](https://grpc.io/) is the network call framework that TypeDB uses. A TypeDB client needs a gRPC client library to communicate with the server. Most languages have gRPC libraries.

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

## TypeDB Protocol

[Protocol Buffers](https://developers.google.com/protocol-buffers) is the encoding used to serialise network messages.
Proto definition files can be compiled into server-side and client-side libraries using a Protobuf Compiler.
In our case, we only need client-side library compilation. Most languages have Protobuf compilers available.

TypeDB's protobuf definitions can be found at https://github.com/vaticle/typedb-protocol.
During development, it's sufficient to manually copy-paste from this repository and do a one-time compilation.
A more reliable method is to import the Protocol repo via a package manager and compile it at build time.
TypeDB's build system, [Bazel](https://bazel.build/), offers one approach. If you'd like to use a different package manager, 
the TypeDB team may also be able to help by setting up a distribution channel for your language's compiled protobuf files.
If this is the case, please get in touch.

## Client Code Architecture

TypeDB’s official client drivers adhere to a common architecture. This greatly reduces the workload of
maintaining them, so we also recommend community contributions to follow the same basic structure.

This diagram shows all the packages (directories) in Client Java and their dependency graph:
![Client Package Structure](../images/client-api/package-structure.png)

The entry point is the root package, in this case named `client-java`.
`api` is where we declare all the available client methods – basically all the interfaces.
`core` holds the basic building blocks: client, session, transaction.
Then we have `query` for querying, `concept` for Concept API, `logic` for reasoning.

There are many places you could start building a client. In this guide, we start by attempting to make a single gRPC call to TypeDB.

## Entry point: Create a Channel and a Service Stub


