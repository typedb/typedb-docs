#
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#

load("@graknlabs_common//test/server:rules.bzl", "grakn_java_test", "native_grakn_artifact")


native_grakn_artifact(
    name = "native-grakn-artifact",
    mac_artifact = "@graknlabs_grakn_core_artifact_mac//file",
    linux_artifact = "@graknlabs_grakn_core_artifact_linux//file",
    windows_artifact = "@graknlabs_grakn_core_artifact_windows//file",
    visibility = ["//test:__subpackages__"],
)

#########################
# Graql Java Query Test #
#########################
grakn_java_test(
    name = "graql-java",
    test_class = "grakn.doc.test.query.GraqlJavaTest",
    srcs = [":graql-java-tests"],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
    ],
    native_grakn_artifact = ":native-grakn-artifact",
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
    ]
)


genrule(
    name = "graql-java-tests",
    srcs = [
        "graql-java-tests.py",
        "templates/GraqlJavaTest.java",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location graql-java-tests.py) $(location templates/GraqlJavaTest.java) $@ $(locations //:content)",
    outs = ["GraqlJavaTest.java"]
)

#########################
# Graql Lang Query Test #
#########################
grakn_java_test(
    name = "graql-lang",
    test_class = "grakn.doc.test.query.GraqlLangTest",
    srcs = [":graql-lang-tests"],
    deps = [
        "@graknlabs_client_java//:client-java",
        "@graknlabs_graql//java:graql",
    ],
    native_grakn_artifact = ":native-grakn-artifact",
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
    ]
)


genrule(
    name = "graql-lang-tests",
    srcs = [
        "graql-lang-tests.py",
        "templates/GraqlLangTest.java",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location graql-lang-tests.py) $(location templates/GraqlLangTest.java) $@ $(locations //:content) ",
    outs = ["GraqlLangTest.java"]
)
