---
pageTitle: Concept API
keywords: grakn, concept, api
longTailKeywords: grakn concept api, concept api
Summary: Concept Hierarchy in Grakn.
toc: false
---

## Concept Architecture
Anything in Grakn, whether a type or an instance of data, is a [Concept](../04-concept-api/01-concept.md). The diagram below, illustrates how the Concept Superclass is inherited by its direct and indirect descendants.

![Concept Hierarchy](../images/concept-api/overview_hierarchy.png)

**Type** refers to a Concept Type as defined in the [schema](../09-schema/00-overview.md#data-model.md).

**Thing** refers to an instance of data that is an instantiation of a Concept Type.

**Rule** refers to a [Graql Rule](../09-schema/02-rules.md).

<div class="note">
[Important]
The methods called on Concepts are bound to the [transaction](../03-client-api/00-overview#transaction.md) that was used to retrieve the concept initially. As soon as the transaction in question is closed, methods can no longer be called on the retrieved Concepts. To do so, we must retrieve the Concept again with a newly created transaction.
</div>

In the sections that follow, we learn about the methods available on [Concept](../04-concept-api/01-concept.md), [Type](/docs/concept-api/type#type-methods), [EntityType](/docs/concept-api/type#entitytype-methods), [AttributeType](/docs/concept-api/type#attributetype-methods), [RelationType](/docs/concept-api/type#relationtype-methods), [Thing](../04-concept-api/04-thing#thing-methods.md), [Attribute](../04-concept-api/04-thing#attribute-methods.md), [Relation](../04-concept-api/04-thing#relation-methods.md) and [Rule](../04-concept-api/03-rule.md).
