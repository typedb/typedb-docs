load("@graknlabs_common//test/server:rules.bzl", "grakn_test")

#########################
# Graql Java Query Test #
#########################

grakn_test(
    name = "graql-java",
    test_class = "grakn.doc.test.query.GraqlJavaTest",
    srcs = [":graql-java-tests"],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
    ],
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
    ],
    grakn_artifact = "@graknlabs_grakn_core_artifact//file",
)

genrule(
    name = "graql-java-tests",
    srcs = [
        "graql-java-tests.py",
        "GraqlJavaTest.java.template",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location graql-java-tests.py) $(location GraqlJavaTest.java.template) $@ $(locations //:content)",
    outs = ["GraqlJavaTest.java"]
)

#########################
# Graql Lang Query Test #
#########################

grakn_test(
    name = "graql-lang",
    test_class = "grakn.doc.test.query.GraqlLangTest",
    srcs = [":graql-lang-tests"],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
    ],
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
    ],
    grakn_artifact = "@graknlabs_grakn_core_artifact//file",
)

genrule(
    name = "graql-lang-tests",
    srcs = [
        "graql-lang-tests.py",
        "GraqlLangTest.java.template",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location graql-lang-tests.py) $(location GraqlLangTest.java.template) $@ $(locations //:content) ",
    outs = ["GraqlLangTest.java"]
)
