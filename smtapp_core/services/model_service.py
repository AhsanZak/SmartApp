"""
Model service for managing AI models
"""
from typing import List, Dict, Optional
import httpx
import ollama

from config.settings import get_settings, get_toml_config


class ModelService:
    """Service for managing AI models"""
    
    def __init__(self):
        self.settings = get_settings()
        self.ollama_config = get_toml_config("ollama")
    
    async def list_available_models(self) -> List[Dict]:
        """
        List all available models from configured providers
        """
        models = []
        
        # Get Ollama models
        try:
            ollama_models = await self.get_ollama_models()
            for model in ollama_models:
                models.append({
                    "name": model["name"],
                    "provider": "ollama",
                    "context_length": model.get("context_length", 4096),
                    "available": True
                })
        except Exception as e:
            print(f"Error fetching Ollama models: {e}")
        
        # Add configured models from TOML
        if self.ollama_config and "models" in self.ollama_config:
            for model_name, model_info in self.ollama_config["models"].items():
                if not any(m["name"] == model_info["name"] for m in models):
                    models.append({
                        "name": model_info["name"],
                        "provider": "ollama",
                        "context_length": model_info.get("context_length", 4096),
                        "available": False
                    })
        
        return models
    
    async def get_ollama_models(self) -> List[Dict]:
        """
        Get list of Ollama models
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.settings.ollama_base_url}/api/tags",
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                return [
                    {
                        "name": model["name"],
                        "size": model.get("size", 0),
                        "context_length": 4096  # Default, could be in model details
                    }
                    for model in data.get("models", [])
                ]
        except Exception as e:
            raise Exception(f"Failed to fetch Ollama models: {str(e)}")
    
    async def pull_ollama_model(self, model_name: str) -> Dict:
        """
        Pull an Ollama model
        """
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self.settings.ollama_base_url}/api/pull",
                    json={"name": model_name}
                )
                response.raise_for_status()
                return {"status": "success", "model": model_name}
        except Exception as e:
            raise Exception(f"Failed to pull model: {str(e)}")
    
    async def generate_response(
        self,
        messages: List[Dict],
        model_name: str,
        model_provider: str = "ollama",
        context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate a response from the AI model
        """
        if model_provider == "ollama":
            return await self._generate_ollama_response(
                messages=messages,
                model_name=model_name,
                context=context,
                temperature=temperature
            )
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")
    
    async def _generate_ollama_response(
        self,
        messages: List[Dict],
        model_name: str,
        context: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate response using Ollama
        """
        try:
            # Add context to the system message if provided
            if context:
                system_message = {
                    "role": "system",
                    "content": f"Use the following context to answer questions:\n{context}"
                }
                messages = [system_message] + messages
            
            # Use ollama library
            client = ollama.Client(host=self.settings.ollama_base_url)
            
            response = client.chat(
                model=model_name,
                messages=messages
            )
            
            return response["message"]["content"]
            
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

