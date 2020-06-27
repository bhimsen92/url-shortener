import grpc
from concurrent import futures
import time
import os
import snowflake_pb2
import snowflake_pb2_grpc
from id_generator import IdGenerator

BASE62 = "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-"


class SnowFlakeService(snowflake_pb2_grpc.SnowFlakeServicer):
    def __init__(self, url_id_generator: IdGenerator, user_id_generator: IdGenerator):
        self.url_id_generator = url_id_generator
        self.user_id_generator = user_id_generator

    def get_unique_url_id(self, request, context):
        unique_id = self.encode(self.url_id_generator.next_id())
        return_value = snowflake_pb2.UniqueUrlID(value=unique_id)
        return return_value

    def get_unique_user_id(self, request, context):
        unique_id = self.user_id_generator.next_id()
        return_value = snowflake_pb2.UniqueUserID(value=unique_id)
        return return_value

    @staticmethod
    def encode(num, alphabet=BASE62):
        if num == 0:
            return alphabet[0]
        arr = []
        base = len(alphabet)
        while num:
            num, rem = divmod(num, base)
            arr.append(alphabet[rem])
        arr.reverse()
        return "".join(arr)


def main():
    # load machine/service id.
    service_id = os.environ.get("SERVICE_ID", 1)
    url_id_generator = IdGenerator(service_id)
    user_id_generator = IdGenerator(service_id)
    snowflake_service = SnowFlakeService(url_id_generator, user_id_generator)

    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    snowflake_pb2_grpc.add_SnowFlakeServicer_to_server(snowflake_service, server)

    server.add_insecure_port("[::]:%s" % os.environ.get("SNOWFLAKE_SERVICE_PORT", 5000))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


main()
