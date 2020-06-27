import grpc
from snowflake.snowflake_pb2 import Request
from snowflake.snowflake_pb2_grpc import SnowFlakeStub


class SnowFlakeClient:
    snowflake = None

    @classmethod
    def get_unique_url_id(cls) -> str:
        request = Request()
        response = cls.snowflake.get_unique_url_id(request)
        return response.value

    @classmethod
    def get_unique_user_id(cls) -> int:
        request = Request()
        response = cls.snowflake.get_unique_user_id(request)
        return response.value


def setup_snowflake_client(configuration):
    channel = grpc.insecure_channel(
        "%s:%s" % (configuration.snowflake_host, configuration.snowflake_port)
    )
    SnowFlakeClient.snowflake = SnowFlakeStub(channel)
