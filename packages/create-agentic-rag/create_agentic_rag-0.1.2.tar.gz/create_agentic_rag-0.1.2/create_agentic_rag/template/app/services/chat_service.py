import json
import time

from app.api.models import ChatCompletionRequest
from app.config import settings
from app.rag.graph import build_rag_graph
from app.utils.helpers import (
    convert_to_langgraph_messages,
    create_openai_response,
    estimate_tokens,
    format_sse_chunk,
)
from app.utils.logging import logger
from fastapi import HTTPException
from fastapi.responses import StreamingResponse


class ChatService:
    # Singleton instance
    _instance = None
    # Cache of RAG graphs by model_name
    _rag_graphs = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatService, cls).__new__(cls)
        return cls._instance

    def _get_rag_graph(self, model_name: str = None):
        """Get or create a RAG graph for the specified model."""
        # Ensure we have a valid model name or use default
        model_name = model_name or settings.LLM_MODEL

        # Create a cache key
        cache_key = model_name

        # Return cached graph if exists
        if cache_key in self._rag_graphs:
            return self._rag_graphs[cache_key]

        # Create and cache new graph
        graph = build_rag_graph(model_name)
        self._rag_graphs[cache_key] = graph
        return graph

    async def chat(self, request: ChatCompletionRequest):
        """Process chat completions in OpenAI format."""
        # Use model from request or default from settings
        model_name = request.model or settings.LLM_MODEL

        if request.stream:
            return StreamingResponse(
                self._stream_chat_response(request, model_name),
                media_type="text/event-stream",
            )
        return await self._direct_chat_response(request, model_name)

    async def _stream_chat_response(
        self, request: ChatCompletionRequest, model_name: str = None
    ):
        """Stream chat response in OpenAI SSE format."""
        try:
            # Ensure model_name is valid
            model_name = model_name or settings.LLM_MODEL

            # Get the right graph for the model
            rag_graph = self._get_rag_graph(model_name)

            # Convert messages to LangGraph format
            input_messages = convert_to_langgraph_messages(request.messages)

            created_at = time.time()
            # Stream the content
            async for message, metadata in rag_graph.astream(
                {"messages": input_messages},
                stream_mode="messages",
            ):
                if (
                    hasattr(message, "content")
                    and message.content
                    and message.type != "tool"
                ):
                    chunk = format_sse_chunk(
                        model=model_name, message=message, created_at=created_at
                    )
                    yield f"data: {json.dumps(chunk)}\n\n"
                elif (
                    message.content == ""
                    and message.tool_calls
                    and message.type != "tool"
                ):
                    # Handle the case where the content is empty but the tool_calls are not
                    message.content = "\n\n"
                    chunk = format_sse_chunk(
                        model=model_name, message=message, created_at=created_at
                    )
                    yield f"data: {json.dumps(chunk)}\n\n"

            # Final chunk
            final_chunk = format_sse_chunk(model=model_name, finish_reason="stop")
            yield f"data: {json.dumps(final_chunk)}\n\n"

            # End the stream
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Error in streaming response: {str(e)}", exc_info=True)
            error_chunk = {"error": {"message": str(e), "type": "server_error"}}
            yield f"data: {json.dumps(error_chunk)}\n\n"
            yield "data: [DONE]\n\n"

    async def _direct_chat_response(
        self, request: ChatCompletionRequest, model_name: str = None
    ):
        """Direct chat response."""
        try:
            # Ensure model_name is valid
            model_name = model_name or settings.LLM_MODEL

            # Get the right graph for the model
            rag_graph = self._get_rag_graph(model_name)

            # Convert messages to LangGraph format
            input_messages = convert_to_langgraph_messages(request.messages)

            # Invoke the graph
            result = await rag_graph.ainvoke({"messages": input_messages})

            # Extract the final assistant message
            final_message = result["messages"][-1]
            content = final_message.content if hasattr(final_message, "content") else ""

            # Estimate token usage (rough estimation)
            prompt_tokens = sum(
                estimate_tokens(msg.content) for msg in request.messages
            )
            completion_tokens = estimate_tokens(content)

            # Format response like OpenAI
            response = create_openai_response(
                content=content,
                model=model_name,
                prompt_tokens=int(prompt_tokens),
                completion_tokens=int(completion_tokens),
            )

            return response

        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
