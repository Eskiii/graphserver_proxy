from langgraph_sdk import get_client
import asyncio
from langgraph_sdk.schema import Command
# from logger import logger
from utils import create_headers


if __name__ == "__main__":
    async def main():
        # 主图逻辑
        app_id = "9556C54317CE4B8F9468"
        # api_key = "44CBD47552824EC6BF3DF24CD82B2F0F"
        api_key = "9A5611568A8443DD856D241F6462B518"
        api_host = "172.16.251.149"
        assistant_id = "afb46ad576eb26093f1814dfec439eef"
        api_url = "http://172.16.251.149:9062/openapi/v2/graph/api/v2.0/graphApp/"+assistant_id
        headers = create_headers(app_id=app_id, app_secret=api_key, host=api_host)
        client = get_client(url=api_url, api_key=api_key, headers=headers)
        thread = await client.threads.create()
        thread_id = thread.get("thread_id")
        inputs = {"messages": [{"role": "user", "content": [{"role": "user", "content": "锁等待"}]}]}
        agent_name = "saas_flow"
        interrupt_tmp = {}
        subsaas_values = {}
        assistant_id = "f90ed4e9-5c83-50ae-b65c-74ab0fa26f98"
        async for mode, data in client.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            input=inputs,
            stream_mode=[
            "updates",
            "events"
            ],
            # stream_subgraphs=True,
        ):
            print(f"mode: {mode}")
            if data:
                print(f"data.keys(): {data.keys()}")
            if mode == "events":
                graph_event = data["event"]
                name = data["name"]
                print(f"event: {graph_event} - name: {name}")
                if name == agent_name:
                    print(f"{agent_name} end...")
            if data and "__interrupt__" in data:
                print(f"Interrupted: {data}")
                subsaas_values = data['__interrupt__'][0].get("value")
                print(f"interrupt subsaas_values: {subsaas_values}")
                break

        # state = await client.threads.get_state(thread_id=thread_id)
        # next = state.get("next")
        # values = state.get("values")
        # checkpointer = state.get("checkpoint")
        # interrupts = state.get("interrupts")
        # logger.info(f"next: {next}, values: {values}")
        # logger.info(f"checkpointer: {checkpointer}")
        # logger.info(f"interrupts: {interrupts}")
        # logger.info(f"subsaas_values: {subsaas_values}")

        resume = True
        resume_params = "test resume_params"
        runs = True
        end_node_name = "end_node"
        if resume:
            while runs:
                print("graph resume...")
                async for mode, data in client.runs.stream(
                thread_id=thread_id,
                assistant_id=assistant_id,
                stream_mode=[
                "updates",
                "events"
                ],
                config={
                    "configurable":subsaas_values
                },
                command=Command(resume=resume_params),
                # stream_subgraphs=True,
                ):
                    print(f"mode: {mode}")
                    if data:
                        print(f"data.keys(): {data.keys()}")
                    if mode == "events":
                        graph_event = data["event"]
                        name = data["name"]
                        print(f"event: {graph_event} - name: {name}")
                        if "on_chain_end" in graph_event and name == end_node_name:
                            runs = False
                            print(f"{agent_name} end...")
                            break
                    if mode == "error":
                        runs = False
                        print(f"data: {data}")
                    if data and "__interrupt__" in data:
                        dynamic_params = data['__interrupt__'][0].get("value")
                        print(f"Interrupted: {data}, type: {type(dynamic_params)}")
                        # resume_params = input(f"need inputs:")
                        resume_params = {}
                        # 弹窗逻辑
                        for k, v in dynamic_params.items():
                            hint = f"请输入{k}，默认值{v}:"
                            print(hint)
                            user_input = input()
                            resume_params[k] = user_input
                if not runs:
                    break
                # state = await client.threads.get_state(thread_id=thread_id)
                # # next = state.get("next")
                # values = state.get("values")
                # checkpointer = state.get("checkpoint")
                # interrupts = state.get("interrupts")
                # print(f"next: {next}, values: {values}")
                # logger.info(f"checkpointer: {checkpointer}")
                # logger.info(f"interrupts: {interrupts}")

    asyncio.run(main())