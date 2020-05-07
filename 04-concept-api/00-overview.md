---
pageTitle: Concept API
keywords: grakn, concept, api
longTailKeywords: grakn concept api, concept api
Summary: Concept Hierarchy in Grakn.
toc: false
---

## Concept Architecture
Anything in Grakn, whether a concept type or a data instance, is a [Concept](../04-concept-api/01-concept.md). The diagram below, illustrates how the Concept superclass is inherited by its direct and indirect descendants.

![Concept Hierarchy](../images/concept-api/overview_hierarchy.png)

**Type** refers to a Concept Type as defined in the [schema](../09-schema/00-overview.md#grakn-data-model).

**Thing** refers to an instance of data that is an instantiation of a Concept Type.

**Rule** refers to a [Graql Rule](../09-schema/03-rules.md).

<div class="note">
[Important]
In order to run Concept API methods, a live [transaction](../03-client-api/00-overview.md#transaction) is required (to execute the method RPCs). Concepts returned from a method will be bound to the same transaction as the concept that was used to call the method.

Since Grakn 1.7.0, queries return some additional information about attribute values and types so that they do not need to be retreived using separate RPCs. Most clients will instead return a `Local` concept that is limited to retrieving this data. In order to make concept RPC calls, a `Remote` concept can be created from the `Local` one. See the client specific documentation for more details.
</div>

In the sections that follow, we learn about the methods available on [Concept](../04-concept-api/01-concept.md), [Type](../04-concept-api/02-type.md#type-methods), [EntityType](../04-concept-api/02-type.md#entitytype-methods), [AttributeType](../04-concept-api/02-type.md#attributetype-methods), [RelationType](../04-concept-api/02-type.md#relationtype-methods), [Thing](../04-concept-api/04-thing.md#thing-methods), [Attribute](../04-concept-api/04-thing.md#attribute-methods), [Relation](../04-concept-api/04-thing.md#relation-methods) and [Rule](../04-concept-api/03-rule.md).
