############################
# Phone Calls Example Test #
############################

java_test(
    name = "phone-calls",
    test_class = "grakn.doc.test.example.PhoneCallsTest",
    srcs = [
        "PhoneCallsTest.java",
        ":phone-calls-tests",
    ],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
        "@graknlabs_grakn_core//concept:concept",
        "@graknlabs_grakn_core//server:server",
        "@graknlabs_grakn_core//test-integration/rule:grakn-test-server",
        "//dependencies/maven/artifacts/org/sharegov:mjson",
        "//dependencies/maven/artifacts/com/google/code/gson:gson",
        "//dependencies/maven/artifacts/com/univocity:univocity-parsers",
        "//dependencies/maven/artifacts/javax/xml/stream:stax-api"
    ],
    classpath_resources = [
        "@graknlabs_grakn_core//test-integration/resources:logback-test",
    ],
    data = [
        "//files:phone-calls-kg",
        "//test/conf:cassandra-embedded.yaml",
        "@graknlabs_grakn_core//server:conf/grakn.properties",
    ]
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "java_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location java_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## examples/migration-java
        "PhoneCallsCSVMigration.java",
        "PhoneCallsJSONMigration.java",
        "PhoneCallsXMLMigration.java",
        ## examples/queries
        "PhoneCallsFirstQuery.java",
        "PhoneCallsSecondQuery.java",
        "PhoneCallsThirdQuery.java",
        "PhoneCallsForthQuery.java",
        "PhoneCallsFifthQuery.java",
    ]
)

###################################
# social_network Standalones Test #
###################################

java_test(
    name = "social-network",
    test_class = "grakn.doc.test.example.SocialNetworkTest",
    srcs = [
        "SocialNetworkTest.java",
        ":social-network-tests",
    ],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
        "@graknlabs_grakn_core//concept:concept",
        "@graknlabs_grakn_core//server:server",
        "@graknlabs_grakn_core//test-integration/rule:grakn-test-server",
    ],
    classpath_resources = [
        "@graknlabs_grakn_core//test-integration/resources:logback-test",
    ],
    data = [
        "//test/conf:cassandra-embedded.yaml",
        "@graknlabs_grakn_core//server:conf/grakn.properties",
        "//files:social-network-kg",
    ]
)

genrule(
    name = "social-network-tests",
    srcs = [
        "java_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location java_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        # general/quickstart
        "SocialNetworkQuickstartQuery.java",
        # client-api/java
        "GraknQuickstartA.java",
        "GraknQuickstartB.java",
        "GraknQuickstartC.java",
    ]
)