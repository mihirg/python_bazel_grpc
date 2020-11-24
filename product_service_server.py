from concurrent import futures
import logging
import grpc
import product_service_pb2
import product_service_pb2_grpc

class ProductServiceImpl(product_service_pb2_grpc.ProductServiceServicer):

    def GetProductDetails(self, request, context):
        return product_service_pb2.ProductDetails(id=1, quantity=10, vendors="test")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig();
    serve()
