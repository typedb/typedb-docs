---
pageTitle: Negation
keywords: typeql, query, pattern, statement, variable, negation, not
longTailKeywords: typeql patterns, typeql statements, typeql variables, negation, not
Summary: Working with negation blocks in patterns.
---

## Queries with negation

Oftentimes we encounter situations where we would like to form queries with the use of negation.
Examples of such queries include:

a) List all people that were unemployed in the last 6 months

b) Show me text-only timelines (no videos or images) 

c) All single people who have posted a photo in a forum

The intuitive meaning of a negated pattern is that of a complement. However, a relation complement is not a clearly defined term as it requires the definition of a domain of values with respect to which the complement is computed. Even in this case, we end up with an infinite relation which leaves the projection or join operations unapplicable. As a result, we understand pattern negation in terms of computation of set differences. The set-difference semantics
are different to the perhaps familiar semantics of _Negation-as-Failure_ of Prolog and in this chapter, we will attempt to provide a clear explanation of the meaning
of pattern negation in TypeDB. 

Let us consider the relation of unemployment which can be trivially understood as the absence of employment. We define negation blocks by enclosing patterns with
curly braces and preceding them with a `not` keyword:

```
not {
    ...
};
```

Therefore, to retrieve people that are unemployed we want to express:

```
Person($x), ¬Employment($x, employer: $y)
```

i.e. we look for the following TypeQL pattern:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    not {
        (employee: $x, employer: $y) isa employment;
    };
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"), 
    not(
        var().rel("employee", var("x")).rel("employer", var("y")).isa("employment")
    )
);
```
[tab:end]
</div>

Please note that the `$y` variable inside the negation block is not bound. This is of great importance when discussing the meaning of negation. 
If we were to interpret the query using the simple complement semantics we would arrive at a conclusion that unemployed people are people for which there exists 
a company that doesn't hire them - it would get evaluated to all `($x, $y)` pairs where `$x` is a person and `$y` isa a company that is not 
in an employment relation with `$x`. What we do instead is we interpret the negation block as some relation of arity equal to the number of variables that are bound
to non-negated statements. This imposes a requirement of at least one variable in the negation block being bound to a variable outside the block.
Here our only bound variable is `$x`. Consequently we can think of the query as:

```
Person($x), ¬SomeRelation($x)
SomeRelation($x) :- Employment(employee: $x, employer: $y)
```

In this way, we have no problems defining the projection or join operations as these are handled by the native rule semantics. Consequently, we can proceed with the set difference
semantics unambiguously. As a result, the unemployment is evaluated according to our expectation of unemployment as an absence of being part of any employment - from the
set of people we subtract the set of people being in employment relations. Consequently, as a user the only thing we need to type is our query pattern:

```typeql
{
    $x isa person;
    not {
        (employee: $x, employer: $y) isa employment;
    };
}
```

The variables in the negation block are local to the negation block. Consequently, executing the query:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
    $x isa person;
    not {
        (employee: $x, employer: $y) isa employment;
    };
get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
    var("x").isa("person"), 
    not(
        var()
            .rel("employee", var("x"))
            .rel("employer", var("y"))
            .isa("employment")
    )
).get("x");
```
[tab:end]
</div>

will yield a list of concepts assigned to the `$x` variable.

Should we decide that our unemployment pattern is a common one, we might decide to express it via a rule. In the case when the set of bound variables has only one element, it is more convenient to define it in terms of a type. 
Defining the unemployment in terms of a rule and the freshly introduced negation block we can then write: 

<div class="tabs dark">

[tab:TypeQL]
```typeql
define rule unemployment:
    when {
        $x isa person;
        not{
            (employee: $x, employer: $y) isa employment;
        };
    } then {
        $x has unemployed true;
    };
```
[tab:end]

[tab:Java]
```java
TypeQLDefine query = TypeQL.define(
    rule("unemployment")
        .when(
            and(
                var("x").isa("person"),
                not(
                    var().rel("employee", "x").rel("employer", "y").isa("employment")
                )
            )
        )
        .then(
            var("x").has("unemployed", true)
        )
);
```
[tab:end]
</div>

Consequently, our unemployment query pattern simply becomes:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    $x isa unemployed;
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"), 
    var("x").isa("unemployed")
);
```
[tab:end]
</div>

Negation blocks are not tied to relations. We are free to define our patterns inside the negation blocks as long as they are conjunctive. For example, we can use negation
blocks to perform exclusions, e.g. the query pattern to list all non-English speaking employees can read:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    (employee: $x) isa employment;
    (speaker: $x, language: $y) isa fluency;
    not { $y "English";};
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var().rel("employee", var("x")).isa("employment"),
    var()
        .rel("speaker", var("x"))
        .rel("language", var("y"))
        .isa("fluency"),
    not(var("y").eq("English"))
);
```
[tab:end]
</div>

We shall now see how we can form more complex patterns with negation. Let's say we want to find people that are orphans:

```
Person($x), ¬Parentship($x, father: $y), ¬Parentship($x, mother: $y)
```

To express that in TypeQL, we require two negation blocks:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"),
    not(
        var()
            .rel(var("x"))
            .rel("father", var("y"))
            .isa("parentship")
    ),
    not(
        var()
            .rel(var("x"))
            .rel("mother", var("y"))
            .isa("parentship")
    )
);
```
[tab:end]
</div>

which is equivalent to having two extra specific types in the schema:

<div class="tabs dark">

[tab:TypeQL]
```typeql
define

person-with-a-father sub entity;
person-with-a-mother sub entity;
```
[tab:end]

[tab:Java]
```java
TypeQLDefine query = TypeQL.define(
    type("person-with-a-father").sub("entity"),
    type("person-with-a-mother").sub("entity")
);
```
[tab:end]
</div>

and then defining a pattern:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    not { $x isa person-with-a-father;};
    not { $x isa person-with-a-mother;};
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"),
    not(var("x").isa("person-with-a-father")),
    not(var("x").isa("person-with-a-mother"))
);
```
[tab:end]
</div>


Now let's look at how we arrive at the answers if we execute this as a match query. To do this we will go through
the set difference computation procedure. Let's define a set `P` to be the set of all people, i.e. a set that is the answer set to a query:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x isa person; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = match(var("x").isa("person")).get("x");
```
[tab:end]
</div>
 
a set `F` as the set of people having a father, i. e. a set that is the answer set of a query: 

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x isa person-with-a-father; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = match(var("x").isa("person-with-a-father")).get("x");
```
[tab:end]
</div>

and finally a set `M` as the set of people having a mother which can be defined in terms of a query:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x isa person-with-a-mother; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = match(var("x").isa("person-with-a-mother")).get("x");
```
[tab:end]
</div>

We can illustrate the relationships between the sets with a suitable Venn diagram:

![Calculating the P \ F \ M set difference](/docs/images/pattern/pfm.png)

Consequently, our set of answers of our match pattern is defined as `A = P \ F \ M`. As a result, from the set of all people we subtract those who have a father and those who have a mother.
Please note that the scope of variables in a negation block is local to the negation block. As a result, the above pattern does not look for people that do not have a mother and a father that is the same person.

Now let's say we have three people, Alice (A), Bob (B) and Charlie (C). Consequently, our set `P` reads:

```
P = {Alice, Bob, Charlie}
```

Additionally, let's say we know that the following two `parentship` relations hold:

```
Parentship(child: Alice, father: Bob)
Parentship(child: Bob, mother: Charlie)
```

i.e. Bob is the father of Alice and Charlie is the mother of Bob.

This results in our sets `F` and `M` being defined as:

```
F = {Alice}
M = {Bob}
```

Consequently, the final result of the match query:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"),
    not(
        var().rel(var("x")).rel("father", var("y")).isa("parentship")
    ),
    not(
        var().rel(var("x")).rel("mother", var("y")).isa("parentship")
    )
);
```
[tab:end]
</div>

will only have the Charlie concept as the result obtained by computing the set difference:

```
A = P \ F \ M = {Charlie}
```

Now let's complicate things a little and see what happens if we bind the `$y` variable for parents, i. e. if we consider a query pattern:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    $y isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern =and(
    var("x").isa("person"),
    var("y").isa("person"), 
    not(
        var().rel(var("x")).rel("father", var("y")).isa("parentship")
    ),
    not(
        var().rel(var("x")).rel("mother", var("y")).isa("parentship")
    )
);
```
[tab:end]
</div>

Upon inspection, we can see that in this case our three sets are different. Let's define them as `P'`, `M'` and `F'`.
The first difference is that an element of each set is a pair (2-tuple). Our set of people `P` corresponds to the answer set of a match query:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
$x isa person;
$y isa person;
get $x, $y;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
    var("x").isa("person"),
    var("y").isa("person")
).get("x", "y");
```
[tab:end]
</div>

As a result, we have (abbreviating the names for clarity):

```
P' = { 
        (A, A), (A, B), (A, C),
        (B, A), (B, B), (B, C),
        (C, A), (C, B), (C, C)
}
```

Now the set `F'` is a set of pairs `{($x, $y)}` such that the concepts in the pair are connected via `parentship` relation with the concept assigned to `$y` variable playing the role of a father. 
Similarly, the set `M'` is a set of pairs `{($x, $y)}` such that the concepts in the pair are connected via `parentship` relation with the concept assigned to `$y` variable playing the role of a mother. 
Consequently we have:

```
F' = {(A, B)}
M' = {(B, C)}
```

Now, executing our query pattern as an ordinary match-get query:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    $y isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"),
    var("y").isa("person"), 
    not(
        var().rel(var("x")).rel("father", var("y")).isa("parentship")
    ),
    not(
        var().rel(var("x")).rel("mother", var("y")).isa("parentship")
    )
);
```
[tab:end]
</div>

will yield the following concept pairs mapped to `$x` and `$y` variables:

```
A' = P' \ F' \ M' =
{ 
        (A, A), (A, C),
        (B, A), (B, B), 
        (C, A), (C, B), (C, C)
}
```

However! If we now do a projection onto the `$x` variable to compare the results with our previous query variant where 
the `$y` variable is unbounded, i.e. if we execute:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
    $x isa person;
    $y isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
    var("x").isa("person"),
    var("y").isa("person"),
    not(
        var().rel(var("x")).rel("father", var("y")).isa("parentship")
    ),
    not(
        var().rel(var("x")).rel("mother", var("y")).isa("parentship")
    )
).get("x");
```
[tab:end]
</div>

we will get the following concepts in return:

```
A' = P' \ F' \ M' | x = {A, B, C}
```

which is clearly different to the anticipated result of `A = {C}` - our answer set is not a set of orphans, instead it is a projection from a set of people pairs where pairs playing in a `parentship` relation are excluded.
As a result, extra care should be taken and thought given when formulating queries with negation blocks.

One might be tempted to put the two negation blocks into one. Let's look at the outcome of that. If we define:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    not { 
        ($x, father: $y) isa parentship;
        ($x, mother: $z) isa parentship;
    };
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"),
    and(
        not(
            and(
                var().rel(var("x")).rel("father", var("y")).isa("parentship"),
                var().rel(var("x")).rel("mother", var("y")).isa("parentship")
            )
        )
   )
);
```
[tab:end]
</div>

noting that this time we need to pick a fresh variable for mother as we are in the same negation block. The meaning of this pattern is the following. From all people,
remove the people that have both a mother and a father. As a result, our answer set will contain people that have at most one parent.

We can go further than that. Negation blocks in queries can be nested. Consequently, if we wanted to find people whose father is unemployed we can write something
like this:

<div class="tabs dark">

[tab:TypeQL]
```typeql
{
    $x isa person;
    not { 
        ($x, father: $y) isa parentship;
        not { ($y) isa employment; };
    };
}
```
[tab:end]

[tab:Java]
```java
Pattern pattern = and(
    var("x").isa("person"),
    not(
        and(
            var()
                .rel(var("x"))
                .rel("father", var("y"))
                .isa("parentship"),
            not(var().rel(var("y")).isa("employment"))
        )
    )
);
```
[tab:end]
</div>

Please note, nesting of negation blocks is only allowed in queries, but not in rules.

## Negation blocks: DOs and DONTs

Please note, the following restrictions apply to negation blocks:
- for each negation block in a query, at least one variable in the negation block must be bound to a statement outside of the negation block.
This ensures that set difference operations are performed on sets that are not disjoint
- variables in negation blocks are local to the block they are defined in


## Negation in rules
As we have already mentioned, we can use negation blocks within rules.
 
However, when inserting negation blocks in rules, currently the following restrictions apply:
- all restrictions applying to queries with negation blocks
- only conjunctive statements are allowed within rule negations (i.e. no nested `not` or `or` statements)
- rules with negations may not contradict themselves (i.e. recurse back to themselves, even indirectly. An error will be thrown if this is possible.)
 
We will illustrate the use of negation with rules with a graphical example.

Let us define a network of nodes with possible edges between nodes:

<div class="tabs dark">

[tab:TypeQL]
```typeql
define

traversable sub entity,
    plays edge:from,
    plays edge:to,
    plays reachable:from,
    plays reachable:to,
    plays indirect-edge:from,
    plays indirect-edge:to;


node sub traversable;

edge sub relation, relates from, relates to;
```
[tab:end]

[tab:Java]
```java
TypeQLDefine query = TypeQL.define(
    type("traversable").sub("entity").plays("edge", "from").plays("edge", "to"),
    type("node").sub("traversable"), 
    type("edge").sub("relation").relates("from").relates("to")
);
```
[tab:end]
</div>

Then we can define two nodes as being reachable if there exists an edge between them:

<div class="tabs dark">

[tab:TypeQL]
```typeql
define

reachable sub relation, relates from, relates to;
rule reachabilityA:
    when {
        (from: $x, to: $y) isa edge;
    } then {
        (from: $x, to: $y) isa reachable;
    };

rule reachabilityB:
    when {
        (from: $x, to: $z) isa edge;
        (from: $z, to: $y) isa reachable;
    } then {
        (from: $x, to: $y) isa reachable;
    };
```
[tab:end]

[tab:Java]
```java
TypeQLDefine query = TypeQL.define(
    type("reachable").sub("relation").relates("from").relates("to"),
    rule("reachabilityA")
        .when(
           and(var().rel("from", "x").rel("to", "y").isa("edge"))
        )
        .then(
            var().rel("from", "x").rel("to", "y").isa("reachable")
        ),
    rule("reachabilityB")
        .when(
            and(
                var().rel("from", "x").rel("to", "z").isa("edge"),
                var().rel("from", "z").rel("to", "y").isa("reachable")
            )
        )
        .then(
            var().rel("from", "x").rel("to", "y").isa("reachable")
        )        
);
```
[tab:end]
</div>

Consequently, with the use of negation we can define edges that are indirect:

<div class="tabs dark">

[tab:TypeQL]
```typeql
define

indirect-edge sub relation, relates from, relates to;
rule indirect-edge-rule:
    when {
        (from: $x, to: $y) isa reachable;
        not {(from: $x, to: $y) isa edge;};
    } then {
        (from: $x, to: $y) isa indirect-edge;
    };
```
[tab:end]

[tab:Java]
```java
TypeQLDefine query = TypeQL.define(
    type("indirect-edge").sub("relation").relates("from").relates("to"),
    rule("indirect-edge-rule")
        .when(
            and(
                var().rel("from", "x").rel("to", "y").isa("reachable"),
                not(
                    var().rel("from", "x").rel("to", "y").isa("edge")
                )
            )
        )
        .then(
            var().rel("from", "x").rel("to", "y").isa("indirect-edge")
        )
);
```
[tab:end]
</div>

We can mark the unreachable nodes by defining the following rule:

<div class="tabs dark">

[tab:TypeQL]
```typeql
define

unreachable sub relation, relates from, relates to;
traversable sub entity,
    plays unreachable:from,
    plays unreachable:to;
rule unreachability-rule:
    when {
        $x isa node;
        $y isa node;
        not {(from: $x, to: $y) isa reachable;};
    } then {
        (from: $x, to: $y) isa unreachable;
    };
```
[tab:end]

[tab:Java]
```java
TypeQLDefine query = TypeQL.define(
    type("unreachable").sub("relation").relates("from").relates("to"),
    type("traversable").sub("entity").plays("unreachable", "from").plays("unreachable", "to"),
    rule("unreachability-rule")
        .when(
            and(
                var("x").isa("node"),
                var("y").isa("node"),
                not(
                    var().rel("from", "x").rel("to", "y").isa("unreachable")
                )
            )
        )
        .then(
            var().rel("from", "x").rel("to", "y").isa("reachable")
        )
);
```
[tab:end]
</div>

Please note the explicit addition of the `node` types in the body of the rule. This is to ensure the boundedness condition
is satisfied as well as to maintain the expected meaning of the `unreachable` relation.
