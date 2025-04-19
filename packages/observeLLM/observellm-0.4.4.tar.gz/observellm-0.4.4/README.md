# ObserveLLM

A powerful observability library for AI/ML applications that provides comprehensive tracing and monitoring capabilities using Langfuse.

## Installation

Install the package from PyPI using:
```bash
pip install observeLLM
```

Note: It is recommended to use the latest version for optimal performance.

## Quick Start

### 1. Initialize Langfuse Client

First, initialize the Langfuse client at your application startup:

```python
from observe_traces import LangfuseInitializer

# Initialize Langfuse client
LangfuseInitializer.initialize(
    langfuse_public_key='your_langfuse_public_key',
    langfuse_secret_key='your_langfuse_secret_key',
    langfuse_host='your_host_url',  # e.g., 'http://localhost:3000'
    release='app_version',          # e.g., '1.0.0'
    environment='your_environment'  # e.g., 'development', 'production'
)

# Optional: Close Langfuse client when shutting down
LangfuseInitializer.close()
```

### 2. FastAPI Middleware Setup

Add the unified middleware to your FastAPI application in `main.py` or your entry point:

```python
from fastapi import FastAPI, Request
from observe_traces import unified_middleware

app = FastAPI()

@app.middleware("http")
async def set_request_context_middleware(request: Request, call_next):
    session_id = request.headers.get("X-Request-ID")
    body = await request.json()

    metadata = {
        "sessionId": session_id,
        "environment": "development",
        "serviceName": "observeLLM",
        "apiEndpoint": request.url.path,
        "user": request.headers.get("X-User-Email"),
        **body,
    }
    return await unified_middleware(request, call_next, metadata)
```

## Tracing Decorators

ObserveLLM provides four powerful decorators to enable comprehensive tracing for different AI/ML components:

### 1. LLM Tracing
```python
from observe_traces import llm_tracing

@llm_tracing(provider='openai')  # or any other LLM provider
async def llm_api_calling_function(
    model: str,                  # e.g., 'gpt-3.5-turbo'
    system_prompt: str,          # System instructions
    chat_messages: list,         # Conversation history
    **params                     # Additional parameters
):
    # Your LLM API calling logic here
    # Returns either:
    # 1. Tuple of (response_data, raw_response)
    # 2. Raw response object
```

Supported LLM Providers:
- OpenAI (GPT-3.5, GPT-4, GPT-4o, etc.)
- Anthropic (Claude models)
- Groq
- Custom providers can be added using `register_provider()`

### 2. LLM Streaming Tracing
```python
from observe_traces import llm_streaming_tracing
import json

@llm_streaming_tracing(provider='anthropic')  # Currently only supports Anthropic provider
async def llm_streaming_function(
    model: str,                  # e.g., 'claude-3-opus-20240229'
    system_prompt: str,          # System instructions
    chat_messages: list,         # Conversation history
    **params                     # Additional parameters
):
    # Your streaming LLM API calling logic here
    # Should be an async generator that yields specific formatted lines:
    
    # 1. For streaming response chunks:
    #    yield f"data: {json.dumps({'type': 'data', 'data': chunk_text})}"
    #    Example:
    #    yield 'data: {"type": "data", "data": "Hello"}'
    
    # 2. For token usage information:
    #    yield f"tokens: {json.dumps({'data': {'input': input_tokens, 'output': output_tokens}})}"
    #    Example:
    #    yield 'tokens: {"data": {"input": 10, "output": 5}}'
    
    # 3. Any other lines that should be passed through unchanged
    
    # The decorator will:
    # - Collect all response chunks to build the complete response
    # - Track token usage throughout the stream
    # - Calculate costs based on token usage
    # - Create a trace in Langfuse with the complete response and metrics
```

### 3. Embedding Tracing
```python
from observe_traces import embedding_tracing

@embedding_tracing(provider='openai')  # or any other embedding provider
async def embedding_generation_function(
    model_name: str,            # e.g., 'text-embedding-ada-002'
    inputs: list,               # List of texts to embed
    **kwargs                    # Additional parameters
):
    # Your embedding API calling logic here
    # Returns either:
    # 1. Tuple of (embeddings, raw_response)
    # 2. Raw response object
```

Supported Embedding Providers:
- OpenAI
- Cohere
- Jina
- VoyageAI
- Custom providers can be added using `register_embedding_provider()`

### 4. Vector Database Tracing
```python
from observe_traces import vectordb_tracing

# For write operations
@vectordb_tracing(provider='pinecone', operation_type='write')
async def vectordb_write_function(
    index_host: str,
    vectors: list,
    namespace: str
):
    # Your vector DB write logic here
    # Returns raw response object

# For read operations
@vectordb_tracing(provider='pinecone', operation_type='read')
async def vectordb_read_function(
    index_host: str,
    namespace: str,
    top_k: int,
    query: str,
    query_vector_embeds: list,
    query_sparse_embeds: dict = None,
    include_metadata: bool = True,
    filter_dict: dict = None
):
    # Your vector DB read logic here
    # Returns raw response object
```

Supported Vector DB Providers:
- Pinecone
- Custom providers can be added by extending the provider configurations

### 5. Reranking Tracing
```python
from observe_traces import reranking_tracing

@reranking_tracing(provider='cohere')  # or any other reranker provider
async def reranking_function(
    model_name: str,
    query: str,
    documents: list,
    top_n: int,
    **kwargs
):
    # Your reranking API calling logic here
    # Returns either:
    # 1. Tuple of (rerank_results, raw_response)
    # 2. Raw response object
```

Supported Reranking Providers:
- Cohere
- Pinecone
- Jina
- VoyageAI
- Custom providers can be added using `register_reranking_provider()`

## Features

- **Automatic Request Tracing**: Unique trace IDs for each request
- **Comprehensive Metadata**: Track user info, endpoints, and custom metadata
- **Cost Tracking**: Automatic calculation of token usage and costs
- **Performance Monitoring**: Response time measurements for all operations
- **Multi-Provider Support**: Works with various AI/ML providers
- **Flexible Integration**: Supports both tuple returns and single response objects
- **Context Management**: Maintains request state throughout the lifecycle
- **Token Cost Tracking**: Automatic calculation of costs based on provider-specific pricing
- **Streaming Support**: Comprehensive tracing for streaming LLM responses
- **Custom Provider Support**: Easy registration of new providers

## Prerequisites

1. **Self-Hosted Langfuse**: You must have a Langfuse instance running. Configure:
   - `langfuse_host`: Your Langfuse server URL
   - `langfuse_public_key`: Your public API key
   - `langfuse_secret_key`: Your secret API key

2. **FastAPI Application**: The middleware is designed for FastAPI applications

## Best Practices

1. **Error Handling**: The decorators automatically handle exceptions while maintaining trace context
2. **Metadata**: Include relevant metadata in your middleware for better observability
3. **Resource Cleanup**: Call `LangfuseInitializer.close()` when shutting down your application
4. **Context Variables**: The system uses context variables to maintain request state
5. **Provider Registration**: Use the appropriate registration functions to add custom providers
6. **Token Cost Tracking**: Ensure your provider configurations include accurate pricing information
7. **Streaming Support**: Follow the specified format for streaming responses to ensure proper tracing

## Note

The tracing system uses context variables to maintain request state throughout the request lifecycle. It's essential to define your methods using the specified parameters for consistency and compatibility. The decorators handle both tuple returns (response data + raw response) and single raw response returns, making them flexible for different API implementations.






