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
        "@maven//:org_sharegov_mjson",
        "@maven//:com_google_code_gson_gson",
        "@maven//:com_univocity_univocity_parsers",
        "@maven//:javax_xml_stream_stax_api",
    ],
    data = [
        "//files:phone-calls-kg",
    ]
)

genrule(
    name = "phone-calls-tests",
    srcs = [
        "java_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "$(location java_tests.py) $(OUTS) $(locations //:content)",
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
    ],
    data = [
        "//files:social-network-kg",
    ]
)

genrule(
    name = "social-network-tests",
    srcs = [
        "java_tests.py",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "$(location java_tests.py) $(OUTS) $(locations //:content)",
    outs = [
        # general/quickstart
        "SocialNetworkQuickstartQuery.java",
        # client-api/java
        "GraknQuickstartA.java",
        "GraknQuickstartB.java",
        "GraknQuickstartC.java",
    ]
)
