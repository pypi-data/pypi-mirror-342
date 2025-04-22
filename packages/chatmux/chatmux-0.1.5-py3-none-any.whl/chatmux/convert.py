import base64
import binascii
import io
from io import BytesIO
from typing import Any, Dict, List, Tuple

import requests
from PIL import Image, UnidentifiedImageError

# Define a standard User-Agent header
REQUESTS_HEADERS = {
    "User-Agent": "Nebulous-py/0.1 (https://github.com/agentsea/nebulous-py; contact@agentsea.ai)"
}


def oai_to_unsloth(
    messages_input: Dict[
        str, Any
    ],  # Assume input is always dict like {'messages': [...]}
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Converts messages from a JSON object containing a 'messages' key
    (typical in JSON Lines format) to the Nebulous conversation format.
    Images specified by URLs or base64 strings are loaded into PIL.Image objects.

    {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Who is this an image of?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://upload.wikimedia.org/wikipedia/commons/5/57/Abraham_Lincoln_1863_Portrait_%283x4_cropped%29.jpg"
                        }
                    }
                ]
            }
        ]
    }

    Output format example:
    {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the image."},
                    {"type": "image", "image": <PIL.Image.Image object>},
                ]
            },
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "This is an image of..."}]
            }
        ]
    }
    """
    # Directly extract the list of messages, assuming input structure
    messages_to_process = messages_input.get("messages", [])

    # Validate that 'messages' key contained a list
    if not isinstance(messages_to_process, list):
        print(
            f"Warning: Input dict provided, but 'messages' key does not contain a list: {type(messages_to_process)}. Returning empty."
        )
        return {"messages": []}

    nebu_conversation = []
    for message in messages_to_process:  # Use the extracted list
        # Add check here for robustness against malformed items *within* the list
        if not isinstance(message, dict):
            print(f"Warning: Skipping non-dictionary item in message list: {message!r}")
            continue

        role = message.get("role")
        input_content = message.get("content")  # Can be list or string
        image_url_top_level = message.get("image_url")  # Check for top-level image_url

        processed_content = []

        if isinstance(input_content, list):
            # Process list content (multi-modal)
            for item in input_content:
                item_type = item.get("type")
                if item_type in ("input_text", "text"):
                    processed_content.append(
                        {"type": "text", "text": item.get("text", "")}
                    )
                elif item_type in (
                    "input_image",
                    "image_url",
                    "image",
                ):  # Accept 'image' as source key too
                    # Use "image_url" first, then fallback to "image" if needed
                    image_source_value = item.get("image_url", item.get("image"))
                    image_url_to_load = None
                    pil_image_to_load = None

                    if item_type == "image_url" and isinstance(
                        image_source_value, dict
                    ):
                        # Handle nested {"url": "..."}
                        image_url_to_load = image_source_value.get("url")
                    elif isinstance(image_source_value, str):
                        # Handle direct URL string or base64 string
                        image_url_to_load = image_source_value  # Could be URL or base64
                    elif isinstance(image_source_value, Image.Image):
                        # Handle direct PIL image
                        pil_image_to_load = image_source_value

                    if pil_image_to_load:  # If we already have a PIL image
                        processed_content.append(
                            {"type": "image", "image": pil_image_to_load}
                        )
                    elif (
                        image_url_to_load
                    ):  # If we have a URL or base64 string to process
                        pil_image = None
                        try:
                            if image_url_to_load.startswith(("http://", "https://")):
                                # Handle URL
                                response = requests.get(
                                    image_url_to_load,
                                    stream=True,
                                    headers=REQUESTS_HEADERS,
                                )
                                response.raise_for_status()  # Raise an exception for bad status codes
                                pil_image = Image.open(response.raw)
                            else:  # Assume base64
                                # Handle base64 string
                                # Remove potential data URI prefix (e.g., "data:image/png;base64,")
                                if "," in image_url_to_load:
                                    image_url_to_load = image_url_to_load.split(",", 1)[
                                        1
                                    ]
                                image_bytes = base64.b64decode(image_url_to_load)
                                pil_image = Image.open(io.BytesIO(image_bytes))

                            if pil_image:
                                processed_content.append(
                                    {"type": "image", "image": pil_image}
                                )
                            else:
                                # This condition might be less likely now with the separated logic
                                print(
                                    f"Warning: Could not load image from source: {type(image_url_to_load)}"
                                )

                        except requests.exceptions.RequestException as e:
                            print(
                                f"Warning: Failed to fetch image from URL {image_url_to_load}: {e}"
                            )
                        except (binascii.Error, ValueError) as e:
                            print(f"Warning: Failed to decode base64 image string: {e}")
                        except (IOError, UnidentifiedImageError) as e:
                            print(f"Warning: Failed to open image: {e}")
                        except Exception as e:
                            print(
                                f"Warning: An unexpected error occurred while processing image: {e}"
                            )

                    else:
                        print(
                            "Warning: Image item provided but could not resolve image source (URL, base64, or PIL Image)."
                        )

                # Add handling for other potential input types if necessary
        elif isinstance(input_content, str):
            # Handle simple string content (common for assistant messages)
            processed_content.append({"type": "text", "text": input_content})
        # else: Handle unexpected content format (e.g., log warning, skip message)

        # Handle potential top-level image_url (after processing content)
        if image_url_top_level and isinstance(image_url_top_level, str):
            pil_image = None
            try:
                if image_url_top_level.startswith(("http://", "https://")):
                    # Handle URL
                    response = requests.get(
                        image_url_top_level, stream=True, headers=REQUESTS_HEADERS
                    )
                    response.raise_for_status()  # Raise an exception for bad status codes
                    pil_image = Image.open(response.raw)
                else:
                    # Assume base64 string if not URL (could refine this check)
                    # Remove potential data URI prefix
                    if "," in image_url_top_level:
                        image_url_top_level = image_url_top_level.split(",", 1)[1]
                    image_bytes = base64.b64decode(image_url_top_level)
                    pil_image = Image.open(io.BytesIO(image_bytes))

                if pil_image:
                    processed_content.append({"type": "image", "image": pil_image})
                else:
                    print(
                        f"Warning: Could not load image from top-level source: {type(image_url_top_level)}"
                    )

            except requests.exceptions.RequestException as e:
                print(
                    f"Warning: Failed to fetch top-level image from URL {image_url_top_level}: {e}"
                )
            except (binascii.Error, ValueError) as e:
                print(f"Warning: Failed to decode top-level base64 image string: {e}")
            except (IOError, UnidentifiedImageError) as e:
                print(f"Warning: Failed to open top-level image: {e}")
            except Exception as e:
                print(
                    f"Warning: An unexpected error occurred while processing top-level image: {e}"
                )

        if role and processed_content:
            nebu_conversation.append({"role": role, "content": processed_content})
        # else: Handle missing role or empty content if needed

    return {"messages": nebu_conversation}


def oai_to_qwen(
    messages_input: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Convert from an OpenAI message format to a format where image URLs
    are kept as strings.

    Input format example:
    [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "some text"},
                {"type": "image_url", "image_url": {"url": "https://..."}},
            ],
        }
    ]

    Output format example:
    [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "some text"},
                {"type": "image", "image": "https://..."},
            ],
        }
    ]
    """
    new_schema = []
    for message in messages_input:
        role = message.get("role")
        input_content = message.get("content")

        if not isinstance(role, str) or not isinstance(input_content, list):
            # Skip malformed messages
            print(f"Warning: Skipping malformed message: {message!r}")
            continue

        processed_content = []
        for item in input_content:
            item_type = item.get("type")
            if item_type == "text":
                text = item.get("text", "")
                processed_content.append({"type": "text", "text": text})
            elif item_type == "image_url":
                image_url_dict = item.get("image_url", {})
                url = image_url_dict.get("url")
                if url:
                    processed_content.append({"type": "image", "image": url})
                else:
                    print(f"Warning: image_url item missing 'url': {item!r}")
            # else: Handle or ignore other types if necessary

        if role and processed_content:
            new_schema.append({"role": role, "content": processed_content})
        # else: Handle cases with missing role or empty resulting content if needed

    return new_schema
