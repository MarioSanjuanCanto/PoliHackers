from openai import OpenAI

hf_token = "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"


def translate(input: str) -> str:
    client = OpenAI(
        base_url="https://y9qb4ck1bebf371m.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key=hf_token
    )
    chat_completion = client.chat.completions.create(
        model="gplsi/Aitana-TA-2B-S",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text from Spanish into Valencian.\nSpanish: {input} \nValencian:"
            }
        ],
        stream=True,
        temperature=0.5,
        max_tokens=400,
        frequency_penalty=1.2
    )
    traduccion = ""
    for message in chat_completion:
        delta = message.choices[0].delta.content
        if delta:
            traduccion += delta

    return traduccion.strip()

