from dotenv import load_dotenv
import os

load_dotenv()

# Lazily initialised so importing this module never crashes the server
_client = None


def _get_client():
    global _client
    if _client is None:
        from groq import Groq
        _client = Groq()
    return _client


def classify_with_llm(log_message):
    client = _get_client()

    prompt = f"""Classify the log message into one of these categories:
       (1) Workflow Error, (2) Deprecation Warning.
       If you can't figure out a category, use "Unknown".
       Only return the Category name. No preamble
       Log message: {log_message}"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
    )

    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            full_response += content

    return full_response.strip()


if __name__ == "__main__":
    print(classify_with_llm(
        "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
    print(classify_with_llm(
        "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
    print(classify_with_llm("System reboot initiated by user 12345."))
