---
title: Hierarchical
keywords:
tags: []
summary: ""
permalink: /docs/reasoning/hierarchical
---

### Type Inference
The type inference is based on a simple traversal along the `sub` links. Every instance of a given concept type is automatically classified as an (indirect) instance of all (possibly indirect) supertypes of that type. For example, whenever `customer sub human` is in the schema, every instance of `customer` will be retrieved on the query `match $x isa human`.

Similarly for roles, every instance playing a given role is inferred to also play all its (possibly indirect) super-roles. <!--For example, whenever `inst` plays the role of wife in a relationship of the type `marriage`, the system will infer that `inst` plays also the role of `partner1` in that relationship, given the schema from Figure 2.-->

The type inference is set ON by default when querying Grakn.
