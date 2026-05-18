import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Calculator Tool
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

tools = [
    {
        "name": "calculator",
        "description": "You MUST always use this tool for ANY arithmetic calculation, no matter how simple. Never calculate anything yourself. Always use this tool.",
        'input_schema' : {
            'type': 'object',
            'properties': {
                'expression': {
                    'type': 'string',
                    'description': 'The mathematical expression to evaluate, e.g., "824 / 8".'
                }
            },
            'required': ['expression']
        }
    }
]

tool_map = {
    "calculator": calculator
}

messages = [
    {"role": "user", "content": "What is 4 multiplies 83 devided by 5, then minus 34?"}
]

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=messages,
    tools=tools,
    system="You are a calculator assistant. You MUST always use the provided calculator tool for ANY arithmetic calculation, no matter how simple. Never calculate anything yourself. Always use the provided calculator tool."
    )


if response.stop_reason == "tool_use":

    tool_use = next(block for block in response.content if block.type == "tool_use")

    tool_name = tool_use.name
    tool_input = tool_use.input
    tool_function = tool_map.get(tool_name)
    result = tool_function(**tool_input)

    print(f"Tool called: {tool_name}")
    print(f"Expression: {tool_input}")
    print(f"Result: {result}")


    messages.append({'role': 'assistant', 'content': response.content})
    messages.append({'role': 'user', 'content': [
        {
            'type': 'tool_result',
            'tool_use_id': tool_use.id,
            'content': result
        }
    ]})

    final_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=messages,
        tools=tools,
        system="You are a calculator assistant. You MUST always use the provided calculator tool for ANY arithmetic calculation, no matter how simple. Never calculate anything yourself. Always use the provided calculator tool."
    )


    print(f"\nClaude: {final_response.content[0].text}")
