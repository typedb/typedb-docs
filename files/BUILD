exports_files([
    "negation/schema.tql"
])

filegroup(
    name = "social-network-kg",
    srcs = ["social-network/schema.tql"],
    visibility = ["//visibility:public"]
)

filegroup(
    name = "phone-calls-kg",
    srcs = ["phone-calls/schema.tql"] + glob(["phone-calls/data/*.csv"] + glob(["phone-calls/data/*.json"]) + glob(["phone-calls/data/*.xml"])),
    visibility = ["//visibility:public"]
)

#filegroup(
#    name = "iam-kg",
#    srcs = ["iam/iam-schema.tql"] + ["iam/iam-schema.tql"],
#    visibility = ["//visibility:public"]
#)
