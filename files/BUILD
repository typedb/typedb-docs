filegroup(
    name = "social-network-kg",
    srcs = ["social-network/schema.gql"],
    visibility = ["//visibility:public"]
)

filegroup(
    name = "phone-calls-kg",
    srcs = ["phone-calls/schema.gql"] + glob(["phone-calls/data/*.csv"] + glob(["phone-calls/data/*.json"]) + glob(["phone-calls/data/*.xml"])),
    visibility = ["//visibility:public"]
)