# chatmux

Convert to and from common LLM chat schemas.

All implementations are built on pydantic base models to be network ready.

## Installation

```bash
pip install chatmux
```

## Usage

Fully OpenAI compatible pydantic models
```python
from chatmux.openai import UserMessage, TextContentPart, ImageContentPart, ImageUrl

# Example using Pydantic models (more robust):
user_message = UserMessage(
    role="user",
    content=[
        TextContentPart(type="text", text="Describe this image:"),
        ImageContentPart(
            type="image_url",
            image_url=ImageUrl(url="https://example.com/image.jpg")
        )
    ]
)
openai_messages = [user_message.model_dump(exclude_none=True)] # Convert model to dict
```

Conversion methods to and from other schemas
```python
from chatmux.convert import oai_to_qwen

qwen_messages = oai_to_qwen(openai_messages)
print(qwen_messages)
# Expected Output (structure based on oai_to_qwen):
# [
#     {
#         'role': 'user',
#         'content': [
#             {'type': 'text', 'text': 'Describe this image:'},
#             {'type': 'image', 'image': 'https://example.com/image.jpg'}
#         ]
#     }
# ]
```

### Supported Conversions (as implemented in `src/chatmux/convert.py`):

*   **OpenAI-like -> Unsloth Inference**: Converts multimodal messages, downloads images, and formats for Unsloth. Returns new schema and PIL Images. (`convert_to_unsloth_inference`)
*   **OpenAI-like -> Unsloth**: Converts messages (potentially from JSONL), handling image URLs/base64, embedding PIL Images. (`oai_to_unsloth`)
*   **OpenAI-like -> Qwen**: Converts multimodal messages, keeping image URLs as strings but adjusting the content structure. (`oai_to_qwen`)

## Contributing

Please open an issue before submitting a PR.

## License

MIT
