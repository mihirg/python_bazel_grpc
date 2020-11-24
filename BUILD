package(default_visibility = ["//visibility:public"])

load("@rules_proto_grpc//python:defs.bzl", "python_grpc_compile")
load("@rules_proto_grpc//python:defs.bzl", "python_grpclib_library")
load("@rules_proto_grpc//python:defs.bzl", "python_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

# Defines a logical collection of proto files. This is supposed to be reusable.
proto_library(
    name = "product_service_proto",
    srcs = ["product_service.proto"],
)

# Uses the proto collection to generate stub code
python_grpclib_library(
    name = "product_service_grpc_lib",
    deps = [":product_service_proto"],
)

# Product Service Server
py_binary(
    name = "product_service_server",
    srcs = ["product_service_server.py"],
    deps = [":product_service_grpc_lib"]
)

# Product Serivice Client
py_binary(
    name = "product_service_client",
    srcs = ["product_service_client.py"],
    deps = [":product_service_grpc_lib"]
)


