from django.http import StreamingHttpResponse, HttpResponse
from pydantic_ai.messages import UserPrompt, ModelTextResponse
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from lubricentro_myc.chatbot.agent import agent
from lubricentro_myc.chatbot.database import database
from lubricentro_myc.chatbot.types import MessageTypeAdapter
from lubricentro_myc.chatbot.utils import async_to_sync_gen


class ChatView(APIView):
    # parser_classes = [FormParser, MultiPartParser]

    # TODO: remove this, I DO need authentication
    authentication_classes = []
    permission_classes = []

    """
    curl -X POST http://192.168.0.69:8000/lubricentro_myc/chatbot/ -F prompt="hello!""
    
    curl -X POST http://192.168.0.69:8000/lubricentro_myc/chatbot/ \
     -H "Content-Type: application/json" \
     -d '{"prompt": "hello!"}'
    """

    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response(
                {"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        async def stream_messages():
            """Streams new line delimited JSON `Message`s to the client."""
            # stream the user prompt so that can be displayed straight away
            yield MessageTypeAdapter.dump_json(UserPrompt(content=prompt)) + b"\n"

            # get the chat history so far to pass as context to the agent
            messages = list(database.get_messages())

            # run the agent with the user prompt and the chat history
            async with agent.run_stream(prompt, message_history=messages) as result:
                async for text in result.stream(debounce_by=0.01):
                    m = ModelTextResponse(content=text, timestamp=result.timestamp())
                    yield MessageTypeAdapter.dump_json(m) + b"\n"

            # add new messages (e.g. the user prompt and the agent response in this case) to the database
            database.add_messages(result.new_messages_json())

        return StreamingHttpResponse(
            async_to_sync_gen(lambda: stream_messages()), content_type="text/plain"
        )

    def get(self, request, *args, **kwargs):
        messages = database.get_messages()
        return HttpResponse(
            b"\n".join(MessageTypeAdapter.dump_json(m) for m in messages),
            content_type="text/plain",
        )
