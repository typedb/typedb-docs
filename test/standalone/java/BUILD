################################
# phone_calls Standalones Test #
################################

java_test(
    name = "standalone-java-phone-calls",
    test_class = "generated.TestStandalonePhoneCalls",
    srcs = [
        ":move-test-standalone-java-phone-calls",
        ":generate-standalones-java-phone-calls"
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
        "//test/grakn-test-server/conf:cassandra-embedded.yaml",
        "//test/grakn-test-server/conf:grakn.properties",
        "//files:phone-calls-kg"
    ]
)

genrule(
    name = "generate-standalones-java-phone-calls",
    srcs = [
        "generate_standalone_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## examples/migration-java
        "generated/PhoneCallsCSVMigration.java",
        "generated/PhoneCallsJSONMigration.java",
        "generated/PhoneCallsXMLMigration.java",
        ## examples/queries
        "generated/PhoneCallsFirstQuery.java",
        "generated/PhoneCallsSecondQuery.java",
        "generated/PhoneCallsThirdQuery.java",
        "generated/PhoneCallsForthQuery.java",
        "generated/PhoneCallsFifthQuery.java",
    ]
)

genrule(
    name = "move-test-standalone-java-phone-calls",
    srcs = ["PhoneCalls.java"],
    cmd = "cp $(location PhoneCalls.java) $(location generated/TestStandalonePhoneCalls.java)",
    outs = ["generated/TestStandalonePhoneCalls.java"]
)

###################################
# social_network Standalones Test #
###################################

java_test(
    name = "standalone-java-social-network",
    test_class = "generated.TestStandaloneSocialNetwork",
    srcs = [
        ":move-test-standalone-java-social-network",
        ":generate-standalones-java-social-network"
    ],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
        "@graknlabs_grakn_core//concept:concept",
        "@graknlabs_grakn_core//server:server",
        "@graknlabs_grakn_core//test-integration/rule:grakn-test-server"
    ],
    classpath_resources = [
        "@graknlabs_grakn_core//test-integration/resources:logback-test",
    ],
    data = [
        "//test/grakn-test-server/conf:cassandra-embedded.yaml",
        "//test/grakn-test-server/conf:grakn.properties",
        "//files:social-network-kg"
    ]
)

genrule(
    name = "generate-standalones-java-social-network",
    srcs = [
        "generate_standalone_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        # general/quickstart
        "generated/SocialNetworkQuickstartQuery.java",
        # client-api/java
        "generated/GraknQuickstartA.java",
        "generated/GraknQuickstartB.java",
        "generated/GraknQuickstartC.java"
    ]
)

genrule(
    name = "move-test-standalone-java-social-network",
    srcs = ["SocialNetwork.java"],
    cmd = "cp $(location SocialNetwork.java) $(location generated/TestStandaloneSocialNetwork.java)",
    outs = ["generated/TestStandaloneSocialNetwork.java"]
)