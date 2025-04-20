import os
import anthropic
from openai import OpenAI
from groq import Groq
from google import genai
from google.genai import types
import requests
import json
from typing import Generator, List, Dict
import traceback
import sys
import configparser
import time
from typing import Generator, List, Dict
from litellm import completion, completion_cost, token_counter

# Suppress Google API and gRPC logging
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['GRPC_PYTHON_LOG_LEVEL'] = 'ERROR'
os.environ['GRPC_TRACE'] = 'none'
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class LLMConnector:
    def __init__(self, config, model=None, system_prompt=None, stream_mode=True, web_search=False):
        self.config = config
        self.model = model or config.get('DEFAULT', 'default_model', fallback='')
        self.system_prompt = system_prompt or 'You are a helpful assistant with a cheerful disposition.'
        self.input_tokens = 0
        self.output_tokens = 0
        self.stream_mode = stream_mode
        self.web_search = web_search

        # Skip API key setup for test model
        if not self.model.startswith('test:'):
            self.setup_api_keys()

            # Initialize clients only if we have API keys
            openai_key = self.config.get('DEFAULT', 'openai_api_key', fallback='')
            self.openai_client = OpenAI(api_key=openai_key) if openai_key else None

            anthropic_key = self.config.get('DEFAULT', 'anthropic_api_key', fallback='')
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None

            groq_key = self.config.get('DEFAULT', 'groq_api_key', fallback='')
            self.groq_client = Groq(api_key=groq_key) if groq_key else None

            google_key = self.config.get('DEFAULT', 'google_api_key', fallback='')
            if google_key:
                client = genai.Client(api_key=google_key)
                self.google_client = client
            else:
                self.google_client = None

    def setup_api_keys(self):
        for key in ['openai_api_key', 'anthropic_api_key', 'groq_api_key', 'google_api_key']:
            if key not in self.config['DEFAULT'] or not self.config['DEFAULT'][key]:
                self.config['DEFAULT'][key] = os.environ.get(key.upper(), '')
            # Set environment variables for LiteLLM
            env_var_name = key.upper()
            api_key_value = self.config['DEFAULT'][key]
            os.environ[env_var_name] = api_key_value
            # Also set GEMINI_API_KEY if GOOGLE_API_KEY is set, as LiteLLM might prefer it
            if env_var_name == 'GOOGLE_API_KEY' and api_key_value:
                os.environ['GEMINI_API_KEY'] = api_key_value

    def get_available_models(self, provider) -> List[str]:
        if provider == "openai":
            return self.get_openai_models()
        elif provider == "anthropic":
            return self.get_anthropic_models()
        elif provider == "ollama":
            return self.get_ollama_models()
        elif provider == "groq":
            return self.get_groq_models()
        elif provider == "gemini":
            return self.get_google_models()
        else:
            return [f"Unsupported provider: {provider}"]

    def get_openai_models(self) -> List[str]:
        if not self.config.get('DEFAULT', 'openai_api_key'):
            return ["No API key set"]
        if not self.openai_client:
            return ["Error: OpenAI client not initialized"]
        try:
            openai_models = self.openai_client.models.list()
            return [model.id for model in openai_models.data if model.id.startswith("gpt")]
        except Exception as e:
            print(f"Error fetching OpenAI models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def get_anthropic_models(self) -> List[str]:
        """Get available Anthropic models"""
        if not self.config.get('DEFAULT', 'anthropic_api_key'):
            return ["No API key set"]
        try:
            models = self.anthropic_client.models.list()
            sorted_models = sorted([model.id for model in models.data])
            return sorted_models
        except Exception as e:
            print(f"Error fetching Anthropic models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def get_ollama_models(self) -> List[str]:
        # Read the base URL from config, falling back to the default
        ollama_base_url = self.config.get('DEFAULT', 'ollama_base_url', fallback='http://localhost:11434')
        ollama_tags_url = f"{ollama_base_url}/api/tags"
        try:
            # Add a timeout (e.g., 5 seconds) to prevent hanging
            response = requests.get(ollama_tags_url, timeout=5)
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            ollama_models = response.json().get('models', [])
            return [model['name'] for model in ollama_models]

        except requests.exceptions.ConnectionError:
            # Specifically handle connection errors (server down, wrong address/port)
            print(f"Error: Could not connect to Ollama server at {ollama_base_url}. Please ensure it is running.", file=sys.stderr)
            return ["Ollama server not reachable"] # Return a more specific status
        except requests.exceptions.Timeout:
            # Handle timeouts
            print(f"Error: Connection to Ollama server at {ollama_base_url} timed out.", file=sys.stderr)
            return ["Ollama connection timed out"]
        except requests.exceptions.RequestException as e:
            # Handle other request errors (like HTTP errors from raise_for_status)
            print(f"Error fetching Ollama models: {str(e)}", file=sys.stderr)
            return ["Error fetching models"]
        except Exception as e:
            # Catch any other unexpected errors (e.g., JSON decoding)
            print(f"Unexpected error fetching Ollama models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Unexpected error fetching models"]

    def get_groq_models(self) -> List[str]:
        if not self.config.get('DEFAULT', 'groq_api_key'):
            return ["No API key set"]
        try:
            groq_models = self.groq_client.models.list()
            return [model.id for model in groq_models.data]
        except Exception as e:
            print(f"Error fetching Groq models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def get_google_models(self) -> List[str]:
        if not self.config.get('DEFAULT', 'google_api_key'):
            return ["No API key set"]
        try:
            models = self.google_client.models.list()
            google_models = []
            for m in models:
                if 'generateContent' in m.supported_actions:
                    # Strip the 'models/' prefix from the model name
                    name = m.name.replace('models/', '')
                    google_models.append(name)
            return google_models
        except Exception as e:
            print(f"Error fetching Google models: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return ["Error fetching models"]

    def send_prompt(self, prompt: str, debug: bool = False) -> Generator[str, None, None]:
        if debug:
            print(f"\n[DEBUG] Sending prompt with model: {self.model}", file=sys.stderr)

        try:
            if self.model.startswith('test:'):
                yield from self.send_prompt_test(prompt, debug)
                return

            # Add current date and time to system prompt if web search is enabled
            system_content = self.system_prompt
            if self.web_search:
                from datetime import datetime
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                system_content = f"{self.system_prompt}\n\nCurrent date and time: {current_datetime}\n\nWhen using web search, you MUST include citations for your information sources. After your response, list all sources with their URLs and webpage titles in a completely new section titled 'Sources:'."
                if debug:
                    print(f"\n[DEBUG] Added current datetime to system prompt: {current_datetime}", file=sys.stderr)

            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]

            # Determine provider and get the correct API key
            provider = self.model.split('/')[0] if '/' in self.model else None
            api_key = None
            if provider == 'gemini':
                api_key = self.config.get('DEFAULT', 'google_api_key', fallback=None)
            elif provider == 'openai':
                api_key = self.config.get('DEFAULT', 'openai_api_key', fallback=None)
            elif provider == 'anthropic':
                api_key = self.config.get('DEFAULT', 'anthropic_api_key', fallback=None)
            elif provider == 'groq':
                api_key = self.config.get('DEFAULT', 'groq_api_key', fallback=None)
            # Add other providers as needed

            # Model name is already in the correct format
            model_to_use = self.model

            completion_args = {
                "model": model_to_use,
                "messages": messages,
                "stream": self.stream_mode
            }
            if api_key:
                completion_args["api_key"] = api_key

            # Add web search capability if requested and supported
            if self.web_search and provider == 'gemini':
                completion_args["tools"] = [{"googleSearch": {}}]
                if debug:
                    print(f"\n[DEBUG] Enabling web search for {model_to_use}", file=sys.stderr)


            # Reset token counts before processing response
            self.input_tokens = 0
            self.output_tokens = 0

            # Count input tokens using token_counter
            try:
                self.input_tokens = token_counter(model=model_to_use, messages=messages)
            except Exception as e:
                # If token counting fails, use a simple word count estimate
                self.input_tokens = len(prompt.split()) + len(self.system_prompt.split())

            response = completion(**completion_args)

            # Process response

            # Collect response content
            response_content = ""
            citations = []

            if self.stream_mode:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_content += content
                        yield content

                    # Check for citations in tool calls
                    if hasattr(chunk.choices[0].delta, 'tool_calls') and chunk.choices[0].delta.tool_calls:
                        for tool_call in chunk.choices[0].delta.tool_calls:
                            if hasattr(tool_call, 'function'):
                                if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                    try:
                                        import json
                                        search_results = json.loads(tool_call.function.arguments)
                                        if 'searchResults' in search_results:
                                            for result in search_results['searchResults']:
                                                citations.append(result)
                                        # Try alternative formats
                                        elif 'results' in search_results:
                                            for result in search_results['results']:
                                                citations.append(result)
                                    except Exception as e:
                                        pass
            else:
                response_content = response.choices[0].message.content
                yield response_content

                # Check for citations in tool calls for non-streaming response
                if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                    print(f"\n[#555555]Found tool_calls in response: {response.choices[0].message.tool_calls}[/#555555]", file=sys.stderr)
                    for tool_call in response.choices[0].message.tool_calls:
                        print(f"\n[#555555]Processing tool_call: {tool_call}[/#555555]", file=sys.stderr)
                        if hasattr(tool_call, 'function'):
                            print(f"\n[#555555]Function: {tool_call.function}[/#555555]", file=sys.stderr)
                            if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                try:
                                    import json
                                    print(f"\n[#555555]Function arguments: {tool_call.function.arguments}[/#555555]", file=sys.stderr)
                                    search_results = json.loads(tool_call.function.arguments)
                                    print(f"\n[#555555]Parsed search results: {search_results}[/#555555]", file=sys.stderr)
                                    if 'searchResults' in search_results:
                                        for result in search_results['searchResults']:
                                            citations.append(result)
                                    # Try alternative formats
                                    elif 'results' in search_results:
                                        for result in search_results['results']:
                                            citations.append(result)
                                except Exception as e:
                                    print(f"Error parsing search results: {str(e)}", file=sys.stderr)

            # Display citations if available and web search was used
            if self.web_search:
                # Print raw response for debugging
                if hasattr(response, 'choices') and response.choices:
                    choice = response.choices[0]

                    # Check for groundingMetadata in additional_kwargs
                    if hasattr(choice, 'message') and hasattr(choice.message, 'additional_kwargs'):
                        # Extract grounding metadata if available
                        grounding_metadata = additional_kwargs.get("groundingMetadata", {})

                        # Extract citations from grounding chunks
                        for chunk in grounding_metadata.get("groundingChunks", []):
                            web = chunk.get("web", {})
                            if web:
                                citations.append({
                                    "title": web.get("title", "Source"),
                                    "url": web.get("uri", ""),
                                    "snippet": web.get("snippet", "")
                                })

                    # Tool calls are already processed in the streaming and non-streaming sections

                    # Check for tool_response field
                    if hasattr(choice, 'message') and hasattr(choice.message, 'tool_response'):
                        try:
                            if isinstance(choice.message.tool_response, dict) and 'results' in choice.message.tool_response:
                                for result in choice.message.tool_response['results']:
                                    citations.append(result)
                        except Exception as e:
                            pass


            # Estimate output tokens by word count
            self.output_tokens = len(response_content.split())

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            yield f"Error: {str(e)}"

    def chat_completion(self, messages: List[Dict[str, str]], stream: bool = True) -> Generator[str, None, None]:
        try:
            if self.model.startswith('test:'):
                yield from self._chat_completion_test(messages, stream)
                return

            # Add current date and time to the first system message if web search is enabled
            if self.web_search and messages and messages[0]["role"] == "system":
                from datetime import datetime
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                messages[0]["content"] = f"{messages[0]['content']}\n\nCurrent date and time: {current_datetime}\n\nWhen using web search, you MUST include citations for your information sources. After your response, list all sources with their webpage titles and URLs inside a bulleted list in a completely new section titled 'Sources:'."

            # Determine provider and get the correct API key
            provider = self.model.split('/')[0] if '/' in self.model else None
            api_key = None
            if provider == 'gemini':
                api_key = self.config.get('DEFAULT', 'google_api_key', fallback=None)
            elif provider == 'openai':
                api_key = self.config.get('DEFAULT', 'openai_api_key', fallback=None)
            elif provider == 'anthropic':
                api_key = self.config.get('DEFAULT', 'anthropic_api_key', fallback=None)
            elif provider == 'groq':
                api_key = self.config.get('DEFAULT', 'groq_api_key', fallback=None)
            # Add other providers as needed

            # Model name is already in the correct format
            model_to_use = self.model

            completion_args = {
                "model": model_to_use,
                "messages": messages,
                "stream": stream
            }
            if api_key:
                completion_args["api_key"] = api_key

            # Add web search capability if requested and supported
            if self.web_search and provider == 'gemini':
                completion_args["tools"] = [{"googleSearch": {}}]



            # Reset token counts before processing response
            self.input_tokens = 0
            self.output_tokens = 0

            # Count input tokens using token_counter
            try:
                self.input_tokens = token_counter(model=model_to_use, messages=messages)
            except Exception as e:
                # If token counting fails, use a simple word count estimate
                total_words = 0
                for msg in messages:
                    if 'content' in msg and msg['content']:
                        total_words += len(msg['content'].split())
                self.input_tokens = total_words

            response = completion(**completion_args)

            # Process response



            # Collect response content
            response_content = ""
            citations = []

            if stream:
                for chunk in response:

                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_content += content
                        yield content

                    # Check for citations in tool calls
                    if hasattr(chunk.choices[0].delta, 'tool_calls') and chunk.choices[0].delta.tool_calls:
                        for tool_call in chunk.choices[0].delta.tool_calls:
                            if hasattr(tool_call, 'function'):
                                if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                    try:
                                        import json
                                        search_results = json.loads(tool_call.function.arguments)
                                        if 'searchResults' in search_results:
                                            for result in search_results['searchResults']:
                                                citations.append(result)
                                        # Try alternative formats
                                        elif 'results' in search_results:
                                            for result in search_results['results']:
                                                citations.append(result)
                                    except Exception as e:
                                        pass
            else:
                response_content = response.choices[0].message.content
                yield response_content

                # Check for citations in tool calls for non-streaming response
                if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                    for tool_call in response.choices[0].message.tool_calls:
                        if hasattr(tool_call, 'function'):
                            if hasattr(tool_call.function, 'name') and tool_call.function.name == 'googleSearch':
                                try:
                                    import json
                                    search_results = json.loads(tool_call.function.arguments)
                                    if 'searchResults' in search_results:
                                        for result in search_results['searchResults']:
                                            citations.append(result)
                                    # Try alternative formats
                                    elif 'results' in search_results:
                                        for result in search_results['results']:
                                            citations.append(result)
                                except Exception as e:
                                    pass

            # Display citations if available and web search was used
            if self.web_search:
                # Extract citations from response
                if hasattr(response, 'choices') and response.choices:
                    choice = response.choices[0]

                    # Check for groundingMetadata in additional_kwargs
                    if hasattr(choice, 'message') and hasattr(choice.message, 'additional_kwargs'):
                        additional_kwargs = choice.message.additional_kwargs

                        # Extract grounding metadata if available
                        grounding_metadata = additional_kwargs.get("groundingMetadata", {})

                        # Extract citations from grounding chunks
                        for chunk in grounding_metadata.get("groundingChunks", []):
                            web = chunk.get("web", {})
                            if web:
                                citations.append({
                                    "title": web.get("title", "Source"),
                                    "url": web.get("uri", ""),
                                    "snippet": web.get("snippet", "")
                                })

                    # Tool calls are already processed in the streaming and non-streaming sections

                    # Check for tool_response field
                    if hasattr(choice, 'message') and hasattr(choice.message, 'tool_response'):
                        try:
                            if isinstance(choice.message.tool_response, dict) and 'results' in choice.message.tool_response:
                                for result in choice.message.tool_response['results']:
                                    citations.append(result)
                        except Exception as e:
                            pass

            # Estimate output tokens by word count
            self.output_tokens = len(response_content.split())

        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            yield f"Error: {str(e)}"

    def send_prompt_test(self, prompt: str, debug: bool = False) -> Generator[str, None, None]:
        """Test model that returns predefined responses for testing."""
        try:
            test_response = "This is a test response from the test model.\n"
            test_response += "It can be used for testing without hitting real LLMs.\n"
            test_response += f"Your prompt was: {prompt}\n"
            test_response += f"System prompt was: {self.system_prompt}"

            # Set token counts for test model
            self.input_tokens = len(prompt.split()) + len(self.system_prompt.split())
            self.output_tokens = len(test_response.split())

            words = test_response.split()
            for word in words:
                yield word + " "
                if self.stream_mode:
                    time.sleep(0.01)

        except Exception as e:
            yield f"Error in test model: {str(e)}"

    def _chat_completion_test(self, messages: List[Dict[str, str]], stream: bool) -> Generator[str, None, None]:
        """Handle test model chat completion"""
        try:
            test_response = "This is a test chat response.\n"
            test_response += "Chat history:\n"

            # Calculate input tokens from messages
            input_token_count = 0
            for msg in messages:
                test_response += f"{msg['role'].upper()}: {msg['content']}\n"
                input_token_count += len(msg.get('content', '').split())

            # Set token counts for test model
            self.input_tokens = input_token_count
            self.output_tokens = len(test_response.split())

            if stream:
                words = test_response.split()
                for word in words:
                    yield word + " "
                    if self.stream_mode:
                        time.sleep(0.01)
            else:
                yield test_response

        except Exception as e:
            yield f"Error in test model: {str(e)}"

    def supports_web_search(self) -> bool:
        """Check if the current model supports web search"""
        # Currently only Gemini models support web search
        return self.model.startswith('gemini/')
