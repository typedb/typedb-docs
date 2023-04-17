---
pageTitle: Java API Reference
keywords: typedb, client, java
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: API Reference of TypeDB Client Java.
templatePath: 02-clients/references/
toc: true
---

# Java API reference

## Query

{% include api/generic.html data=site.data.03_client_api.references.typedb language="java" %}

### Client

{% include api/generic.html data=site.data.03_client_api.references.client language="java" %}

### Session

{% include api/generic.html data=site.data.03_client_api.references.session language="java" %}

### Options

{% include api/generic.html data=site.data.03_client_api.references.options language="java" %}

### Transaction

{% include api/generic.html data=site.data.03_client_api.references.transaction language="java" %}

### TypeQL

{% include api/generic.html data=site.data.03_client_api.references.typeql language="java" %}

### Query

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="java" %}

## Response

{% include api/answers.html data=site.data.03_client_api.references.answer language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.query_future language="java" %}

### Concept Methods

`Concept` is inherited and extended by [`Type`](#type-methods) and [`Data`](#data-methods).

{% include api/generic.html data=site.data.04_concept_api.references.concept language="java" %}

{% include api/generic.html data=site.data.04_concept_api.references.concept_manager language="java" %}

### Type Methods

`Type` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.type language="java" %}

#### ThingType Methods

<!-- #todo Update the Thing keyword as soon as API implementation update will change it --->

`ThingType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing_type language="java" %}

#### EntityType Methods
`EntityType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="java" %}

#### AttributeType Methods

`AttributeType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="java" %}

#### BooleanAttributeType Methods

`BooleanAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="java" %}

#### LongAttributeType Methods

`LongAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="java" %}

#### DoubleAttributeType Methods

`DoubleAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="java" %}

#### StringAttributeType Methods

`StringAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="java" %}

#### DateTimeAttributeType Methods

`DateTimeAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="java" %}

#### RelationType Methods

`RelationType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="java" %}

#### RoleType Methods

`RoleType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.role_type language="java" %}

### Rule Methods

{% include api/generic.html data=site.data.04_concept_api.references.rule language="java" %}

{% include api/generic.html data=site.data.04_concept_api.references.logic_manager language="java" %}

### Data Methods

`Data` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing language="java" %}

#### Entity Methods

`Entity` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity language="java" %}

#### Attribute Methods

`Attribute` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute language="java" %}

#### Relation Methods

`Relation` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation language="java" %}

