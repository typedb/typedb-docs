---
title: Rule-based
keywords:
tags: []
summary: ""
permalink: /docs/reasoning/rule-based
---

The rule-based inference exploits a set of user-defined datalog rules and is conducted by means of the  reasoner built natively into Grakn. Every rule is declared as an instance of a built-in Grakn type `rule`.

A rule is an expression of the form `when G1 then G2`, where `G1` and `G2` are a pair of Graql patterns. Whenever the "when" pattern `G1` is found in the data, the "then" pattern `G2` can be assumed to exist. For example:

```graql
define
  location sub entity;

  located-in sub relationship,
    relates located-subject, relates subject-location;

  transitive-location
    when {
      ($x, $y) isa located-in;
      ($y, $z) isa located-in;
    }
    then {
      (located-in:$x, located-x:$z) isa located-in;
    };

```

<br /> <img src="/images/knowledge-model9.png" style="width: 600px;" alt="
An image showing that King's Cross is 'located-in' London and London is 'located-in' the UK - therefore King's Cross is
'located-in' the UK
"/> <br />

<br />

The rule above expresses that, if `$x` has a `located-in` relationship with `$y`, and `$y` has a `located-in` relationship with `$z`, then `$x` has a `located-in` relationship with `$z`. As a concrete example: King's Cross is in London, and London is in the UK, so one can infer that King's Cross is in the UK.

The rule-based inference is currently set ON by default when querying Grakn. It can be deactivated if needed. For more detailed documentation on rules see [Graql Rules](../building-schema/defining-rules).

