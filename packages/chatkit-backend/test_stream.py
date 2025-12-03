import asyncio
import os
os.environ['LLM_PROVIDER'] = 'gemini'
os.environ['GEMINI_API_KEY'] = 'AIzaSyB4wtkAtJkag6Ib3RbWp7WnK3oiKYN5iZY'
os.environ['GEMINI_DEFAULT_MODEL'] = 'gemini-2.5-flash'

from chatkit_backend.agents import create_tutor_agent
from agents import Runner, RawResponsesStreamEvent

async def test():
    agent = create_tutor_agent()
    result = Runner.run_streamed(starting_agent=agent, input="Say hi")

    async for event in result.stream_events():
        etype = type(event).__name__
        print(f"Event: {etype}")
        if isinstance(event, RawResponsesStreamEvent):
            data = event.data
            print(f"  data: {data}")

asyncio.run(test())
