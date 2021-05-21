---
pageTitle: Schema
keywords: typedb, workbase, schema designer
longTailKeywords: typedb design schema, workbase schema designer
Summary: Using Workbase to design a schema.
toc: false
---

<div class = "note">
[Warning]
The schema designer is not yet stable in version 2.0 and has been disabled. To view your schema in the visualiser, please run the following query:

```
match $x sub thing;
```
</div>

## Design a Schema
Workbase allows the visualisation and design of a typedb schema.

### Navigate to the Schema Designer

![schema designer](/docs/images/workbase/schema_btn.png)
[caption: We can access the schema designer by clicking the top left **schema desinger** icon.]


### Define New Entity Type
<div class="slideshow">

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-entity-btn.png)[body:end]
[footer:start]We can use the left bar to define new entity type.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-entity-name-supertype.png)[body:end]
[footer:start]We can specify the name of the entity and the super type.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-entity-has.png)[body:end]
[footer:start]We can specifiy the attributes that the entity can have, given that the attribute type has already been defined.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-entity-plays.png)[body:end]
[footer:start]We can specify the roles the entity type can play, given that the relation for those roles have been defined.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-entity-submit.png)[body:end]
[footer:start] Create the type by clikcing on **Submit**. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-entity-result.png)[body:end]
[footer:start] [footer:end]
[slide:end]

</div>

### Define New Attribute Type
<div class="slideshow">

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-attribute-btn.png)[body:end]
[footer:start]We can use the left bar to deine new attribute type.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-attribute-name-valuetype.png)[body:end]
[footer:start]We can specify the name of the attribute and the data type.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-attribute-has.png)[body:end]
[footer:start]We can specifiy the attributes that the attribute can have, given that the attribute type has already been defined. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-attribute-plays.png)[body:end]
[footer:start]We can specify the roles the attribute type can play, given that the relation for those roles have been defined. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-attribute-submit.png)[body:end]
[footer:start] Create the type by clikcing on **Submit**. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-attribute-result.png)[body:end]
[footer:start] [footer:end]
[slide:end]

</div>

### Define New Relation Type
<div class="slideshow">

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-relation-btn.png)[body:end]
[footer:start]We can use the left bar to deine new relation type.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-relation-name-supertype.png)[body:end]
[footer:start]We can specify the name of the relation, the super type and the role players.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-relation-has.png)[body:end]
[footer:start]We can specifiy the attributes that the relation can have, given that the attribute type has already been defined. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-relation-plays.png)[body:end]
[footer:start]We can specify the roles the relation type can play, given that the relation for those roles have been defined. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-relation-submit.png)[body:end]
[footer:start] Create the type by clikcing on **Submit**. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_define-relation-result.png)[body:end]
[footer:start] [footer:end]
[slide:end]

</div>

### Manage Attribute Types
<div class="slideshow">

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_attribute-panel.png)[body:end]
[footer:start]We may add an exisiting attribute type to a schema concept type by selecting it and clicking on **Add Attribute Types** in the right bar.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_attribute-select.png)[body:end]
[footer:start]Select the attribute we want to add.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_attribute-add.png)[body:end]
[footer:start]Click **Add**. [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_attribute-added.png)[body:end]
[footer:start] [footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_attribute-remove.png)[body:end]
[footer:start]We can remove an attribute by clicking on the **trash** icon next to the attribute. [footer:end]
[slide:end]
</div>

### Display Settings
<div class="slideshow">

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_settings-tab.png)[body:end]
[footer:start]Navigate to the **Display Settings** by clicking on the **gear** icon.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_settings-display-panel.png)[body:end]
[footer:start]We can toggle schema concept types to show or hide them.[footer:end]
[slide:end]

[slide:start]
[body:start]![schema designer](/docs/images/workbase/schema_settings-display-toggled.png)[body:end]
[footer:start] [footer:end]
[slide:end]

</div>

### Delete

![schema designer](/docs/images/workbase/schema_delete.png)
[caption: We may delete an existing schema concept type by right-clicking on the node and clicking **Delete**.]
