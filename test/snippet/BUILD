#####################
# Java Snippet Test #
#####################

java_test(
    name = "snippet-java",
    test_class = "generated.TestSnippetJava",
    srcs = [":generate-test-snippet-java"],
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
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
        "//test/grakn-test-server/conf:cassandra-embedded.yaml",
        "//test/grakn-test-server/conf:grakn.properties"
    ]
)

genrule(
    name = "generate-test-snippet-java",
    srcs = [
        "generate-test-snippet-java.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location generate-test-snippet-java.py) $@ $(locations //:content)",
    outs = ["generated/TestSnippetJava.java"]
)

######################
# Graql Snippet Test #
######################

java_test(
    name = "snippet-graql",
    test_class = "generated.TestSnippetGraql",
    srcs = [":generate-test-snippet-graql"],
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
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
        "//test/grakn-test-server/conf:cassandra-embedded.yaml",
        "//test/grakn-test-server/conf:grakn.properties"
    ]
)

genrule(
    name = "generate-test-snippet-graql",
    srcs = [
        "generate-test-snippet-graql.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location generate-test-snippet-graql.py) $@ $(locations //:content)",
    outs = ["generated/TestSnippetGraql.java"]
)