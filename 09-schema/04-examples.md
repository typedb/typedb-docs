---
pagetitles: Schema Examples
keywords: typeql, schema
longTailKeywords: typeql schema, typeql define query, typeql type hierarchy, typeql concepts, typeql define entity, typeql define relation, typeql define attribute, typeql schema definition
Summary: Additonal schema examples to accelerate your learning and development on TypeDB. 
---

## How to Use These Example Schemas

These example schema files, which allow you to explore how data in a particular domain could be modelled in TypeDB, can be picked up and used by anyone looking to explore the database for complex data.

Building a TypeDB knowledge graph is fairly simple as TypeDB's hypergraph structure represents the real world much more intuitively than columns and rows of data. The examples below are meant to enable any developer to get started building with TypeDB, faster.

1. Review the modelling example highlights or jump right to the schema files and click to download
2. Download [TypeDB](http://docs.vaticle.com/docs/running-typedb/install-and-run#download-and-install-typedb) and [TypeDB Workbase](https://grakn.ai/download#workbase)
3. Select an example below and download the .gql file via github link
4. Load .gql file via [TypeDB Console](http://docs.vaticle.com/docs/running-typedb/console)
5. Open TypeDB Workbase and [visualise your schema](http://docs.vaticle.com/docs/workbase/schema-designer)
6. Iterate on the model, clean your keyspace, and re-load into TypeDB - rinse and repeat as needed

## Modelling Examples

### Unary Relation
To define a unary relation, where a `thing` is in a relation referring itself.

<div class="tabs dark">

[tab:Social Network]

<!-- test-delay -->
```typeql
define

person sub entity,
    plays group-member,
    plays group-owner,
    plays group-membership-requester,
    plays group-membership-respondant;

request sub relation,
    relates approved-subject,
    relates requester,
    relates respondent;

group-membership-request sub request,
    has approved-date,
    relates approved-group-membership as approved-subject,
    relates group-membership-requester as requester,
    relates group-membership-respondent as respondent;
```

[tab:end]

[tab:Phone Calls]
<!-- test-delay -->
```typeql
person sub entity,
    plays customer,
    plays caller,
    plays callee,
    has first-name,
    has last-name,
    has phone-number,
    has city,
    has age;

call sub relation,
    relates caller,
    relates callee,
    has started-at,
    has duration;
```

[tab:end]

[tab:BioTypeDB COVID]
<!-- test-delay -->
```typeql
gene sub fully-formed-anatomical-structure,
    has gene-symbol,
    has entrez-id,
    has ensembl-gene-stable-id,
    has ensembl-xref,
    has gene-name,
    plays expressing-gene,
    plays encoding-gene,
    plays transcribing-gene,
    plays mentioned,
    plays associated-gene,
    plays target-gene,
	plays associated-virus-gene,
	plays located-gene,
	plays inhibited,
	plays inhibiting;

inhibition sub relation,
	relates inhibited,
	relates inhibiting,
	plays mentioned-genes-relation,
	has sentence-text;
```
[tab:end]
</div>

### Rule to infer a relation
To build a rule that infers a new relation type based on an existing set of data. 

<div class="tabs dark">

[tab:Financial Services]

<!-- test-delay -->
```typeql
define

organisation-owns-subsidiary-bond sub rule,
when {
	$c isa organisation; $c2 isa organisation; $c != $c2; 
	$c3 isa organisation; $c3 != $c; 
	$e isa bond; 
	$jv (jv-owned: $c3, jv-owner: $c2, jv-owner: $c) isa joint-venture; 
	$r2 (owner: $c3, owned: $e) isa owns; 
}, then {
	(owner: $c, owned: $e) isa indirect-owns;
	};
```

[tab:end]

[tab:Customer 360]
<!-- test-delay -->
```typeql
define

negative-product-recommendation sub rule, 
when {
	$p isa person;
	$pr isa product;
	$1 (receiving: $p, promoted: $pr) isa promotion, has opens $o;
	$2 (receiving: $p, promoted: $pr) isa promotion, has opens $o2;
	$1 != $2; 
	$o == 0; 
	$o2 == 0;
}, then {
	(negative-recommended-product: $pr, negative-recommended-to: $p) isa negative-recommendation;
};
```

[tab:end]

</div>

### Rule to infer an attribute
To build a rule that infers a new relation type based on an existing set of data. 

<div class="tabs dark">

[tab:BioTypeDB COVID]

<!-- test-delay -->
```typeql
define

gene-disease-association-and-gene-protein-encoding-protein-disease-association sub rule,
when {
    $g isa gene;
    $pr isa protein;
    $di isa disease;
    $r1 (associated-disease: $di, associated-gene: $g) isa gene-disease-association;
    $r2 (encoding-gene: $g, encoded-protein: $pr) isa gene-protein-encoding;
}, then {
    (associated-protein: $pr, associated-disease: $di) isa protein-disease-association;
};
```

[tab:end]

[tab:Role Player Game]
<!-- test-delay -->
```typeql
define 

task-can-not-begin-if-it-is-already-started sub rule,
when {
	$task isa campaign-task, has started true;
}, then {
	$task has can-begin false;
};

task-can-not-begin-if-it-lacks-required-tech sub rule,
when {
	$task isa campaign-task, has has-required-techs false;
}, then {
	$task has can-begin false;
};
```

[tab:end]

[tab:Financial Services]
<!-- test-delay -->
```typeql
define

when-risks-then-high-combined-risk sub rule, 
when {
	$war isa war, has risk-level 'high'; 
	$civ-un isa civil-unrest, has risk-level 'high';
	$ter isa terrorism, has risk-level 'high'; 
	$risk (individual-risk: $war, individual-risk: $civ-un, individual-risk: $ter) isa risk;
}, then {
	$risk has risk-level 'high';
};
```
[tab:end]
</div>

### Chained Rule 
To infer multiple new facts based on inferred concepts it is necessary to chain rules, as a rule can only infer one new fact per conclusion.  

<div class="tabs dark">

[tab:Financial Services]
<!-- test-delay -->
```typeql
define 

owns-subsidiary sub rule,
when {
	$b isa bank; $b2 isa bank; $b != $b2;
	$real-estate-corporate isa real-estate-corporate; 
	$r1 (owner: $b, owned: $b2) isa owns; 
	$r2 (owner: $b2, owned: $real-estate-corporate) isa owns; 
}, then {
	(owner: $b, owned: $real-estate-corporate) isa indirect-owns; 
	};

bank-cyber-attack sub rule,
when {
	$b isa bank; 
	$real-estate-corporate isa real-estate-corporate;
	$attack-campaign isa attack-campaign;
	$r1 (owner: $b, owned: $real-estate-corporate) isa indirect-owns;
	$r2 (attacked: $real-estate-corporate, attacker-campaign: $attack-campaign) isa cyber-attack; 
}, then {
	(attacked: $b, attacker-campaign: $attack-campaign) isa cyber-attack;
};

cyber-crime-risk sub rule,
when {
	$b isa bank; 
	$attack-campaign isa attack-campaign;
	$cyber-crime isa cyber-crime;
	$r2 (risk-subject: $attack-campaign, risk-value: $cyber-crime) isa risk-exposure;
	$r1 (attacked: $b, attacker-campaign: $attack-campaign) isa cyber-attack;
}, then {
	(risk-value: $cyber-crime, risk-subject: $b) isa risk-exposure;
};
```

[tab:end]

[tab:Customer 360]

<!-- test-delay -->
```typeql
define

product-recommendation sub rule,
when {
	$p isa person;
	$pr isa product;
	$w isa web-page;
	$sess isa session; 
	$0 (active-session: $sess, active-device: $dev, active-person: $p) isa device-session; 
	$1 (visiting: $sess, visited-website: $w) isa website-visit;
	$2 (promoting-page: $w, promoted: $pr) isa website-promotion;
	$post isa post;
	$sp (promoting-post: $post, promoted: $pr) isa social-promotion;
	$com isa comment;
	$reply (replied-to: $post, replied-by: $p, reply-content: $com) isa reply;
	$liking (reacted-to: $post, reacted-by: $p) isa liking; 
}, then {
	(recommended-product: $pr, recommended-to: $p) isa recommendation;
};

mortgage-marriage-recommendation sub rule,
when {
	$p isa person;
	$p2 isa person;
	$2 ($p2, $p) isa marriage; 
	$pr isa mortgage;
	$1 (recommended-product: $pr, recommended-to: $p2) isa recommendation;
}, then {
	(recommended-product: $pr, recommended-to: $p) isa recommendation;
};
```

[tab:end]

</div>

### Events that overlap
Modelling `periodic-event`s where `start-date` of one event is before the `end-date` of another.  

<div class="tabs dark">

[tab:Social Network]

<!-- test-delay -->
```typeql
define

event-overlapping sub relation,
    relates overlapped-event;

events-overlap sub rule,
when {
    $e1 isa periodic-event;
    $e1 has start-date $sd1, has end-date $ed1;
    $e2 isa periodic-event;
    $e2 has start-date $sd2, has end-date $ed2;
    $sd2 > $sd1;
    $sd2 < $ed1;
    $e1 != $e2;
}, then {
    (overlapped-event: $e1, overlapped-event: $e2) isa event-overlapping;
};
```
[tab:end]

</div>

### Life Events
Modelling various life events within the context of a Social Network.   

<div class="tabs dark">

[tab:Birth]

<!-- test-delay -->
```typeql
define

location-of-everything sub relation,
    abstract,
    relates located-subject,
    relates subject-location;

location-of-birth sub location-of-everything,
    relates located-birth as located-subject,
    relates birth-location as subject-location;

birth sub relation,
    has birth-date,
    relates birthed-child,
    plays located-birth,
    plays mutual-birth;

person sub entity,
    plays birthed-child,
    plays mutual-birthed-child;

location sub entity,
    plays birth-location,
    plays mutual-birth-location;
```
[tab:end]

[tab:Residency]

<!-- test-delay -->
```typeql
define

location-of-everything sub relation,
    abstract,
    relates located-subject,
    relates subject-location;

location-of-residence sub location-of-everything,
    relates located-residence as located-subject,
    relates residence as subject-location;

residency sub periodic-event,
    relates resident,
    plays located-residence,
    plays mutual-residency;

person sub entity,
    plays resident,
    plays mutual-resident;

location sub entity,
    plays residence,
    plays mutual-residence;
```
[tab:end]

[tab:Travel]

<!-- test-delay -->
```typeql
define

location-of-everything sub relation,
    abstract,
    relates located-subject,
    relates subject-location;

location-of-travel sub location-of-everything,
    relates located-travel as located-subject,
    relates travel-location as subject-location;

travel sub periodic-event,
    relates traveler,
    plays located-travel,
    plays mutual-travel;

person sub entity,
    plays traveler,
    plays mutual-traveler;

location sub entity,
    plays travel-location,
    plays mutual-travel-location;

```
[tab:end]

[tab:Education]

<!-- test-delay -->
```typeql
define

location-of-school sub location-of-everything,
    relates located-school as located-subject,
    relates school-location as subject-location;

	school-course-enrollment sub periodic-event,
		has graduated,
		has score,
		relates student,
		relates enrolled-course,
		relates enrolling-school,
		plays mutual-course-enrollment;

	school sub entity,
		key name,
		has ranking,
		plays offerring-school,
		plays located-school,
		plays enrolling-school,
		plays mutual-school;

	school-course sub entity,
		key title,
		plays offered-course,
		plays enrolled-course;

	person sub entity,
		plays student,
		plays schoolmate,
		plays coursemate;

	location sub entity,
		plays school-location;

```
[tab:end]

</div>

### Business Operations
Modelling various business scenarios.    

<div class="tabs dark">

[tab:Employement]

<!-- test-delay -->
```typeql
define

person sub entity,
    plays employee,
    plays mutual-employee;

work-position sub entity,
    key title,
    plays offered-position,
    plays mutual-position;

organisation sub entity,
    key name,
    key registration-number,
    plays office-owner,
    plays employer,
    plays mutual-organisation;

periodic-event sub relation,
    abstract,
    has start-date,
    has end-date,
    plays overlapped-event;

employment sub periodic-event,
    key reference-id,
    has salary,
    relates employer,
    relates employee,
    relates offered-position,
    plays mutual-employment;

```
[tab:end]

[tab:Employement in Common]

<!-- test-delay -->
```typeql
define

person sub entity,
    plays employee,
    plays mutual-employee;

work-position sub entity,
    key title,
    plays offered-position,
    plays mutual-position;

organisation sub entity,
    key name,
    key registration-number,
    plays office-owner,
    plays employer,
    plays mutual-organisation;

employment sub periodic-event,
    key reference-id,
    has salary,
    relates employer,
    relates employee,
    relates offered-position,
    plays mutual-employment;

employment-mutuality sub relation,
		relates mutual-employee,
		relates mutual-employment,
		relates mutual-organisation;

people-work-at-the-same-organisation sub rule,
when {
    $e1 (employee: $p1, employer: $o) isa employment;
    $e2 (employee: $p2, employer: $o) isa employment;
    $p1 != $p2;
}, then {
    (mutual-employee: $p1, mutual-employee: $p2, mutual-organisation: $o, mutual-employment: $e1, mutual-employment: $e2) isa employment-mutuality;
};

work-position-mutuality sub relation,
    relates mutual-employee,
    relates mutual-employment,
    relates mutual-position;

people-work-at-the-same-position sub rule,
when {
    $e1 (employee: $p1, offered-position: $p) isa employment;
    $e2 (employee: $p2, offered-position: $p) isa employment;
    $p1 != $p2;
}, then {
    (mutual-employee: $p1, mutual-employee: $p2, mutual-position: $p, mutual-employment: $e1, mutual-employment: $e2) isa work-position-mutuality;
};
```
[tab:end]

[tab:Facilities Ownership]

<!-- test-delay -->
```typeql
define

organisation sub entity,
    key name,
    key registration-number,
    plays office-owner,
    plays employer,
    plays mutual-organisation;

office sub entity,
    key registration-number,
    plays owned-office,
    plays located-office;

location sub entity,
    plays office-location;

ownership sub relation,
    relates owner,
    relates owned;
    
location-of-everything sub relation,
    abstract,
    relates located-subject,
    relates subject-location;

location-of-office sub location-of-everything,
    relates located-office as located-subject,
    relates office-location as subject-location;

```
[tab:end]

</div>

### Language
Modelling languages in various contexts.  

<div class="tabs dark">

[tab:Spoken Language]

<!-- test-delay -->
```typeql
define

person sub entity,
    plays speaker,
    plays mutual-speaker;
    
language sub attribute,
    value string,
    plays spoken,
    plays mutual-language;

speaking-of-language sub relation,
    relates speaker,
    relates spoken,
    plays mutual-language-speaking;
    
speaking-language-mutuality sub relation,
    relates mutual-speaker,
    relates mutual-language-speaking,
    relates mutual-language;

people-speak-the-same-language sub rule,
when {
    $sol1 (speaker: $p1, spoken: $l) isa speaking-of-language;
    $sol2 (speaker: $p2, spoken: $l) isa speaking-of-language;
    $p1 != $p2;
}, then {
    (mutual-speaker: $p1, mutual-speaker: $p2, mutual-language: $l, mutual-language-speaking: $sol1, mutual-language-speaking: $sol2) isa speaking-language-mutuality;
};
```
[tab:end]

[tab:Content Language]

<!-- test-delay -->
```typeql
define

content sub attribute,
    value string,
    has language;
    
language sub attribute,
    value string,
    plays spoken,
    plays mutual-language;

post sub entity,
		abstract,
		key identifier,
		plays permitted-content,
		plays shared-content,
		plays replied-to,
		plays tagged-in,
		plays reacted-to;

	status-update sub post,
		has content,
		plays attached-to;

	comment sub post,
		has content,
		plays reply-content,
		plays attached-to;
```

[tab:end]
</div>

### Content Access
Modelling content permissions using TypeDB Rules.   

<div class="tabs dark">

[tab:Access Permissions]

<!-- test-delay -->
```typeql
define

public-permission sub rule,
when {
    (shared-content: $sc) isa public-sharing;
    $pu isa public-user;
}, then {
    (permitted-content: $sc, permission-grantee: $pu) isa permitted-to-see;
};

friends-permission sub rule,
when {
    (shared-content: $sc, shared-by: $sb) isa friends-sharing;
    (friend: $sb, $f) isa friendship;
}, then {
    (permitted-content: $sc, permission-grantee: $f) isa permitted-to-see;
};

inclusive-permissions sub rule,
when {
    (shared-content: $sc, shared-with: $sw) isa inclusive-sharing;
}, then {
    (permitted-content: $sc, permission-grantee: $sw) isa permitted-to-see;
};

friends-excluded-permission sub rule,
when {
    (shared-content: $sc, shared-by: $sb, hidden-from: $hf) isa friends-with-exclusion-sharing;
    (friend: $sb, $f) isa friendship;
    $f != $hf;
}, then {
    (permitted-content: $sc, permission-grantee: $f) isa permitted-to-see;
};

private-permission sub rule,
when {
    (shared-content: $sc, shared-by: $sb) isa private-sharing;
    $pu isa public-user;
}, then {
    (permitted-content: $sc, permission-grantee: $sb) isa permitted-to-see;
};

author-permission sub rule,
when {
    (shared-content: $sc, shared-by: $sb) isa sharing;
    $pu isa public-user;
}, then {
    (permitted-content: $sc, permission-grantee: $sb) isa permitted-to-see;
};
```

[tab:end]

</div>

## Example Schema Files

### Social Network

Here we have modelled a schema for a social network. We get examples of:

- unary relation
- ternary relation
- nested relation
- n-ary relation
- type hierarchy
- TypeDB Rule
- attributes asigned to a relation

[Download](https://raw.githubusercontent.com/vaticle/examples/master/schemas/social-network-schema.gql)

### Public Transit System

Here we have modelled a schema for a transit network. We get examples of:

- role player hierarchy 
- unary relation
- ternary relation
- geographic location of a `station`
- route modelling

[Download](https://raw.githubusercontent.com/vaticle/examples/master/schemas/tube-network-schema.gql)

### BioTypeDB - Disease Network

Here we have modelled a disease network for COVID-19 research. We get examples of:

- role player hierarchy 
- unary relation
- ternary relation
- nested relation
- n-ary relation
- type hierarchy 
- TypeDB Rule
- attributes asigned to a relation

[Download](https://raw.githubusercontent.com/vaticle/biotypedb-covid/master/Schema/biotypedb-covid.gql)

### Modelling A Phone Call Network

Here we have modelled a schema for a network of phone calls between persons. We get examples of:

- uniary relations
- attributes asigned to a relation

[Download](https://raw.githubusercontent.com/vaticle/examples/master/schemas/phone-calls-schema.gql)

### Customer 360

Here we have modelled a schema for a Customer 360 use case within the context of a financial institution. We get examples of:

- role player hierarchy 
- unary relation
- ternary relation
- nested relation
- n-ary relation
- type hierarchy 
- TypeDB Rule
- attributes asigned to a relation

[Download](https://raw.githubusercontent.com/vaticle/examples/master/schemas/customer-360-schema.gql)

### Financial Services

Here we have modelled a schema for a financial services use case within the context of risk exposure. We get examples of:

- role player hierarchy 
- unary relation
- ternary relation
- nested relation
- n-ary relation
- type hierarchy 
- TypeDB Rule
- attributes asigned to a relation

[Download](https://raw.githubusercontent.com/vaticle/examples/master/schemas/financial-services-schema.gql)


### Role Player Game 

Here we have modelled a schema for a role player game with campaigns, . We get examples of:

- role player hierarchy 
- unary relation
- ternary relation
- nested relation
- n-ary relation
- type hierarchy 
- TypeDB Rule
- attributes asigned to a relation

[Download](https://raw.githubusercontent.com/vaticle/examples/master/schemas/xcom-schema.gql)
