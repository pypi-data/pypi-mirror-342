# PAI-LLM

## Conversation

### 1. Conversation

* History Conversation
    - save
    - query
    - rename
    - delete
    - search

### 2. Chat

* Single-round Chat
* Multi-round Chat

## Chat

### OpenAI Chat format

* 简单文本（字符串）

```json
{
  "role": "user",
  "content": "Hello"
}
```

* 多模态内容（数组）

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "这张图片是什么？"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/image.jpg"
      }
    }
  ]
}
```

* 特殊字段

assistant角色

```json
{
  "role": "assistant",
  "content": "我需要查询天气预报",
  "tool_calls": [
    {
      "id": "call_id",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\":\"北京\",\"unit\":\"celsius\"}"
      }
    }
  ]
}
```

tool角色

```json
{
  "role": "tool",
  "tool_call_id": "call_id",
  "content": "{\"location\":\"北京\",\"unit\":\"celsius\",\"temperature\":25}"
}
```
