---
pageTitle: Java query builder
keywords: typedb, client, java, install, repository
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: Tutorial for TypeDB Client Java.
---

## Java query builder

The Java builder library can be used to programmatically construct TypeQL queries with native Java code.

To use TypeQL, we first add it as a dependency to our `pom.xml`. Don't forget to replace the `{version}` placeholder 
with exact version of the library.

The latest version of `typeql-lang` can be found in the 
[public Maven repository](https://repo.vaticle.com/#browse/browse:maven:com%2Fvaticle%2Ftypeql%2Ftypeql-lang).

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

```java
import com.vaticle.typeql.lang.TypeQL;
```

We are now ready to construct TypeQL queries, using the methods available on the `TypeQL` class.

<!-- #todo Add query examples here

[//]: # (Check out the following pages to learn, by example, how the TypeQL API allows construction of various TypeQL queries:)

[//]: # (- [Expressive patterns]&#40;../query/match-clause&#41;)

[//]: # (- [Retrieval queries]&#40;../query/get-query&#41;)

[//]: # (- [Insertion queries]&#40;../query/insert-query&#41;)

[//]: # (- [Deletion queries]&#40;../query/delete-query&#41;)

[//]: # (- [Aggregation queries]&#40;../query/aggregate-query&#41;)

--->
