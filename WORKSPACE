#
# GRAKN.AI - THE KNOWLEDGE GRAPH
# Copyright (C) 2018 Grakn Labs Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

workspace(name = "graknlabs_docs")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_jar")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")


################################
# Load Grakn Labs Dependencies #
################################

git_repository(
    name = "graknlabs_graql",
    remote = "https://github.com/graknlabs/graql",
    commit = '33b53ca88871a4efdd3d4e17e7e40e2317c3778b' # sync-marker: do not remove this comment, this is used for sync-dependencies by @graknlabs_graql
)

git_repository(
    name = "graknlabs_grakn_core",
    remote = "https://github.com/graknlabs/grakn",
    commit = '6baaffb22bafb9f202ac4f3084291edf6d317250' # sync-marker: do not remove this comment, this is used for sync-dependencies by @graknlabs_grakn_core
)

git_repository(
    name = "graknlabs_client_java",
    remote = "https://github.com/graknlabs/client-java",
    commit = 'e2d3cba2216c5aadf58184c9abeb16dd3718c677' # sync-marker: do not remove this comment, this is used for sync-dependencies by @graknlabs_client_java
)

git_repository(
    name = "graknlabs_client_python",
    remote = "https://github.com/graknlabs/client-python",
    commit = 'bf27d7b0872ffadba15bd72db1716080875e7dd2' # sync-marker: do not remove this comment, this is used for sync-dependencies by @graknlabs_client_python
)

git_repository(
    name = "graknlabs_build_tools",
    remote = "https://github.com/graknlabs/build-tools",
    commit = "4815b8583ca98ad59058d1a808b87e6b2f47dbf7", # sync-marker: do not remove this comment, this is used for sync-dependencies by @graknlabs_build_tools
)

load("@graknlabs_build_tools//distribution:dependencies.bzl", "graknlabs_bazel_distribution")
graknlabs_bazel_distribution()


####################
# Load Build Tools #
####################

# Load additional build tools, such bazel-deps and unused-deps
load("@graknlabs_build_tools//bazel:dependencies.bzl", "bazel_common", "bazel_deps",
     "bazel_toolchain", "bazel_rules_docker", "bazel_rules_nodejs", "bazel_rules_python")
bazel_common()
bazel_deps()
bazel_toolchain()
bazel_rules_docker()
bazel_rules_nodejs()
bazel_rules_python()


###########################
# Load Local dependencies #
###########################

# for Java

load("//dependencies/maven:dependencies.bzl", "maven_dependencies")
maven_dependencies()

# for Node.js

load("@build_bazel_rules_nodejs//:package.bzl", "rules_nodejs_dependencies")
rules_nodejs_dependencies()

load("@build_bazel_rules_nodejs//:defs.bzl", "node_repositories", "npm_install")
node_repositories()

npm_install(
    name = "nodejs_dependencies",
    package_json = "//test/standalone/nodejs:package.json",
    data = [
      "@build_bazel_rules_nodejs//internal/babel_library:package.json",
      "@build_bazel_rules_nodejs//internal/babel_library:babel.js",
      "@build_bazel_rules_nodejs//internal/babel_library:yarn.lock"
    ]
)

# for Python

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

pip_import(
    name = "local_pypi_dependencies",
    requirements = "//test/standalone/python:requirements.txt",
)

load("@local_pypi_dependencies//:requirements.bzl", "pip_install")
pip_install()


################################
# Load Grakn Core dependencies #
################################

load("@graknlabs_grakn_core//dependencies/maven:dependencies.bzl", grakn_core_dependencies = "maven_dependencies")
grakn_core_dependencies()

load("@graknlabs_grakn_core//dependencies/compilers:dependencies.bzl", "grpc_dependencies")
grpc_dependencies()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", "grpc_deps")
grpc_deps()

load("@stackb_rules_proto//java:deps.bzl", "java_grpc_compile")
java_grpc_compile()

load("@com_github_google_bazel_common//:workspace_defs.bzl", "google_common_workspace_rules")
google_common_workspace_rules()


###########################
# Load Graql dependencies #
###########################

# Load ANTLR dependencies for Bazel
load("@graknlabs_graql//dependencies/compilers:dependencies.bzl", "antlr_dependencies")
antlr_dependencies()

# Load ANTLR dependencies for ANTLR programs
load("@rules_antlr//antlr:deps.bzl", "antlr_dependencies")
antlr_dependencies()

load("@graknlabs_graql//dependencies/maven:dependencies.bzl", graql_dependencies = "maven_dependencies")
graql_dependencies()


###################################
# Load Client Python dependencies #
###################################

# TODO: client python's pip_import should be called pypi_dependencies_grakn_client
pip_import(
    name = "pypi_dependencies",
    requirements = "@graknlabs_client_python//:requirements.txt",
)

pip_import(
    name = "pypi_deployment_dependencies",
    requirements = "@graknlabs_bazel_distribution//pip:requirements.txt",
)

load("@pypi_dependencies//:requirements.bzl", client_python_pip_install = "pip_install")
client_python_pip_install()