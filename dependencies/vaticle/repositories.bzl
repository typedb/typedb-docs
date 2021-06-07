#
# Copyright (C) 2021 Grakn Labs
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

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

def vaticle_dependencies():
    git_repository(
        name = "vaticle_dependencies",
        remote = "https://github.com/vaticle/dependencies",
        commit = "515d6adf719cc7e78f9d313e6c97bce9f918b60b", # sync-marker: do not remove this comment, this is used for sync-dependencies by @vaticle_dependencies
    )

def vaticle_typedb_client_java():
    git_repository(
        name = "vaticle_typedb_client_java",
        remote = "https://github.com/vaticle/typedb-client-java",
        tag = "2.1.1" # sync-marker: do not remove this comment, this is used for sync-dependencies by @vaticle_typedb_client_java
    )

def vaticle_typedb_client_python():
    git_repository(
        name = "vaticle_typedb_client_python",
        remote = "https://github.com/vaticle/typedb-client-python",
        tag = "2.1.1" # sync-marker: do not remove this comment, this is used for sync-dependencies by @vaticle_typedb_client_python
    )

