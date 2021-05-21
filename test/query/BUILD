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

load("@vaticle_typedb_common//test:rules.bzl", "typedb_java_test", "native_typedb_artifact")


native_typedb_artifact(
    name = "native-typedb-artifact",
    mac_artifact = "@vaticle_typedb_artifact_mac//file",
    linux_artifact = "@vaticle_typedb_artifact_linux//file",
    windows_artifact = "@vaticle_typedb_artifact_windows//file",
    output = "typedb-server-native.tar.gz",
    visibility = ["//test:__subpackages__"],
)

##########################
# TypeQL Java Query Test #
##########################
typedb_java_test(
    name = "typeql-java",
    test_class = "com.vaticle.doc.test.query.TypeQLJavaTest",
    srcs = [":typeql-java-tests"],
    deps = [
        "@vaticle_typedb_client_java//:client-java",
        "@vaticle_typedb_client_java//api",
        "@vaticle_typeql_lang_java//:typeql-lang",
        "@vaticle_typeql_lang_java//query",
        "@vaticle_typeql_lang_java//pattern",
        "@vaticle_typeql_lang_java//common",
    ],
    server_mac_artifact = "@vaticle_typedb_artifact_mac//file",
    server_linux_artifact = "@vaticle_typedb_artifact_linux//file",
    server_windows_artifact = "@vaticle_typedb_artifact_windows//file",
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
        "//files:negation/schema.tql",
    ]
)


genrule(
    name = "typeql-java-tests",
    srcs = [
        "typeql-java-tests.py",
        "templates/TypeQLJavaTest.java",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location typeql-java-tests.py) $(location templates/TypeQLJavaTest.java) $@ $(locations //:content)",
    outs = ["TypeQLJavaTest.java"]
)

##########################
# TypeQL Lang Query Test #
##########################
typedb_java_test(
    name = "typeql-lang",
    test_class = "com.vaticle.doc.test.query.TypeQLLangTest",
    srcs = [":typeql-lang-tests"],
    deps = [
        "@vaticle_typedb_client_java//:client-java",
        "@vaticle_typedb_client_java//api",
        "@vaticle_typeql_lang_java//:typeql-lang",
        "@vaticle_typeql_lang_java//query",
        "@vaticle_typeql_lang_java//pattern"
    ],
    server_mac_artifact = "@vaticle_typedb_artifact_mac//file",
    server_linux_artifact = "@vaticle_typedb_artifact_linux//file",
    server_windows_artifact = "@vaticle_typedb_artifact_windows//file",
    data = [
        "//files:social-network-kg", # filegroup defined in files/BUILD
        "//files:phone-calls-kg", # filegroup defined in files/BUILD
        "//files:negation/schema.tql",
    ],
    size = "large",
)


genrule(
    name = "typeql-lang-tests",
    srcs = [
        "typeql-lang-tests.py",
        "templates/TypeQLLangTest.java",
        "//:content" # filegroup defined in root/BUILD
    ],
    cmd = "python3 $(location typeql-lang-tests.py) $(location templates/TypeQLLangTest.java) $@ $(locations //:content) ",
    outs = ["TypeQLLangTest.java"]
)
