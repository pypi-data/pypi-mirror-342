# import anthropic
import inspect

import dotenv
from langchain_core.tools import tool as callable_as_lc_tool
from langchain_google_genai import ChatGoogleGenerativeAI

# from openai import OpenAI
# from google import genai
# from google.genai import types
# from litellm import completion
# from stores.indexes import LocalIndex
import stores

dotenv.load_dotenv()


# def foo(bar: str = "test"):
#     return bar


# index = stores.Index([foo])
# print(inspect.signature(index.tools[0]))
# print(index.tools[0]())
# quit()


index = stores.Index(
    ["silanthro/todoist"],
    env_var={
        "silanthro/todoist": {
            "TODOIST_API_TOKEN": "6a0815ff164d7ebd6d45d433bdbd32fcb164e1ec",
        }
    },
)

sig = inspect.signature(index.tools[0])
print(sig)

wrap = callable_as_lc_tool()(index.tools[0])
sig_wrap = inspect.signature(wrap)
print(sig_wrap)
# quit()

for argname, arg in sig.parameters.items():
    print(argname)
    print(arg.annotation)
    print([arg.default])

# print(sig)
# quit()

# result = index.execute(
#     "todoist.get_tasks",
#     {
#         "project_id": None,
#         "search_query": None,
#         "due_date_filter": "today",
#         "priority": None,
#         "other_filters": None,
#         "limit": None,
#     },
# )
# print(result)
# quit()


task = "Find tasks of priority 1"

# print(index.tools)

# print(index.format_tools("openai-chat-completions"))
# quit()

# client = OpenAI()
# response = client.responses.create(
#     model="gpt-4o-mini-2024-07-18",
#     input=[{"role": "user", "content": task}],
#     tools=index.format_tools("openai-responses"),
# )
# client = anthropic.Anthropic()
# response = client.messages.create(
#     model="claude-3-5-sonnet-20241022",
#     max_tokens=1024,
#     messages=[{"role": "user", "content": task}],
#     tools=index.format_tools("anthropic"),
# )
# response = completion(
#     model="gemini/gemini-2.0-flash-001",
#     messages=[
#         {
#             "role": "user",
#             "content": task,
#         }
#     ],
#     tools=index.format_tools("google-gemini"),
# )
# client = genai.Client(
#     # api_key=os.environ["GEMINI_API_KEY"],
# )
# config = types.GenerateContentConfig(
#     tools=index.tools,
#     automatic_function_calling=types.AutomaticFunctionCallingConfig(
#         disable=True  # Gemini automatically executes tool calls. This script shows how to manually execute tool calls.
#     ),
# )

# # Get the response from the model
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=task,
#     config=config,
# )
# tool_call = response.candidates[0].content.parts[0].function_call

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")
model_with_tools = model.bind_tools(index.tools)
response = model_with_tools.invoke(task)
tool_call = response.tool_calls[0]

print(tool_call)
# Execute the tool call
# print(response)
