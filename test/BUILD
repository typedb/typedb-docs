#######################################################
## generating and running the java snippet test class #
#######################################################
#
#java_test(
#    name = "snippet-java",
#    test_class = "generated.TestSnippetJava",
#    srcs = [":generate-test-snippet-java"],
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
#    ],
#    classpath_resources = [
#        "@graknlabs_grakn//test-integration/resources:logback-test",
#    ],
#    data = [
#        "//files:social-network-kg", # filegroup defined in files/BUILD
#        "grakn-test-server/conf/cassandra-embedded.yaml",
#        "grakn-test-server/conf/grakn.properties"
#    ]
#)
#
#genrule(
#    name = "generate-test-snippet-java",
#    srcs = [
#        "generate-test-snippet-java.py",
#        "//:content" # filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate-test-snippet-java.py) $@ $(locations //:content)",
#    outs = ["generated/TestSnippetJava.java"]
#)
#
#
########################################################
## generating and running the graql snippet test class #
########################################################
#
#java_test(
#    name = "snippet-graql",
#    test_class = "generated.TestSnippetGraql",
#    srcs = [":generate-test-snippet-graql"],
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
#    ],
#    classpath_resources = [
#        "@graknlabs_grakn//test-integration/resources:logback-test",
#    ],
#    data = [
#        "//files:social-network-kg", # filegroup defined in files/BUILD
#        "grakn-test-server/conf/cassandra-embedded.yaml",
#        "grakn-test-server/conf/grakn.properties"
#    ]
#)
#
#genrule(
#    name = "generate-test-snippet-graql",
#    srcs = [
#        "generate-test-snippet-graql.py",
#        "//:content" # filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate-test-snippet-graql.py) $@ $(locations //:content)",
#    outs = ["generated/TestSnippetGraql.java"]
#)
############################################
## generating and running java standalones #
############################################
#
################
## phone_calls #
################
#
#java_test(
#    name = "standalone-java-phone-calls",
#    test_class = "generated.TestStandalonePhoneCalls",
#    srcs = [
#        ":move-test-standalone-java-phone-calls",
#        ":generate-standalones-java-phone-calls"
#    ],
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server",
#        "//dependencies/maven/artifacts/org/sharegov:mjson",
#        "//dependencies/maven/artifacts/com/google/code/gson:gson",
#        "//dependencies/maven/artifacts/com/univocity:univocity-parsers",
#        "//dependencies/maven/artifacts/javax/xml/stream:stax-api"
#    ],
#    classpath_resources = [
#        "@graknlabs_grakn//test-integration/resources:logback-test",
#    ],
#    data = [
#        "grakn-test-server/conf/cassandra-embedded.yaml",
#        "grakn-test-server/conf/grakn.properties",
#        "//files:phone-calls-kg"
#    ]
#)
#
#genrule(
#    name = "generate-standalones-java-phone-calls",
#    srcs = [
#        "generate_standalone_tests.py",
#        "//:content" # filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
#    outs = [
#        ## examples/migration-java
#        "generated/PhoneCallsCSVMigration.java",
#        "generated/PhoneCallsJSONMigration.java",
#        "generated/PhoneCallsXMLMigration.java",
#        ## examples/queries
#        "generated/PhoneCallsFirstQuery.java",
#        "generated/PhoneCallsSecondQuery.java",
#        "generated/PhoneCallsThirdQuery.java",
#        "generated/PhoneCallsForthQuery.java",
#        "generated/PhoneCallsFifthQuery.java",
#    ]
#)
#
#genrule(
#    name = "move-test-standalone-java-phone-calls",
#    srcs = ["TestStandalonePhoneCalls.java"],
#    cmd = "cp $(location TestStandalonePhoneCalls.java) $(location generated/TestStandalonePhoneCalls.java)",
#    outs = ["generated/TestStandalonePhoneCalls.java"]
#)
#
###################
## social_network #
###################
#
#java_test(
#    name = "standalone-java-social-network",
#    test_class = "generated.TestStandaloneSocialNetwork",
#    srcs = [
#        ":move-test-standalone-java-social-network",
#        ":generate-standalones-java-social-network"
#    ],
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
#    ],
#    classpath_resources = [
#        "@graknlabs_grakn//test-integration/resources:logback-test",
#    ],
#    data = [
#        "grakn-test-server/conf/cassandra-embedded.yaml",
#        "grakn-test-server/conf/grakn.properties",
#        "//files:social-network-kg"
#    ]
#)
#
#genrule(
#    name = "generate-standalones-java-social-network",
#    srcs = [
#        "generate_standalone_tests.py",
#        "//:content" # filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
#    outs = [
#        ## general/quickstart
#        "generated/SocialNetworkQuery.java"
#    ]
#)
#
#genrule(
#    name = "move-test-standalone-java-social-network",
#    srcs = ["TestStandaloneSocialNetwork.java"],
#    cmd = "cp $(location TestStandaloneSocialNetwork.java) $(location generated/TestStandaloneSocialNetwork.java)",
#    outs = ["generated/TestStandaloneSocialNetwork.java"]
#)


load("@io_bazel_rules_python//python:python.bzl", "py_library", "py_test")
load("@pypi_dependencies//:requirements.bzl", "requirement")


py_library(
    name = "standalone-python-phone-calls",
    deps = [
        requirement('grakn'),
        requirement('csv')
  ]
)

py_test(
    name = "standalone-python-phone-calls",
    srcs = [
        "generated/phone_calls_csv_migration.py",
        "generated/test_standalone_phone_calls.py"
    ],
    deps = [
        "standalone-python-phone-calls"
    ]
)

#genrule(
#    name = "generate-standalones-python-phone-calls",
#    srcs = [
#        "generate_standalone_tests.py",
#        "//:content"
#    ],
#    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
#    outs = [
#        ## examples/migration-python
#        "generated/phone_calls_csv_migration.py"
#    ]
#)

#java_test(
#    name = "TestStandalonePhoneCalls",
#    test_class = "test.generated.TestStandalonePhoneCalls",
#    srcs = glob(["generated/*.java"]),
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server",
#        "//dependencies/maven/artifacts/org/sharegov:mjson",
#        "//dependencies/maven/artifacts/com/google/code/gson:gson",
#        "//dependencies/maven/artifacts/com/univocity:univocity-parsers",
#        "//dependencies/maven/artifacts/javax/xml/stream:stax-api"
#    ],
#    classpath_resources = [
#        "@graknlabs_grakn//test-integration/resources:logback-test",
#    ],
#    data = [
#        "grakn-test-server/conf/cassandra-embedded.yaml",
#        "grakn-test-server/conf/grakn.properties",
#        "//files:phone-calls-kg"
#    ]
#)