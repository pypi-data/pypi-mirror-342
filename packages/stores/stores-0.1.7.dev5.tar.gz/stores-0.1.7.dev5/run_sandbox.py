import stores  # noqa

index = stores.Index(
    ["silanthro/python-sandbox"],
    # env_var={
    #     "silanthro/python-sandbox": {
    #         "DENO_PATH": "/drive3/Silanthro/tools/python-sandbox/deno"
    #     }
    # },
)
print(index.tools)

# for value in index.stream_execute("sandbox.run_code", {"code": "1+1"}):
#     print(value)

print(index.execute("sandbox.run_code", {"code": "1+1"}))
