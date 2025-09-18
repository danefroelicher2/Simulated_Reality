from typing import Dict, List, Optional, Any
import ollama
from datetime import datetime
import json


class OllamaClient:
    def __init__(self, model: str = "gemma3:4b", host: str = "http://localhost:11434"):
        """
        Initialize Ollama client for character conversations.

        Args:
            model: The Ollama model to use (default: gemma3:4b)
            host: Ollama server host (default: localhost:11434)
        """
        self.model = model
        self.host = host
        self.client = ollama.Client(host=host)
        self.conversation_history = {}

    def check_connection(self) -> bool:
        """Check if Ollama server is accessible and model is available."""
        try:
            models = self.client.list()
            # Handle different possible model response formats
            if 'models' in models:
                available_models = []
                for model in models['models']:
                    if isinstance(model, dict):
                        if 'name' in model:
                            available_models.append(model['name'])
                        elif 'model' in model:
                            available_models.append(model['model'])
                    else:
                        # Handle model objects with 'model' attribute
                        model_str = str(model)
                        if "model='" in model_str:
                            # Extract model name from the string representation
                            start = model_str.find("model='") + 7
                            end = model_str.find("'", start)
                            if end > start:
                                available_models.append(model_str[start:end])
                        else:
                            available_models.append(model_str)
            else:
                available_models = []

            if self.model not in available_models:
                print(f"Warning: Model '{self.model}' not found. Available models: {available_models}")
                if available_models:
                    self.model = available_models[0]
                    print(f"Switching to available model: {self.model}")
                else:
                    return False
            return True
        except Exception as e:
            print(f"Failed to connect to Ollama: {e}")
            return False

    def generate_response(
        self,
        prompt: str,
        character_id: str = "default",
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """
        Generate a response using Ollama.

        Args:
            prompt: The user's input/question
            character_id: Unique identifier for the character
            system_prompt: System prompt defining character personality
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length

        Returns:
            Dict containing response and metadata
        """
        try:
            messages = []

            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # Add conversation history for this character
            if character_id in self.conversation_history:
                messages.extend(self.conversation_history[character_id])

            # Add current user message
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Generate response
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            )

            response_text = response['message']['content'].strip()

            # Store conversation history
            if character_id not in self.conversation_history:
                self.conversation_history[character_id] = []

            self.conversation_history[character_id].extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response_text}
            ])

            # Keep only last 10 messages to prevent context overflow
            if len(self.conversation_history[character_id]) > 20:
                self.conversation_history[character_id] = self.conversation_history[character_id][-20:]

            return {
                "response": response_text,
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "character_id": character_id,
                "model": self.model,
                "tokens_used": response.get('eval_count', 0),
                "metadata": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "prompt_length": len(prompt)
                }
            }

        except Exception as e:
            return {
                "response": f"I'm having trouble thinking right now. Error: {str(e)}",
                "success": False,
                "timestamp": datetime.now().isoformat(),
                "character_id": character_id,
                "error": str(e)
            }

    def clear_conversation_history(self, character_id: str = None):
        """Clear conversation history for a specific character or all characters."""
        if character_id:
            if character_id in self.conversation_history:
                del self.conversation_history[character_id]
        else:
            self.conversation_history.clear()

    def get_conversation_summary(self, character_id: str) -> Dict[str, Any]:
        """Get summary of conversation history for a character."""
        if character_id not in self.conversation_history:
            return {"message_count": 0, "history": []}

        history = self.conversation_history[character_id]
        return {
            "character_id": character_id,
            "message_count": len(history),
            "last_interaction": history[-1]["content"] if history else None,
            "conversation_length": sum(len(msg["content"]) for msg in history)
        }

    def list_available_models(self) -> List[str]:
        """List all available Ollama models."""
        try:
            models = self.client.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def switch_model(self, model_name: str) -> bool:
        """Switch to a different Ollama model."""
        available_models = self.list_available_models()
        if model_name in available_models:
            self.model = model_name
            print(f"Switched to model: {model_name}")
            return True
        else:
            print(f"Model '{model_name}' not available. Available models: {available_models}")
            return False