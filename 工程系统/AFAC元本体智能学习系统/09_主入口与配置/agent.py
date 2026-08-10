"""
LLM Client using DashScope API (compatible with OpenAI format)
"""
import os
import requests
from typing import Optional, List, Dict, Any


class LLMClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "qwen-plus",
        timeout: int = 60
    ):
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = model
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError("API key is required. Set LLM_API_KEY environment variable or pass api_key parameter.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self,
        system_prompt: str = "",
        user_message: str = "",
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Send a chat request to the LLM.
        
        Args:
            system_prompt: System prompt to set assistant behavior
            user_message: User's message content
            messages: List of message dicts with 'role' and 'content' keys (optional)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Assistant's response content
        """
        if messages is None:
            messages = []
        
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        if user_message:
            messages.append({"role": "user", "content": user_message})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        url = f"{self.base_url}/chat/completions"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            return f"Request error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    llm = LLMClient()
    result = llm.chat(
        system_prompt="You are a helpful assistant.",
        user_message="Hello, say OK"
    )
    print("Response:", result)
