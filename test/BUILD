#######################################################
## generating and running the java snippet test class #
#######################################################

#java_test(
#    name = "java-snippet-test",
#    test_class = "generated.JavaSnippetTest",
#    srcs = [":java-snippet-test-generator"],
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
#    name = "java-snippet-test-generator",
#    srcs = [
#        "generate_java_snippet_tests.py",
#        "//:content" # filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate_java_snippet_tests.py) $@ $(locations //:content)",
#    outs = ["generated/JavaSnippetTest.java"]
#)


########################################################
## generating and running the graql snippet test class #
########################################################
#
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
#        "//files:social-network-kg", # filegroup defined in files/BUILD
#        "grakn-test-server/conf/cassandra-embedded.yaml",
#        "grakn-test-server/conf/grakn.properties"
#    ]
#)
#
#genrule(
#    name = "graql-snippet-test-generator",
#    srcs = [
#        "generate_graql_snippet_tests.py",
#        "//:content" # filegroup defined in root/BUILD
#    ],
#    cmd = "python $(location generate_graql_snippet_tests.py) $@ $(locations //:content)",
#    outs = ["generated/GraqlSnippetTest.java"]
#)

############################################
## generating and running java standalones #
############################################

################
## phone_calls #
################

#java_test(
#    name = "test-standalone-phone-calls-first-query",
#    test_class = "generated.PhoneCallsFirstQuery",
#    srcs = [":test-standalone-generator"],
#    deps = [
#        "@graknlabs_grakn//client-java:client-java",
#        "@graknlabs_grakn//server:server",
#        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
#    ]
#)

#java_test(
#    name = "test-standalone-phone-calls",
#    test_class = "generated.TestStandalonePhoneCalls",
#    srcs = [":move-standalone-phone-calls", ":generate-standalones-phone-calls"],
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
#    name = "generate-standalones-phone-calls",
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
#        ## general/quickstart
##        "generated/SocialNetworkQuery.java"
#    ]
#)
#
#genrule(
#    name = "move-standalone-phone-calls",
#    srcs = ["TestStandalonePhoneCalls.java"],
#    cmd = "cp $(location TestStandalonePhoneCalls.java) $(location generated/TestStandalonePhoneCalls.java)",
#    outs = ["generated/TestStandalonePhoneCalls.java"]
#)

###################
## social_network #
###################

java_test(
    name = "test-standalone-social-network",
    test_class = "generated.TestStandaloneSocialNetwork",
    srcs = [":move-standalone-social-network", ":generate-standalones-social-network"],
    deps = [
        "@graknlabs_grakn//client-java:client-java",
        "@graknlabs_grakn//server:server",
        "@graknlabs_grakn//test-integration/rule:grakn-test-server"
    ],
    classpath_resources = [
        "@graknlabs_grakn//test-integration/resources:logback-test",
    ],
    data = [
        "grakn-test-server/conf/cassandra-embedded.yaml",
        "grakn-test-server/conf/grakn.properties",
        "//files:social-network-kg"
    ]
)

genrule(
    name = "generate-standalones-social-network",
    srcs = [
        "generate_standalone_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python $(location generate_standalone_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        ## general/quickstart
        "generated/SocialNetworkQuery.java"
    ]
)

genrule(
    name = "move-standalone-social-network",
    srcs = ["TestStandaloneSocialNetwork.java"],
    cmd = "cp $(location TestStandaloneSocialNetwork.java) $(location generated/TestStandaloneSocialNetwork.java)",
    outs = ["generated/TestStandaloneSocialNetwork.java"]
)


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