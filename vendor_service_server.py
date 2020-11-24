from concurrent import futures
import logging
import grpc
import vendor_service_pb2
import vendor_service_pb2_grpc

import time

from grpc_opentracing import open_tracing_server_interceptor
from grpc_opentracing.grpcext import intercept_server
from jaeger_client import Config


class VendorServiceImpl(vendor_service_pb2_grpc.VendorServiceServicer):

    def GetVendorForProduct(self, request, context):
        logging.info(f'Received request for product {request.id}')
        return vendor_service_pb2.VendorDetails(details=f"These are vendor details for product {request.id} ")

def serve():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='vendor_service')
    tracer = config.initialize_tracer()
    tracer_interceptor = open_tracing_server_interceptor(
        tracer, log_payloads=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_server(server, tracer_interceptor)
    vendor_service_pb2_grpc.add_VendorServiceServicer_to_server(VendorServiceImpl(), server)
    server.add_insecure_port('[::]:60051')
    server.start()
    # server.wait_for_termination()
    try:
        while True:
            time.sleep(24*24*60)
    except KeyboardInterrupt:
        server.stop(0)



if __name__ == '__main__':
    logging.basicConfig(filename="vendor_server.log", level=logging.INFO)
    serve()
