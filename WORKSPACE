workspace( name = "docs" )

###############################################################
#                    common bazel imports                     #
###############################################################
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_jar")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

###############################################################
#                      Load Build Tools                       #
###############################################################
# Load additional build tools, such bazel-deps and unused-deps
load("//dependencies/tools:dependencies.bzl", "tools_dependencies")
tools_dependencies()

load("//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

###############################################################
#             grakn core + transitive dependencies            #
###############################################################
git_repository(
    name = "graknlabs_grakn_core",
    remote = "https://github.com/graknlabs/grakn",
    commit = '3c416379e6fd8f57fc2cfc7e337551f9c6d3edf1' # grabl-marker: do not remove this comment, this is used for dependency-update by @graknlabs_grakn_core
)

load("@graknlabs_grakn_core//dependencies/compilers:dependencies.bzl", "grpc_dependencies")
grpc_dependencies()

load("@com_github_grpc_grpc//bazel:grpc_deps.bzl", com_github_grpc_grpc_bazel_grpc_deps = "grpc_deps")
com_github_grpc_grpc_bazel_grpc_deps()

load("@stackb_rules_proto//python:deps.bzl", "python_grpc_compile")
python_grpc_compile()

# ----- @graknlabs_grakn_core deps -----
git_repository(
 name="com_github_google_bazel_common",
 remote="https://github.com/graknlabs/bazel-common",
 commit="550f0490798a4e4b6c5ff8cac3b6f5c2a5e81e21",
)

load("@com_github_google_bazel_common//:workspace_defs.bzl", "google_common_workspace_rules")
google_common_workspace_rules()


load("@graknlabs_grakn_core//dependencies/maven:dependencies.bzl", maven_dependencies_for_build = "maven_dependencies")
maven_dependencies_for_build()

load("@stackb_rules_proto//java:deps.bzl", "java_grpc_compile")
java_grpc_compile()

load("@graknlabs_grakn_core//dependencies/docker:dependencies.bzl", "docker_dependencies")
docker_dependencies()

###############################################################
#               graql + transitive dependencies               #
###############################################################
git_repository(
    name = "graknlabs_graql",
    remote = "https://github.com/graknlabs/graql",
    commit = '2dbf9b5f57119038bed604293135ae11263bde68' # grabl-marker: do not remove this comment, this is used for dependency-update by @graknlabs_graql
)

load("@graknlabs_graql//dependencies/maven:dependencies.bzl", "maven_dependencies")
maven_dependencies()

# Load ANTLR dependencies for Bazel
load("@graknlabs_graql//dependencies/compilers:dependencies.bzl", "antlr_dependencies")
antlr_dependencies()

# Load ANTLR dependencies for ANTLR programs
load("@rules_antlr//antlr:deps.bzl", "antlr_dependencies")
antlr_dependencies()

###############################################################
#           client java + transitive dependencies             #
###############################################################
git_repository(
    name = "graknlabs_client_java",
    remote = "https://github.com/graknlabs/client-java",
    commit = 'e2d3cba2216c5aadf58184c9abeb16dd3718c677' # grabl-marker: do not remove this comment, this is used for dependency-update by @graknlabs_client_java
)

######################################################
#      client python + transitive dependencies       #
######################################################
git_repository(
    name = "graknlabs_client_python",
    remote = "https://github.com/graknlabs/client-python",
    commit = 'bf27d7b0872ffadba15bd72db1716080875e7dd2' # grabl-marker: do not remove this comment, this is used for dependency-update by @graknlabs_client_python
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

# ----- transitive python dependencies -----
# TODO: client python's pip_import should be called pypi_dependencies_grakn_client
pip_import(
    name = "pypi_dependencies",
    requirements = "@graknlabs_client_python//:requirements.txt",
)

load("@pypi_dependencies//:requirements.bzl", grakn_client_pip_install = "pip_install")
grakn_client_pip_install()

# ----- local python dependencies -----
pip_import(
    name = "local_pypi_dependencies",
    requirements = "//test/standalone/python:requirements.txt",
)

load("@local_pypi_dependencies//:requirements.bzl", "pip_install")
pip_install()

# ----- grakn bazel distribution dependencies -----
git_repository(
    name="graknlabs_bazel_distribution",
    remote="https://github.com/graknlabs/bazel-distribution",
    commit="ca5c3e1284bdfbfd8c34a7fe2299254d902bdba0"
)

pip_import(
    name = "pypi_deployment_dependencies",
    requirements = "@graknlabs_bazel_distribution//pip:requirements.txt",
)

load("@pypi_deployment_dependencies//:requirements.bzl", "pip_install")
pip_install()

######################################################
#                nodejs dependencies                 #
######################################################

git_repository(
    name = "build_bazel_rules_nodejs",
    remote = "https://github.com/graknlabs/rules_nodejs.git",
    commit = "3d14bf46e177862fc14ea8de8ad5116924c5064e",
)

load("@build_bazel_rules_nodejs//:defs.bzl", "node_repositories", "npm_install")
load("@build_bazel_rules_nodejs//:package.bzl", "rules_nodejs_dependencies")
node_repositories()
rules_nodejs_dependencies()

npm_install(
    name = "nodejs_dependencies",
    package_json = "//test/standalone/nodejs:package.json",
    data = [
      "@build_bazel_rules_nodejs//internal/babel_library:package.json",
      "@build_bazel_rules_nodejs//internal/babel_library:babel.js",
      "@build_bazel_rules_nodejs//internal/babel_library:yarn.lock"
    ]
)