# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import agent_worker_pb2 as agent__worker__pb2


class AgentRpcStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.OpenChannel = channel.stream_stream(
            "/agents.AgentRpc/OpenChannel",
            request_serializer=agent__worker__pb2.Message.SerializeToString,
            response_deserializer=agent__worker__pb2.Message.FromString,
        )
        self.GetState = channel.unary_unary(
            "/agents.AgentRpc/GetState",
            request_serializer=agent__worker__pb2.AgentId.SerializeToString,
            response_deserializer=agent__worker__pb2.GetStateResponse.FromString,
        )
        self.SaveState = channel.unary_unary(
            "/agents.AgentRpc/SaveState",
            request_serializer=agent__worker__pb2.AgentState.SerializeToString,
            response_deserializer=agent__worker__pb2.SaveStateResponse.FromString,
        )


class AgentRpcServicer(object):
    """Missing associated documentation comment in .proto file."""

    def OpenChannel(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def SaveState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AgentRpcServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "OpenChannel": grpc.stream_stream_rpc_method_handler(
            servicer.OpenChannel,
            request_deserializer=agent__worker__pb2.Message.FromString,
            response_serializer=agent__worker__pb2.Message.SerializeToString,
        ),
        "GetState": grpc.unary_unary_rpc_method_handler(
            servicer.GetState,
            request_deserializer=agent__worker__pb2.AgentId.FromString,
            response_serializer=agent__worker__pb2.GetStateResponse.SerializeToString,
        ),
        "SaveState": grpc.unary_unary_rpc_method_handler(
            servicer.SaveState,
            request_deserializer=agent__worker__pb2.AgentState.FromString,
            response_serializer=agent__worker__pb2.SaveStateResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "agents.AgentRpc", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class AgentRpc(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def OpenChannel(
        request_iterator,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            "/agents.AgentRpc/OpenChannel",
            agent__worker__pb2.Message.SerializeToString,
            agent__worker__pb2.Message.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetState(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/agents.AgentRpc/GetState",
            agent__worker__pb2.AgentId.SerializeToString,
            agent__worker__pb2.GetStateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def SaveState(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/agents.AgentRpc/SaveState",
            agent__worker__pb2.AgentState.SerializeToString,
            agent__worker__pb2.SaveStateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
