from concurrent import futures
import logging
import grpc
import product_service_pb2
import product_service_pb2_grpc
import vendor_service_pb2
import vendor_service_pb2_grpc
import time

from grpc_opentracing import open_tracing_server_interceptor
from grpc_opentracing.grpcext import intercept_server
from jaeger_client import Config

class ProductServiceImpl(product_service_pb2_grpc.ProductServiceServicer):

    def GetProductDetails(self, request, context):
        logging.info(f'Received request for product {request.id}')
        with grpc.insecure_channel('localhost:60051') as channel:
            stub = vendor_service_pb2_grpc.VendorServiceStub(channel)
            response = stub.GetVendorForProduct(vendor_service_pb2.ProductIdentifier(id=request.id))
        logging.info(f'got vendor list from vendor service {response.details}')

        return product_service_pb2.ProductDetails(id=request.id, quantity=10, vendors=response.details)

def serve():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='product_service')
    tracer = config.initialize_tracer()
    tracer_interceptor = open_tracing_server_interceptor(
        tracer, log_payloads=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_server(server, tracer_interceptor)
    product_service_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # server.wait_for_termination()
    try:
        while True:
            time.sleep(24*24*60)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(filename="product_server.log", level=logging.INFO)
    serve()
