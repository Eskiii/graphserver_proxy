"""
异步方式测试 LangGraph SDK 的 client.assistants.search() 方法
"""
import asyncio
from langgraph_sdk import get_client
from utils import load_env_config
from utils import load_env_config, create_headers

async def test_assistants_search_async(app_id="", api_key="", api_host="", api_url=""):
    """
    使用异步客户端测试 assistants.search() 方法
    """
    # 加载环境配置
    config = load_env_config()
    
    # 获取配置参数
    api_url = config.get('LANGGRAPH_API_URL', 'http://127.0.0.1:2024')
    api_key = config.get('LANGGRAPH_API_KEY', 'your_api_key')
    app_id = config.get("APP_ID", "your_app_id")
    app_secret = config.get("APP_SECRET", "your_app_secret")
    app_host = config.get("APP_HOST", "you_app_host")

    # print(f"使用的API URL: {api_url}")
    # print(f"使用的API Key: {api_key}")
    # # 创建异步客户端
    # print(f"正在连接到: {api_url}")

    # 由于聚智平台使用了与langsmith不同的认证方式，这里不需要api_key
    # 而是需要传入聚智平台专门的header进行认证
    headers = create_headers(
        app_id=app_id, 
        app_secret=app_secret,
        host=app_host
        )
    client = get_client(url=api_url, api_key=api_key, headers=headers)
    # client = get_client(url=api_url, api_key=api_key)
    ASSISTANT_ID = config.get('LANGGRAPH_ASSISTANT_ID')
    try:

        # 调用 assistants.search() 方法 (异步)
        print("正在调用 await client.assistants.search()...")
        result = await client.assistants.search()
        
        # 输出结果
        print("搜索结果:")
        print(f"类型: {type(result)}")
        print(f"内容: {result}")
        ASSISTANT_ID = result[0].get('assistant_id') if result else config.get('LANGGRAPH_ASSISTANT_ID')
        print(f"调用成功，获取的第一个助手ID: {ASSISTANT_ID}")
    except Exception as e:
        print(f"调用失败: {e}")

    thread = await client.threads.create()
    thread_id = thread.get("thread_id")

    # try:
    #     # 创建thread.run()进行流式对话
    #     async for chunk in client.runs.stream(
    #         thread_id=thread_id,
    #         assistant_id=ASSISTANT_ID,
    #         input={"messages": [{"type": "human", "content":  [{
    #                     "type": "human",
    #                     "content": "11",
    #                     "id": "e9673158-5504-4373-bdd9-c593c3b79801"
    #                 }]}]},
    #         stream_mode=["messages", "debug"],
    #         metadata={"run_type": "test_run"}
    #     ):
    #         print(f"流式输出: {chunk}")
    # except Exception as e:
    #     print(f"调用失败: {e}")

async def main():
    """
    主函数 - 演示异步方式的使用
    """
    print("=== LangGraph SDK 异步客户端测试 ===")
    # # app_id = "74858E5E666E48448CD8"
    # api_key = "76041D6E891A42B88D5D0532CA84782D"
    # api_host = "172.16.251.149"
    # app_id = "d377f5c87b0a6f386d76d9ae4576d450"
    # # api_url = "http://172.16.251.149:9062/agentV2/multi-agents/graph/api/v1.0/graphApp/"+app_id
    # # api_url = "http://172.16.251.149:9062/openapi/v2/graph/api/v1.0/graphApp/"
    # api_url = "http://172.16.251.142:9060/agentV2/multi-agents/graph/api/v1.0/graphApp/d377f5c87b0a6f386d76d9ae4576d450"

    #生产测试
    # app_id = "74858E5E666E48448CD8"
    # api_key = "76041D6E891A42B88D5D0532CA84782D"
    # api_host = "172.16.251.149"
    # assistant_id = "b0cf76f050e144a938403e7a754e4268"
    # # app_id = ""
    # api_url = "http://172.16.251.149:9062/openapi/v2/graph/api/v2.0/graphApp/"+assistant_id
    # api_url = "http://10.255.77.9:9062/openapi/v2/graph/api/v2.0/graphApp/"+assistant_id
    # api_url = "http://172.16.251.142:9062/agentV2/multi-agents/graph/api/v1.0/graphApp/afb4/6ad576eb26093f1814dfec439eef"
    # api_url = "http://172.16.251.149:9062/agentV2/multi-agents/graph/api/v2.0/graphApp/"+assistant_id
    # api_url = "http://10.255.77.9:9060/agentV2/multi-agents/graph/api/v1.0/graphApp/1f356e21ab1625c5a5f5fbf613658936"
    # api_host = "172.16.251.149"
    # api_url = "http://172.16.251.142:9060/agentV2/multi-agents/graph/api/v1.0/graphApp/875e234b0b33b38c4099a7aeb62487e8"

    app_id = "9556C54317CE4B8F9468"
    # api_key = "44CBD47552824EC6BF3DF24CD82B2F0F"
    api_key = "9A5611568A8443DD856D241F6462B518"
    api_host = "172.16.251.149"
    assistant_id = "afb46ad576eb26093f1814dfec439eef"
    api_url = "http://172.16.251.149:9062/openapi/v2/graph/api/v2.0/graphApp/"+assistant_id
    await test_assistants_search_async(
        app_id=app_id, 
        api_key=api_key, 
        api_host=api_host, 
        api_url=api_url
    )

    # header = create_headers(app_id="C761D82552BD4C31AF49", app_secret="44CBD47552824EC6BF3DF24CD82B2F0F", host="10.255.77.9")

    # print(header)
    # curl "http://10.255.77.9:9060/agentV2/multi-agents/graph/api/v1.0/graphApp/assistants/0d57b63ebca1e121e8f35275b559b1c1"; \
    # -H "Content-Type: application/json" \
    # -H "X-JZ-AUTHORIZATION: hmac api_key=C761D82552BD4C31AF49, algorithm=hmac-sha256, headers=host date request-line, signature=A9MWIKM9DL9umZMoS808SL8/20P06sA5OL0qpUn+Vc0=" \
    # -H "X-JZ-DATE: Fri, 08 Aug 2025 09:49:44 GMT" \
    # -H "X-JZ-HOST: 10.255.77.9" \
    # -H "X-JZ-APPID: C761D82552BD4C31AF49"
    # curl https://langchain-ai.github.io/assistants/123e4567-e89b-12d3-a456-426614174000

    #磐维智能体graphserver测试
    # app_id = "C761D82552BD4C31AF49"
    # api_key = "44CBD47552824EC6BF3DF24CD82B2F0F"
    # api_host = "172.16.251.149"
    # assistant_id = "afb46ad576eb26093f1814dfec439eef"
    # api_url = "http://172.16.251.149:9062/openapi/v2/graph/api/v2.0/graphApp/"+assistant_id
    # await test_assistants_search_async(
    #     app_id=app_id, 
    #     api_key=api_key, 
    #     api_host=api_host, 
    #     api_url=api_url
    # )

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())


# curl "http://10.248.140.1:46024/agentV2/multi-agents/graph/api/v1.0/graphApp/assistants/0d57b63ebca1e121e8f35275b559b1c1" \
#     -H "Content-Type: application/json" \
#     -H "X-JZ-AUTHORIZATION: hmac api_key=C761D82552BD4C31AF49, algorithm=hmac-sha256, headers=host date request-line, signature=A9MWIKM9DL9umZMoS808SL8/20P06sA5OL0qpUn+Vc0=" \
#     -H "X-JZ-DATE: Fri, 08 Aug 2025 09:49:44 GMT" \
#     -H "X-JZ-HOST: 10.255.77.9" \
#     -H "X-JZ-APPID: C761D82552BD4C31AF49"

# curl -I http://10.248.140.1:46024