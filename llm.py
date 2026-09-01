import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List,Dict
load_dotenv()

class LLMAdaptor:
    def __init__(self,model:str = None,apiKey:str = None,baseUrl:str = None,timeout:int = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        api_key = apiKey or os.getenv("LLM_API_KEY")
        base_url = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, api_key, base_url, timeout]):
            raise ValueError("缺少模型参数")

        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    def think(
            self,
            messags:List[Dict[str,str]],
            temperature:float = 0
            ) -> str:
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.responses.create(
                model=self.model,
                input=messags,
                stream=True
            )

            collected_content = []

            for event in response:
                if event.type != "response.output_text.delta":
                    continue

                content = event.delta or ""
                print(content,end="",flush=True)
                collected_content.append(content)

            print()

            return "".join(collected_content)
        except Exception as error:
            print(f"❌ 调用LLM API时发生错误: {error}")
            
            return None
