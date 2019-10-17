#########################
# Graql Java Query Test #
#########################

java_test(
    name = "graql-java",
    test_class = "grakn.doc.test.query.GraqlJavaTest",
    srcs = [":graql-java-tests"],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
        "@graknlabs_grakn_core//server:server",
        "@graknlabs_grakn_core//test-integration/rule:grakn-test-server"
    ],
    classpath_resources = [
        "@graknlabs_grakn_core//test-integration/resources:logback-test",
    ],
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
        "//test/conf:cassandra-embedded.yaml",
        "@graknlabs_grakn_core//server:conf/grakn.properties"
    ]
)

genrule(
    name = "graql-java-tests",
    srcs = [
        "graql-java-tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location graql-java-tests.py) $@ $(locations //:content)",
    outs = ["GraqlJavaTest.java"]
)

#########################
# Graql Lang Query Test #
#########################

java_test(
    name = "graql-lang",
    test_class = "grakn.doc.test.query.GraqlLangTest",
    srcs = [":graql-lang-tests"],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
        "@graknlabs_grakn_core//server:server",
        "@graknlabs_grakn_core//test-integration/rule:grakn-test-server"
    ],
    classpath_resources = [
        "@graknlabs_grakn_core//test-integration/resources:logback-test",
    ],
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
        "//test/conf:cassandra-embedded.yaml",
        "@graknlabs_grakn_core//server:conf/grakn.properties"
    ]
)

genrule(
    name = "graql-lang-tests",
    srcs = [
        "graql-lang-tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location graql-lang-tests.py) $@ $(locations //:content)",
    outs = ["GraqlLangTest.java"]
)
