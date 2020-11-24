This project contains a minimal working example of a grpc hello world project using bazel.

Use this command to run the server

`bazel run :product_service_server
`

Use this command to run the client

`bazel run :product_service_client
`

Use this command to clean the project

`bazel clean --expunge  `