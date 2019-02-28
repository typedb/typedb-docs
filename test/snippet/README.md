# What is a Snippet?

The term _snippet_ refers to the content of code bocks that are incomplete to run on their own. In other words, to compile and run, they require more code than what they contain.
At the moment, snippets are written either in Java or Graql, and run on one single keyspace that contains the schema definitions of both the `social_network` and the `phone_calls` knowledge graphs.

Snippets are generally code blocks that contains one ore more:
- Graql queries, or
- Instantiation of Java `GraqlQuery` objects.

## Add a Snippet Test

Any code block with its language specified as `java` or `graql` is tested as a snippet.

Examples:

    ```java
    <Java code>
    ```

    ```graql
    <Graql query>
    ```

## Avoid Tests on Snippets

To exclude a snippet from being tested, immediately before the code block, add:
- the `<!-- test-ignore -->` flag for code that not testable.
- the `<!-- test-delay -->` flag for code that is, in fact, testable, but would fail until a back-end implementation/fix.