---
pageTitle: Java query builder
keywords: typedb, client, java, install, repository
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: Tutorial for TypeDB Client Java.
---

# Java query builder

The Java query builder library can be used to programmatically construct TypeQL queries with native Java code.

To use TypeQL, we first add it as a dependency to our `pom.xml`. 

<div class="note">
[Important]
Don't forget to replace the `{version}` placeholder with exact version of the library.
</div>

The latest version of `typeql-lang` can be found in the 
[Vaticle's public Maven repository](https://repo.vaticle.com/#browse/browse:maven:com%2Fvaticle%2Ftypeql%2Ftypeql-lang).

```xml
<repositories>
    <repository>
        <id>repo.vaticle.com</id>
        <url>https://repo.vaticle.com/repository/maven/</url>
    </repository>
</repositories>
<dependencies>
    <dependency>
        <groupId>com.vaticle.typeql</groupId>
        <artifactId>typeql-lang</artifactId>
        <version>{version}</version>
    </dependency>
</dependencies>
```

Then we import `TypeQL`.

<!-- test-ignore -->
```java
import com.vaticle.typeql.lang.TypeQL;
```

We are now ready to construct TypeQL queries, using the methods available on the `TypeQL` class.

## Examples

Using the Java query builder library is quite simple as it produces a TypeQL string.

See the examples below.

### Example 1: A get query

<!-- test-ignore -->
```java
TypeQLMatch.Filtered getQuery = TypeQL.match(
        var("u").isa("user").has("full-name", "Kevin Morrison"),
        var("p").rel("u").rel("pa").isa("permission"),
        var("o").isa("object").has("path", var("fp")),
        var("pa").rel("o").rel("va").isa("access")
).get("fp");
```

As the result of the above example we should get a TypeQL query in a `getQuery` variable that can be used for a 
match query like in the following line.

<!-- test-ignore -->
```java
readTransaction.query().match(getQuery)
```

The result should be the same as if we set `getQuery` variable as a TypeQL string.

<!-- test-ignore -->
```java
String getQuery = "match $u isa user, has full-name 'Kevin Morrison'; $p($u, $pa) isa permission; " +
                  "$o isa object, has path $fp; $pa($o, $va) isa access; get $fp;";
```

### Example 2: A get query with additional parameters

The following example showcases the usage of sorting, offsetting and limiting a get query.

<!-- test-ignore -->
```java
TypeQLMatch.Limited getQuery = TypeQL.match(
        var("u").isa("user").has("full-name", "Kevin Morrison"),
        var("p").rel("u").rel("pa").isa("permission"),
        var("o").isa("object").has("path", var("fp")),
        var("pa").rel("o").rel("va").isa("access"),
        var("va").isa("action").has("name", "view_file")
).get("fp").sort("fp").offset(0).limit(5);
```

### Example 3: An insert query

The following example showcases the usage of insert query.

<!-- test-ignore -->
```java
insertQuery = TypeQL.match(
        var("f").isa("file").has("path", filepath),
        var("vav").isa("action").has("name", "view_file")
                )
        .insert(var("pa").rel("vav").rel("f").isa("access"));
```
