java_test(
    name = "java-snippet-test",
    test_class = "generated.JavaSnippetTest",
    srcs = [":java-snippet-test-generator"],
    deps = [
        "@graknlabs_grakn//client-java:client-java",
        "@graknlabs_grakn//server:server",
        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
    ],
    classpath_resources = [
        "@graknlabs_grakn//test-integration/resources:logback-test",
    ],
    data = [
        "//test-integration:resources/cassandra-embedded.yaml",
        "//server:conf/grakn.properties"
    ]
)

genrule(
    name = "java-snippet-test-generator",
    srcs = [
        "generate_java_snippet_tests.py",
        "//:content" ## name of the filegroup defined in root/BUILD
    ],
    cmd = "python $(location generate_java_snippet_tests.py) $@ $(locations //:content)",
    outs = ["generated/JavaSnippetTest.java"]
)

#java_test(
#    name = "graql-snippet-test",
#    test_class = "generated.GraqlSnippetTest",
#    srcs = [":graql-snippet-test-generator"],
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
#    ],
#    classpath_resources = [
#        "@graknlabs_grakn//test-integration/resources:logback-test",
#    ],
#    data = [
#        "//test-integration:resources/cassandra-embedded.yaml",
#        "//server:conf/grakn.properties"
#    ]
#)
#
#
#genrule(
#    name = "graql-snippet-test-generator",
#    srcs = [
#        "generate_snippet_tests.py",
#        "templates/graql/class.txt",
#        "templates/graql/method.txt",
#        "//:content" ## name of the filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate_snippet_tests.py) graql $(location templates/graql/class.txt) $(location templates/graql/method.txt) $@ $(locations //:content)",
#    outs = ["generated/GraqlSnippetTest.java"]
#)