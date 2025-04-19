from baml_agents._utils._python import sole


def view_prompt(request):
    messages = request.body.json()["messages"]
    prompt_parts = []
    for message in messages:
        content = sole(message["content"])
        if content["type"] != "text":
            raise ValueError(
                f"Expected content type 'text', but got '{content['type']}'"
            )
        prompt_parts.append(f"[{message['role']}]\n{content['text']}")
    return "\n\n".join(prompt_parts)
