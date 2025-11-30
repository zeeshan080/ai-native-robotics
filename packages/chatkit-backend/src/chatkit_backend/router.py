"""
Event router for ChatKit API.

Handles incoming chat requests and streams responses from the tutor agent.
"""

import logging
from typing import AsyncIterator

from agents import Runner, RawResponsesStreamEvent

from .models import ChatRequest, ChatEvent, EventType
from .agents import create_tutor_agent


logger = logging.getLogger(__name__)


# Singleton tutor agent instance
_tutor_agent = None


def get_tutor_agent():
    """Get or create the tutor agent singleton."""
    global _tutor_agent
    if _tutor_agent is None:
        _tutor_agent = create_tutor_agent()
    return _tutor_agent


async def handle_chat_request(request: ChatRequest) -> AsyncIterator[ChatEvent]:
    """
    Handle a chat request and stream the agent's response.

    Args:
        request: The validated chat request from the frontend

    Yields:
        ChatEvent instances for streaming to the client

    The function:
    1. Extracts the user's message
    2. Runs the tutor agent with streaming enabled
    3. Converts agent output chunks to ChatEvent format
    4. Handles errors gracefully with user-friendly messages
    """
    try:
        # Get the tutor agent
        agent = get_tutor_agent()

        # Prepare the input message
        user_message = request.message.content
        message_id = request.message.id

        # Add page context if provided
        if request.context and request.context.pageUrl:
            context_info = f"\n\n[Student is viewing: {request.context.pageTitle or request.context.pageUrl}]"
            user_message += context_info

        logger.info(f"Processing chat request {message_id}: {user_message[:100]}...")

        # Run the agent with streaming (openai-agents SDK v0.6+)
        result = Runner.run_streamed(
            starting_agent=agent,
            input=user_message
        )

        # Stream the response chunks
        accumulated_response = ""
        async for event in result.stream_events():
            # Handle raw response events which contain the streaming text
            if isinstance(event, RawResponsesStreamEvent):
                data = event.data
                # Check for text delta events (ResponseTextDeltaEvent)
                if hasattr(data, 'type') and data.type == 'response.output_text.delta':
                    if hasattr(data, 'delta') and data.delta:
                        text = data.delta
                        accumulated_response += text

                        # Yield text delta event
                        yield ChatEvent(
                            type=EventType.TEXT_DELTA,
                            content=text,
                            done=False,
                            messageId=message_id
                        )

        # Log the final response
        logger.info(f"Completed response for {message_id}: {len(accumulated_response)} chars")

        # Yield completion event
        yield ChatEvent(
            type=EventType.MESSAGE_COMPLETE,
            content=None,
            done=True,
            messageId=message_id
        )

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error processing chat request {request.message.id}: {e}", exc_info=True)

        # Yield user-friendly error event
        yield ChatEvent(
            type=EventType.ERROR,
            content="Sorry, I encountered an error processing your request. Please try again.",
            done=True,
            messageId=request.message.id
        )
