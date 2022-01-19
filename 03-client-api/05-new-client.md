---
pageTitle: New TypeDB Clients
keywords: grpc, protobuf, client, driver
longTailKeywords: typedb client, typedb driver, client development, new client, client implementation
Summary: Guide to writing clients in new languages
---

## Introduction

Creating a client for our chosen language is straightforward! A TypeDB client fundamentally is a lightweight frontend
to the TypeDB server. This page is a guide for the components and protocols that need to be implemented.

## Prerequisites

- [gRPC](https://grpc.io/): TypeDB's network call framework. A TypeDB client needs a gRPC client library to communicate with the server. Most languages have gRPC libraries.
- [Protocol Buffers](https://developers.google.com/protocol-buffers): The encoding used to serialise network messages. Again, most languages already have libraries to handle Protocol Buffers.

## 

## Depend on TypeDB Protocol Definitions

For development purposes, it may be sufficient to manually compile and copy-paste TypeDB's 
[protobuf definitions](https://github.com/vaticle/protocol).

A more reliable method is to stay in sync with protocol changes via a package manager.
TypeDB's build system is [Bazel](https://bazel.build/), and offers one approach. If we'd would like to use a different package manager, 
the TypeDB team may also be able to help by setting up a distribution channel for our chosen language's compiled protobuf files.
In this case, please get in touch!

_This guide is a work in progress and will be updated with further details soon._
