---
pageTitle: Type
keywords: grakn, type, api, methods
longTailKeywords: grakn type, type methods, grakn type methods, grakn entity type methods, grakn attribute type methods, grakn relation type methods, grakn role methods
Summary: Methods available on Type objects.
toc: true
---

## Type Methods
`Type` has all the [`Concept` methods](../04-concept-api/01-concept.md) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.type language="python" %}
[tab:end]

</div>

## EntityType Methods
`EntityType` has all the [`Type` methods](#type-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="python" %}
[tab:end]

</div>

## AttributeType Methods
`AttributeType` has all the [`Type` methods](#type-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="python" %}
[tab:end]

</div>

## BooleanAttributeType
`BooleanAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="python" %}
[tab:end]

</div>

## LongAttributeType
`LongAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="python" %}
[tab:end]

</div>

## DoubleAttributeType
`DoubleAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="python" %}
[tab:end]

</div>

## StringAttributeType
`StringAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="python" %}
[tab:end]

</div>

## DateTimeAttributeType
`DateTimeAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="python" %}
[tab:end]

</div>

## RelationType Methods
`RelationType` has all the [`Type` methods](#type-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="java" %}
[tab:end]

[tab:Javascript]
{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="javascript" %}
[tab:end]

[tab:Python]
{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="python" %}
[tab:end]

</div>

## Role Methods
`Role` has all the [`Concept` methods](#type-methods) plus what follows.

<div class="tabs light" data-no-parse>

[tab:Java]
<div class="note">
[Important]
At the moment, `Role` inherits an intermediary class which, for the sake of simplicity, has not been documented. Therefore, besides the `Concept` methods, Role inherits the following methods from the `Type` class.
- [label();](?tab=java#retrieve-label)
- [type.label(Label.of(label));](?tab=java#rename-label)
- [sup();](?tab=java#retrieve-direct-supertype)
- [sup(Type type);](?tab=java#change-direct-supertype)
- [sups();](?tab=java#retrieve-all-supertypes)
- [subs();](?tab=java#retrieve-all-subtypes)
</div>

{% include api/generic.html data=site.data.04_concept_api.references.role language="java" %}
[tab:end]

[tab:Javascript]
<div class="note">
[Important]
At the moment, `Role` inherits an intermediary class which, for the sake of simplicity, has not been documented. Therefore, besides the `Concept` methods, Role inherits the following methods from the `Type` class.
- [label();](?tab=javascript#retrieve-label)
- [type.label(Label.of(label));](?tab=javascript#rename-label)
- [sup();](?tab=javascript#retrieve-direct-supertype)
- [sup(Type type);](?tab=javascript#change-direct-supertype)
- [sups();](?tab=javascript#retrieve-all-supertypes)
- [subs();](?tab=javascript#retrieve-all-subtypes)
</div>
{% include api/generic.html data=site.data.04_concept_api.references.role language="javascript" %}
[tab:end]

[tab:Python]
<div class="note">
[Important]
At the moment, `Role` inherits an intermediary class which, for the sake of simplicity, has not been documented. Therefore, besides the `Concept` methods, Role inherits the following methods from the `Type` class.
- [label();](?tab=python#retrieve-label)
- [type.label(Label.of(label));](?tab=python#rename-label)
- [sup();](?tab=python#retrieve-direct-supertype)
- [sup(Type type);](?tab=python#change-direct-supertype)
- [sups();](?tab=python#retrieve-all-supertypes)
- [subs();](?tab=python#retrieve-all-subtypes)
</div>
{% include api/generic.html data=site.data.04_concept_api.references.role language="python" %}
[tab:end]

</div>