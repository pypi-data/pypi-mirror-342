# Knit LangGraph SDK

Welcome to the Knit's LangGraph SDK, a powerful toolkit designed to integrate AI-powered agents built using LangGraph with a wide range of SaaS applications. 

As an embedded integration platform, Knit provides a white-labeled solution empowering SaaS companies to effortlessly scale integrations within their own products, enriching customer experiences with dynamic, out-of-the-box functionality.

The Knit LangGraph SDK is designed to facilitate seamless integration between LLM agents and SaaS applications by leveraging Knit's platform and its wide range of connectors. 

## Installation

Kickstart your journey with the Knit LangGraph SDK by installing it via pip:

```bash
pip install knit-langgraph
```

## Quick Start

First, get your Knit API Key by signing up at [https://dashboard.getknit.dev/signup](https://dashboard.getknit.dev/signup)

Now, we're ready to start using the SDK. Here's a simple guide to help you start integrating with the Knit LangGraph SDK:

```python
import logging
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from knit_langgraph import KnitLangGraph, ToolFilter

# Initialize the Knit SDK with your API key
knit = KnitLangGraph(api_key="YOUR_KNIT_API_KEY")

# Initialize your LLM
model = ChatOpenAI(
    api_key="YOUR_OPENAI_API_KEY",
    model="gpt-4o",  # or another model of your choice
    temperature=0,
)

# Discover available tools from a specific app.
# You can then select which tools to pass to the LLM model from these
tools = knit.find_tools(app_id="charliehr")

# Get specific tools you want to pass to the LLM model.
tool_defs = knit.get_tools(tools=[ToolFilter(app_id="charliehr", tool_ids=[tool.tool_id for tool in tools])])

# Create a ReAct agent with the tools
graph = create_react_agent(model, tools=tool_defs)

# Prepare inputs for the agent
inputs = {
    "messages": [
        (
            "user",
            "I want to get the list of offices of the company.",
        )
    ]
}

# Configuration with integration ID
config = {"knit_integration_id": "YOUR_USER's_INTEGRATION_ID"}

# Stream the agent's responses
for response in graph.stream(inputs, {"configurable": config}, stream_mode="values"):
    message = response["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()
```

That's it! It's that easy to get started and add hundreds of SaaS applications to your AI Agent. 

## Detailed Information
That was a quick introduction of how to get started with Knit's LangGraph SDK. 

To know more about how to use its advanced features and for more in depth information, please refer to the detailed guide here: [Knit LangGraph SDK Guide](https://developers.getknit.dev/docs/knit-ai-lanngraph-sdk)

## Support

For support, reach out to kunal@getknit.dev