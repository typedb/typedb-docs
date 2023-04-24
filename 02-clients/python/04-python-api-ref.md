---
pageTitle: Python API Reference
keywords: typedb, client, python
longTailKeywords: typedb python client, typedb client python, client python, python client
Summary: API Reference of TypeDB Client Python.
templatePath: 02-clients/references/
toc: true
---

# Python API reference

## Query section

{% include api/generic.html data=site.data.03_client_api.references.typedb language="python" %}

### Client methods

{% include api/generic.html data=site.data.03_client_api.references.client language="python" %}

### Session methods

{% include api/generic.html data=site.data.03_client_api.references.session language="python" %}

### Options methods

{% include api/generic.html data=site.data.03_client_api.references.options language="python" %}

### Transaction methods

{% include api/generic.html data=site.data.03_client_api.references.transaction language="python" %}

### Query methods

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="python" %}

## Response section

{% include api/answers.html data=site.data.03_client_api.references.answer language="python" %}

### Concept methods

`Concept` is inherited and extended by [`Type`](#type-methods) and [`Data`](#data-methods).

{% include api/generic.html data=site.data.04_concept_api.references.concept language="python" %}

{% include api/generic.html data=site.data.04_concept_api.references.concept_manager language="python" %}

### Future methods

{% include api/generic.html data=site.data.03_client_api.references.query_future language="python" %}

### Type methods

`Type` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.type language="python" %}

#### ThingType methods

<!-- #todo Update the Thing keyword as soon as API implementation update will change it --->

`ThingType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing_type language="python" %}

#### EntityType methods

`EntityType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity_type language="python" %}

#### RelationType methods

`RelationType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation_type language="python" %}

##### RoleType methods

`RoleType` has all the [`Type` methods](#type-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.role_type language="python" %}

#### AttributeType methods

`AttributeType` has all the [`ThingType` methods](#thingtype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute_type language="python" %}

##### BooleanAttributeType methods

`BooleanAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.boolean_attribute_type language="python" %}

##### LongAttributeType methods

`LongAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.long_attribute_type language="python" %}

##### DoubleAttributeType methods

`DoubleAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.double_attribute_type language="python" %}

##### StringAttributeType methods

`StringAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.string_attribute_type language="python" %}

##### DateTimeAttributeType methods

`DateTimeAttributeType` has all the [`AttributeType` methods](#attributetype-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.datetime_attribute_type language="python" %}

### Rule methods

{% include api/generic.html data=site.data.04_concept_api.references.rule language="python" %}

{% include api/generic.html data=site.data.04_concept_api.references.logic_manager language="python" %}

### Data methods

`Data` has all the [`Concept` methods](#concept-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.thing language="python" %}

#### Entity methods

`Entity` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.entity language="python" %}

#### Attribute methods

`Attribute` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.attribute language="python" %}

#### Relation methods

`Relation` has all the [`Data` methods](#data-methods) plus what follows.

{% include api/generic.html data=site.data.04_concept_api.references.relation language="python" %}
