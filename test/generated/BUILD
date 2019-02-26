########
# Test #
########

java_test(
    name = "snippet-java",
    test_class = "generated.TestSnippetJava",
    srcs = ["TestSnippetJava.java"],
    deps = [
        "@graknlabs_grakn_core//client-java:client-java",
        "@graknlabs_graql//java:graql",
        "@graknlabs_grakn_core//concept:concept",
        "@graknlabs_grakn_core//server:server",
        "@graknlabs_grakn_core//test-integration/rule:grakn-test-server"
    ],
    classpath_resources = [
        "@graknlabs_grakn_core//test-integration/resources:logback-test",
    ],
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//test/grakn-test-server/conf:cassandra-embedded.yaml",
        "//test/grakn-test-server/conf:grakn.properties"
    ]
)