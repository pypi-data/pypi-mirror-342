import asyncio

from mm_std import Result, http_request


async def send_message(bot_token: str, chat_id: int, message: str, long_message_delay: int = 3) -> Result[list[int]]:
    messages = _split_string(message, 4096)
    responses = []
    result = []
    while True:
        text = messages.pop(0)
        params = {"chat_id": chat_id, "text": text}
        res = await http_request(f"https://api.telegram.org/bot{bot_token}/sendMessage", method="post", json=params)
        responses.append(res.to_dict())
        if res.is_err():
            return Result.err(res.error or "error", extra={"responses": [responses]})

        message_id = res.parse_json_body("result.message_id", none_on_error=True)
        if message_id:
            result.append(message_id)
        else:
            return Result.err("unknown_response", extra={"responses": responses})

        if len(messages):
            await asyncio.sleep(long_message_delay)
        else:
            break
    return Result.ok(result, extra={"responses": responses})


def _split_string(text: str, chars_per_string: int) -> list[str]:
    return [text[i : i + chars_per_string] for i in range(0, len(text), chars_per_string)]
