import logging
import grpc
import product_service_pb2
import product_service_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = product_service_pb2_grpc.ProductServiceStub(channel)
        response = stub.GetProductDetails(product_service_pb2.ProductIdentifier(id=2))
    print(response.vendors)


if __name__ == "__main__":
    logging.basicConfig()
    run()