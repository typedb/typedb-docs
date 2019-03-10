# What is a Standalone?

The term _standalone_ refers to the content of code blocks in the Grakn documentation that is self-contained. In other words, given the most minimal set of prerequisites, standalones should compile and run with no external dependencies.
The common prerequisite among all standalones are:
- a running Grakn Server.
- a keyspace into which the relevant schema has been loaded.

At the moment, the keyspaces that standalones run on are `social_network` and `phone_calls`. For this reason, there are two templates for testing standalones. Each of these templates, regardless of their language:
- once before testing their standalone, load the corresponding schema into a keyspace with the same name as the one used in the standalones
- once after having tested all their standalone, delete the previously created keyspace

## Add a Java Standalone Test
The steps to configure a Java standalone for testing are as follows:

### 1. Add the Flag

Add the `<!-- test-example <FileName.java> -->` immediately before the intended code block. `FileName` must be unique among all Java standalones.

#### Example:

    ```
    <!-- test-example FileName.java -->
    ```java
    ...
    ```

### 2. Add the Test Method Placeholder

Add a JUnit test method in the corresponding test class (ie. [`test/example/java/PhoneCalls.java`](java/PhoneCallsTest.java) or [`test/example/java/SocialNetwork.java`](java/SocialNetworkTest.java))

#### Format:

```java
@Test
public void test<alphabet>FileName() {
    ClassName.main(new String[]{});
}
```
`ClassName` should be identical to the `FileName`.

Java tests run based on their alphabetic order. This is to speed up the tests, by running standalones that contain heavy `read` operations first, before those that insert many instances of data. The `<alphabet>` in the format above is for this purpose.

### 3. Add the Bazel Data Item

Add `generated/FileName.java` to the list of the `data` property of the corresponding `java_test` rule (ie. `standalone-java-social-network` or `standalone-java-phone-calls`) contained within [`test/example/java/BUILD`](java/BUILD).


## Add a Javascript Standalone Test

The steps to configure a Javascript standalone for testing are as follows:

### 1. Add the Flag

Add the `<!-- test-example <fileName.js> -->` immediately before the intended code block. `fileName` must be unique among all Java standalones.

#### Example:

    <!-- test-example <fileName.js> -->
    ```javascript
    ...
    ```

### 2. Add the Test Method Placeholder

Add a Jasmine `spect` in the relevant `describe` of corresponding test file (ie. [`test/example/nodejs/phoneCallsTemplate.js`](nodejs/phoneCallsTemplate.js) or [`test/example/nodejs/socialNetworkTemplate.js`](nodejs/socialNetworkTemplate.js))

#### Format:

```javascript
it("tests fileName.js", async function() {
    // fileName.js
});
```

By doing this, `test/example/nodejs/generate_standalone_tests.py`:
1. identifies the `fileName.js` standalone in the `.md` files
2. post-processes it to ensure the main function call is prefixed with `await`
3. places the processed standalone content in place of the `// fileName.js`

Javascript specs run based on the order they've been written in. To speed up the tests, ensue to include standalones that contain heavy `read` operations first, before those that insert many instances of data.

## Add a Python Standalone Test

The steps to configure a Python standalone for testing are as follows:

### 1. Add the Flag

Add the `<!-- test-example <file_name.py> -->` immediately before the intended code block. `file_name` must be unique among all Java standalones.

#### Example:

    <!-- test-example <file_name.py> -->
    ```python
    ...
    ```

### 2. Add the Test Method Placeholder

Add a `unittest` method in the corresponding test file (ie. [`test/example/python/phone_calls.py`](python/phone_calls.py) or [`test/example/python/social_network.py`](python/social_network.py))

#### Format:

```python
def test_<alphabete>_file_name(self):
    import file_name
```

Python tests run based on their alphabetic order. This is to speed up the tests, by running standalones that contain heavy `read` operations first, before those that insert many instances of data. The `<alphabete>` in the format above is for this purpose.

### 3. Add the Bazel Data Item

Add `generated/file_name.py` to the list of the `data` property of the corresponding `py_test` rule (ie. `standalone-python-social-network` or `standalone-python-phone-calls`) contained within [`test/example/python/BUILD`](python/BUILD).
