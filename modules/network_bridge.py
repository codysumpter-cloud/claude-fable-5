import os
import http.client
import json

class SecureNetworkBridge:
    def __init__(self, api_key: str = None):
        """
        Initializes the secure network bridge directly to the API endpoint.
        Uses environment variables if the key is not explicitly provided.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.host = "api.anthropic.com"
        self.endpoint = "/v1/messages"
        
        if not self.api_key:
            raise ValueError("API Key is missing. Ensure ANTHROPIC_API_KEY is set.")

    def send_request(self, system_prompt: str, user_prompt: str, model: str = "claude-3-opus-20240229") -> str:
        """
        Sends a direct HTTPS POST request to the API, bypassing web browsers 
        and eliminating intermediary data logging or telemetry.
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": model,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
        
        conn = http.client.HTTPSConnection(self.host)
        try:
            conn.request("POST", self.endpoint, body=json.dumps(payload), headers=headers)
            response = conn.getresponse()
            response_data = response.read().decode("utf-8")
            
            if response.status == 200:
                result_json = json.loads(response_data)
                return result_json["content"][0]["text"]
            else:
                return f"Error {response.status}: {response_data}"
        except Exception as e:
            return f"Network Error: {str(e)}"
        finally:
            conn.close()
