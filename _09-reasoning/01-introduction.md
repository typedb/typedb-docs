---
title: Introduction
keywords: setup, getting started, basics
tags: [getting-started, reasoning, graql]
summary: "Introduction to Grakn's inference strategy"
permalink: /docs/reasoning/introduction
---

## Rule and Sub-Type Inference

Inference is a process of extracting implicit information from explicit data. Grakn supports two inference mechanisms:

1. type inference, based on the semantics of the `sub` hierarchies included in the schema
2. rule-based inference involving user-defined IF-THEN rules.

Both mechanisms can be employed when querying the knowledge graph with Graql, thus supporting retrieval of both explicit and implicit information at query time.

### Type Inference
The type inference is based on a simple traversal along the `sub` links. Every instance of a given concept type is automatically classified as an (indirect) instance of all (possibly indirect) supertypes of that type. For example, whenever `customer sub human` is in the schema, every instance of `customer` will be retrieved on the query `match $x isa human`.

Similarly for roles, every instance playing a given role is inferred to also play all its (possibly indirect) super-roles. <!--For example, whenever `inst` plays the role of wife in a relationship of the type `marriage`, the system will infer that `inst` plays also the role of `partner1` in that relationship, given the schema from Figure 2.-->

The type inference is set ON by default when querying Grakn.