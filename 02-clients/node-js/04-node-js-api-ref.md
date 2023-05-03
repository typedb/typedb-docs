---
pageTitle: Node.js API Reference
keywords: typedb, client, node.js
longTailKeywords: typedb node.js client, typedb client node.js, client node.js, node.js client
Summary: API Reference of TypeDB Client Node.js.
templatePath: 02-clients/references/
toc: true
---

# Node.js API reference

## Query section

{% include api/generic.html data=site.data.03_client_api.references.typedb language="javascript" %}

### Client methods

{% include api/generic.html data=site.data.03_client_api.references.client language="javascript" %}

### Session methods

{% include api/generic.html data=site.data.03_client_api.references.session language="javascript" %}

### Options methods

{% include api/generic.html data=site.data.03_client_api.references.options language="javascript" %}

### Transaction methods

{% include api/generic.html data=site.data.03_client_api.references.transaction language="javascript" %}

### Query methods

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="javascript" %}

## Response section

{% include api/answers.html data=site.data.03_client_api.references.answer language="javascript" %}

### Concept methods

`Concept` is inherited and extended by [`Type`](#type-methods) and [`Data`](#data-methods).

{% include api/generic.html data=site.data.04_concept_api.references.concept language="javascript" %}

{% include api/generic.html data=site.data.04_concept_api.references.concept_manager language="javascript" %}

### Future methods

{% include api/generic.html data=site.data.03_client_api.references.query_future language="javascript" %}

### Type methods

`Type` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.type language="javascript" %}

#### ThingType methods

<!-- #todo Update the Thing keyword as soon as API implementation update will change it --->

`ThingType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing_type language="javascript" %}

#### EntityType methods

`EntityType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="javascript" %}

#### RelationType methods

`RelationType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="javascript" %}

##### RoleType methods

`RoleType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.role_type language="javascript" %}

#### AttributeType methods

`AttributeType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="javascript" %}

##### BooleanAttributeType methods

`BooleanAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="javascript" %}

##### LongAttributeType methods

`LongAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="javascript" %}

##### DoubleAttributeType methods

`DoubleAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="javascript" %}

##### StringAttributeType methods

`StringAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="javascript" %}

##### DateTimeAttributeType methods

`DateTimeAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="javascript" %}

### Rule methods

{% include api/generic.html data=site.data.04_concept_api.references.rule language="javascript" %}

{% include api/generic.html data=site.data.04_concept_api.references.logic_manager language="javascript" %}

### Data methods

`Data` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing language="javascript" %}

#### Entity methods

`Entity` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity language="javascript" %}

#### Attribute methods

`Attribute` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute language="javascript" %}

#### Relation methods

`Relation` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation language="javascript" %}
