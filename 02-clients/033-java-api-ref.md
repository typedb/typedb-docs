---
pageTitle: Java API Reference
keywords: typedb, client, java
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: API Reference of TypeDB Client Java.
templatePath: 02-clients/references/
toc: true
---

# Java API reference

## Query section

{% include api/generic.html data=site.data.03_client_api.references.typedb language="java" %}

### Client methods

{% include api/generic.html data=site.data.03_client_api.references.client language="java" %}

### Session methods

{% include api/generic.html data=site.data.03_client_api.references.session language="java" %}

### Options methods

{% include api/generic.html data=site.data.03_client_api.references.options language="java" %}

### Transaction methods

{% include api/generic.html data=site.data.03_client_api.references.transaction language="java" %}

### Query methods

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="java" %}

## Response section

{% include api/answers.html data=site.data.03_client_api.references.answer language="java" %}

### Concept methods

`Concept` is inherited and extended by [`Type`](#type-methods) and [`Data`](#data-methods).

{% include api/generic.html data=site.data.04_concept_api.references.concept language="java" %}

{% include api/generic.html data=site.data.04_concept_api.references.concept_manager language="java" %}

### Future methods

{% include api/generic.html data=site.data.03_client_api.references.query_future language="java" %}

### Type methods

`Type` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.type language="java" %}

#### ThingType methods

<!-- #todo Update the Thing keyword as soon as API implementation update will change it --->

`ThingType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing_type language="java" %}

#### EntityType methods

`EntityType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="java" %}

#### RelationType methods

`RelationType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="java" %}

##### RoleType methods

`RoleType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.role_type language="java" %}

#### AttributeType methods

`AttributeType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="java" %}

##### BooleanAttributeType methods

`BooleanAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="java" %}

##### LongAttributeType methods

`LongAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="java" %}

##### DoubleAttributeType methods

`DoubleAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="java" %}

##### StringAttributeType methods

`StringAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="java" %}

##### DateTimeAttributeType methods

`DateTimeAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="java" %}

### Rule methods

{% include api/generic.html data=site.data.04_concept_api.references.rule language="java" %}

{% include api/generic.html data=site.data.04_concept_api.references.logic_manager language="java" %}

### Data methods

`Data` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing language="java" %}

#### Entity methods

`Entity` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity language="java" %}

#### Attribute methods

`Attribute` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute language="java" %}

#### Relation methods

`Relation` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation language="java" %}

