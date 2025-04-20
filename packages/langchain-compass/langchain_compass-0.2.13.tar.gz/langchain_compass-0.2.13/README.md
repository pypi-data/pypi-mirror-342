# langchain-compass

The Compass-LangChain toolkit contains tools which enable an LLM agent to perform onchain operations on major DeFi protocols.

[YouTube Introduction](https://youtu.be/wotfGbu46wY)


# Setup

## Installation

```bash
pip install -U langchain-compass
```

## Environment Setup

```
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

# Usage:

## List Tools in Toolkit:

```python
from langchain_compass.toolkits import LangchainCompassToolkit

toolkit = LangchainCompassToolkit(compass_api_key=None)
tools = toolkit.get_tools()
for tool in tools:
    print(tool.name)
```

Expected output:
```bash
# output
aave_supply_
aave_borrow_
aave_repay_
aave_withdraw_
aave_asset_price_get_
...
```

## Using with an agent

```python
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_compass.toolkits import LangchainCompassToolkit
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()


# Initialize LLM - replace 'gpt-4o' with a model of your choice
llm = ChatOpenAI(model='gpt-4o')

# Get the DeFi tools from LangchainCompassToolkit
tools = LangchainCompassToolkit(compass_api_key=None).get_tools()

# Setup memory for your agent
memory = MemorySaver()

# Create a ReAct agent with the specified LLM, tools, and memory
agent = create_react_agent(
    llm,
    tools=tools,
    checkpointer=memory,
    prompt="You are a helpful agent that can interact onchain using tools that you've been told how to use. If you are uncertain that you have sufficient information to call your tools then please ask the user for more information until you have sufficient information to call your tool."
)

# Example user query
from langchain_core.messages import HumanMessage
user_input = 'what is the balance of vitalic.eth.'

# Optional config data, such as thread IDs or session context
config = {"configurable": {"thread_id": "abc123"}}

# Invoke the agent with the user query
output = agent.invoke(input={"messages": [HumanMessage(content=user_input)]}, config=config)

# Display the agent's final response
print(output["messages"][-1].content)
```

Expected output:
```bash
$ python main.py 
The balance of the wallet associated with **vitalik.eth** is approximately **$486,222.54**. Here's a breakdown of the token balances:

- **1INCH**: 6.037 ($1.03)
- **AAVE**: 0.010 ($1.43)
- **BAL**: 0.932 ($1.04)
- **crvUSD**: 0.775 ($0.78)
- **DAI**: 317,203.872 ($317,242.95)
- **ENS**: 1,144.036 ($16,710.33)
- **LINK**: 1.778 ($22.52)
- **rsETH**: 0.00003 ($0.05)
- **UNI**: 0.000017 ($0.00009)
- **USDC**: 123,223.707 ($123,215.08)
- **USDT**: 170.148 ($170.12)
- **WBTC**: 0.00107 ($91.93)
- **WETH**: 16.395 ($28,765.28)

These values are subject to market fluctuations.
```

## Run the agent interactively based on user input.

To run the agent interactively please add this snippet to the bottom of the code in the previous section.

```python
from rich.console import Console
from rich.markdown import Markdown
console = Console()
print("Starting chat mode... Type 'exit' to end.")
while True:
    user_input = input("\nPrompt: ")
    output = agent.invoke(input = {"messages": [HumanMessage(content=user_input)]}, config=config)
    answer = output["messages"][-1].content
    console.print(Markdown(answer))
```

## Next Steps


To see a full implementation of a LangChain agent using these tools, please check out our [GitHub repo here](https://github.com/CompassLabs/compass_ai/).
