import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

# Session Memory in JSON format
import json

HISTORY_FILE = "conversation.json"

def save_history(messages):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(messages, f, indent=2)
    
    print (f"Conversation history saved to {HISTORY_FILE}")

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            messages = json.load(f)
            print(f"Conversation history loaded from {HISTORY_FILE}")
            return messages
    except FileNotFoundError:
        return []

# tools
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def unit_convertor(value, from_unit, to_unit):
    conversions = {
        ("miles", "km"): lambda x: x * 1.60934,
        ("km", "miles"): lambda x: x / 1.60934,
        ('kg', 'pounds'): lambda x: x * 2.20462,
        ('pounds', 'kg'): lambda x: x / 2.20462,
        ('celsius', 'fahrenheit'): lambda x: (x * 9/5) + 32,
        ('fahrenheit', 'celsius'): lambda x: (x - 32) * 5/9,
        ('metres', 'feet'): lambda x: x * 3.28084,
        ('feet', 'metres'): lambda x: x / 3.28084
    }

    key = (from_unit.lower(), to_unit.lower())

    if key not in conversions:
        return f"Error: Conversion from {from_unit} to {to_unit} not supported."

    result = conversions[key](value)
    return f"{value} {from_unit} = {round(result, 4)} {to_unit}"



tool_map ={
    "calculator": calculator,
    "unit_convertor": unit_convertor
}

tools = [
    {
        "name": "calculator",
        "description": "Always use this for ANY arithmetic. Never calculate yourself.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The arithmetic expression to evaluate e.g. '10 * 5'"
                }
            },
            "required": ["expression"]
        }
    },

    {
        "name": "unit_convertor",
        "description": "Use this tool to convert between units of measurement — distance, weight, temperature. Never convert units from memory, always use this tool.",
        "input_schema": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "The numeric value to convert e.g. 9"
                },
                "from_unit": {
                    "type": "string",
                    "description": "The unit to convert from e.g. 'miles', 'kg', 'celsius'"
                },
                "to_unit": {
                    "type": "string",
                    "description": "The unit to convert to e.g. 'km', 'pounds', 'fahrenheit'"
                },
            },
            "required": ["value", "from_unit", "to_unit"]
        }
    }
]

system = """You are a helpful assistant with a calculator tool.
Always use the calculator tool for any arithmetic. Never calculate yourself. Never convert units from memory, always use the unit_convertor tool for unit conversions."""



# Agent Loop
def run_agent(user_input, messages):
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == 'end_turn':
            reply = response.content[0].text
            messages.append({"role": "assistant", "content": reply})
            return reply

        if response.stop_reason == 'tool_use':
            messages.append({"role": "assistant", "content": [
                block.model_dump() for block in response.content
            ]})

            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    result = tool_map[tool_name](**tool_input)
                    print(f"  [tool: {tool_name} | input: {tool_input} | result: {result}]")

                    messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                'type': "tool_result",
                                "tool_use_id": block.id,
                                "content": result
                                }
                            ]
                        }
                    )

# Chat Loop

def main():
    messages = load_history()
    print("Agent ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'quit':
            save_history(messages)
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        reply = run_agent(user_input, messages)
        print(f"Claude: {reply}\n")

if __name__ == "__main__":
    main()

