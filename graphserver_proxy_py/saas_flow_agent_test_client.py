from langgraph_sdk import get_client
import asyncio
from langgraph_sdk.schema import Command
# from logger import logger
from utils import create_headers

if __name__ == "__main__":
    async def main():
        # app_id = "C761D82552BD4C31AF49"
        app_id = "9556C54317CE4B8F9468"
        # api_key = "44CBD47552824EC6BF3DF24CD82B2F0F"
        api_key = "9A5611568A8443DD856D241F6462B518"
        api_host = "172.16.251.149"
        assistant_id = "afb46ad576eb26093f1814dfec439eef"
        api_url = "http://172.16.251.149:9062/openapi/v2/graph/api/v2.0/graphApp/"+assistant_id
        headers = create_headers(app_id=app_id, app_secret=api_key, host=api_host)
        client = get_client(url=api_url, api_key=api_key, headers=headers)
        # 主图逻辑
        # client = get_client(url="http://localhost:2024")
        thread = await client.threads.create()
        thread_id = thread.get("thread_id")
        ASSISTANT_ID = ""
        try:

            # 调用 assistants.search() 方法 (异步)
            print("正在调用 await client.assistants.search()...")
            result = await client.assistants.search()
            
            # 输出结果
            print("搜索结果:")
            print(f"类型: {type(result)}")
            print(f"内容: {result}")
            ASSISTANT_ID = result[0].get('assistant_id') if result else ""
        except Exception as e:
            print(f"调用失败: {e}")
        inputs = {"messages": [{"role": "user", "content": [{
                        "type": "human",
                        "content": "11",
                        "id": "e9673158-5504-4373-bdd9-c593c3b79801"
                    }]}]}
        agent_name = "saas_flow"
        interrupt_tmp = {}
        subsaas_values = {}
        print(f"ASSISTANT_ID1: {ASSISTANT_ID}")
        async for mode, data in client.runs.stream(
            thread_id=None,
            assistant_id=ASSISTANT_ID,
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
                # print(f"Interrupted: {data}")
                subsaas_values = data['__interrupt__'][0].get("value")
                # print(f"interrupt subsaas_values: {subsaas_values}")
                break
        resume = True
        resume_params = "test resume_params"
        runs = True
        end_node_name = "end_node"
        # print(f"subsaas_values: {subsaas_values}")
#         try:

#             # 调用 assistants.search() 方法 (异步)
#             print("正在调用 await client.assistants.search()...")
#             result = await client.assistants.search()
            
#             # 输出结果
#             print("搜索结果:")
#             print(f"类型: {type(result)}")
#             print(f"内容: {result}")
#             ASSISTANT_ID = result[0].get('assistant_id') if result else ""
#         except Exception as e:
#             print(f"调用失败: {e}")
#         # inputs = {"messages": [{"role": "user", "content": [{
#         #                 "type": "human",
#         #                 "content": "11",
#         #                 "id": "e9673158-5504-4373-bdd9-c593c3b79801"
#         #             }]}]}
#         print(f"ASSISTANT_ID2: {ASSISTANT_ID}")
#         txt = """
# flowchart TD
#     A(["开始"]) --> C["表操作_获取膨胀率超过阈值的表"]
#     C --> D{"表操作_检查表的膨胀率是否过大"}
#     D -- 否 --> n15
#     D -- 是 --> n17["表操作_对表做统计信息收集"]
#     n1{"表操作_检查表的膨胀率是否过大"} -- 是 --> n2["表膨胀回收操作_对膨胀表进行数据回收"]
#     n1 -- 否 --> n3["表膨胀回收操作_表膨胀瞬时值可忽略告警"]
#     n2 --> n4["表膨胀回收操作_查看表回收情况"]
#     n4 --> n5{"表膨胀回收操作_检查表膨胀是否回收成功"}
#     n6["事务操作_查询阻塞vacuum的长事务"] --> n19["会话操作_人工选择长事务处理情况"]
#     n7["会话操作_查杀指定后台线程的数据库会话"] --> n8["事务操作_查询阻塞vacuum的长事务查杀情况"]
#     n8 --> n9{"事务操作_长事务查杀是否成功"}
#     n9-- 否 --> n10["会话操作_人工选择是否立即进行主备切换"]
#     n10 --> n25{"会话操作_是否立即进行主备切换"}
#     n25 -- 是 --> n26["集群操作_数据库集群主备切换"]
#     n25 -- 否 --> n27["hint：会话操作_请联系工程师支持"]
#     n26 --> n23["表膨胀回收操作_对膨胀表进行数据回收"]
#     n27 --> n15
#     n5 -- 是 --> n11["表膨胀回收操作_表膨胀问题已解决"]
#     n5 -- 否 --> n12["事务操作_查看事务ID推进情况"]
#     n12 --> n13{"事务操作_检查事务ID是否有推进"}
#     n13 -- 否 --> n6
#     n13 -- 是 --> n14["表膨胀回收操作_表膨胀在回收中可忽略告警"]
#     n11 --> n15(["结束"])
#     n14 --> n15
#     n3 --> n15
#     n17 --> n18["表操作_查看表的膨胀率"]
#     n18 --> n1
#     n19 --> n20{"会话操作_长事务是否可以查杀"}
#     n20 -- 是 --> n7
#     n20 -- 否 --> n21["事务操作_等待事务继续执行"]
#     n21 --> n22["表膨胀回收操作_需等待长事务持续完毕可忽略告警"]
#     n22 --> n15
#     n9 -- 是 --> n24["表膨胀回收操作_对膨胀表进行数据回收"]
#     n23 --> n15
#     n24 --> n15        
# """
#         subsaas_values = {
#             "mermaid_nodes": '[{"id": "n3", "name": "\u8868\u81a8\u80c0\u56de\u6536\u64cd\u4f5c_\u8868\u81a8\u80c0\u77ac\u65f6\u503c\u53ef\u5ffd\u7565\u544a\u8b66", "node_type": "plugin", "tool": {"tool_name": "f967e8ac323147cfab6388cb5c804b78@@vacuum_ops_show_result_vacuum_done_auto", "tool_desc": "\u8868\u81a8\u80c0\u56de\u6536\u64cd\u4f5c_\u8868\u81a8\u80c0\u77ac\u65f6\u503c\u53ef\u5ffd\u7565\u544a\u8b66", "tool_origin_desc": "\u8868\u81a8\u80c0\u56de\u6536\u64cd\u4f5c_\u8868\u81a8\u80c0\u77ac\u65f6\u503c\u53ef\u5ffd\u7565\u544a\u8b66", "input_params": [], "output_params": [{"param_name": "output", "param_desc": "\u8f93\u51fa", "param_value": null, "paramEnumList": null}], "enum_key": null, "enum_value": null, "need_interrupt": false}}]',
#             "mermaid_edges": '[{"start": {"id": "n17", "name": "\u8868\u64cd\u4f5c_\u5bf9\u8868\u505a\u7edf\u8ba1\u4fe1\u606f\u6536\u96c6", "node_type": "plugin", "tool": {"tool_name": "f967e8ac323147cfab6388cb5c804b78@@table_ops_analyze_dilate_tables", "tool_desc": "\u8868\u64cd\u4f5c_\u5bf9\u8868\u505a\u7edf\u8ba1\u4fe1\u606f\u6536\u96c6", "tool_origin_desc": "\u8868\u64cd\u4f5c\uff08\u5bf9\u8868\u505a\u7edf\u8ba1\u4fe1\u606f\u6536\u96c6)", "input_params": [{"param_name": "cluster_ip", "param_desc": "cluster_ip", "param_value": "panweidb_10.248.36.1", "paramEnumList": null}, {"param_name": "table_list", "param_desc": "table_list", "param_value": null, "paramEnumList": null}, {"param_name": "database", "param_desc": "database", "param_value": null, "paramEnumList": null}], "output_params": [], "enum_key": null, "enum_value": null, "need_interrupt": true}}, "end": {"id": "n18", "name": "\u8868\u64cd\u4f5c_\u67e5\u770b\u8868\u7684\u81a8\u80c0\u7387", "node_type": "plugin", "tool": {"tool_name": "f967e8ac323147cfab6388cb5c804b78@@table_ops_query_tables_dilate", "tool_desc": "\u8868\u64cd\u4f5c_\u67e5\u770b\u8868\u7684\u81a8\u80c0\u7387", "tool_origin_desc": "\u8868\u64cd\u4f5c\uff08\u67e5\u770b\u8868\u7684\u81a8\u80c0\u7387)", "input_params": [{"param_name": "cluster_ip", "param_desc": "cluster_ip", "param_value": "panweidb_10.248.36.1", "paramEnumList": null}, {"param_name": "database", "param_desc": "\u6570\u636e\u5e93", "param_value": "testdb", "paramEnumList": null}, {"param_name": "table_list", "param_desc": "table_list", "param_value": null, "paramEnumList": null}], "output_params": [{"param_name": "return_code", "param_desc": "\u8868\u81a8\u80c0\u60c5\u51b5", "param_value": null, "paramEnumList": [{"id": "9a317f082f91486bae778e9a5e571b4e", "outputId": "9ddd1b435eb84e829c2916a574aed43d", "enumValue": "1", "description": "\u8868\u64cd\u4f5c_\u68c0\u67e5\u8868\u7684\u81a8\u80c0\u7387\u662f\u5426\u8fc7\u5927\uff08\u5426\uff09", "outputConvertText": "return_code=1:\u65e0\u8868\u81a8\u80c0\u60c5\u51b5"}, {"id": "f0fef763189341bfada13a009494f033", "outputId": "9ddd1b435eb84e829c2916a574aed43d", "enumValue": "0", "description": "\u8868\u64cd\u4f5c_\u68c0\u67e5\u8868\u7684\u81a8\u80c0\u7387\u662f\u5426\u8fc7\u5927(\u662f)", "outputConvertText": "return_code=0:\u4ecd\u5b58\u5728\u8868\u81a8\u80c0\u60c5\u51b5"}]}, {"param_name": "table_list", "param_desc": "table_list", "param_value": null, "paramEnumList": null}], "enum_key": "return_code", "enum_value": {"\u8868\u64cd\u4f5c_\u68c0\u67e5\u8868\u7684\u81a8\u80c0\u7387\u662f\u5426\u8fc7\u5927\uff08\u5426\uff09": "1", "\u8868\u64cd\u4f5c_\u68c0\u67e5\u8868\u7684\u81a8\u80c0\u7387\u662f\u5426\u8fc7\u5927(\u662f)": "0"}, "need_interrupt": false}}, "enum_desc": "", "enum_value": ""}]',
#             "mermaid_txt": txt
#         }
        # print(f"subsaas_values: {subsaas_values}")
        print(f"entering subgraph...")
        if resume:
            while runs:
                print(f"graph resume...resume: {resume_params}")
                async for mode, data in client.runs.stream(
                thread_id=thread_id,
                assistant_id=ASSISTANT_ID,
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
                        # print(f"data: {data}")
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
                state = await client.threads.get_state(thread_id=thread_id)
                # next = state.get("next")
                values = state.get("values")
                checkpointer = state.get("checkpoint")
                interrupts = state.get("interrupts")
                print(f"next: {next}, values: {values}")
                # logger.info(f"checkpointer: {checkpointer}")
                # logger.info(f"interrupts: {interrupts}")

    asyncio.run(main())