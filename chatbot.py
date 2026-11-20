import os 
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY"),
)
MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer questions clearly and concisely. "
    "If you are not sure about something, say so."
)

history = [{"role": "system", "content": SYSTEM_PROMPT}]


def ask(question):
    """Send the question plus conversation history to Groq and return the answer."""
    history.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=history,
    )
    answer = response.choices[0].message.content

    history.append({"role": "assistant", "content": answer})
    return answer


def main():
    print("Q&A Chatbot (Groq). Type your question, or 'quit' to exit.\n")
    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        try:
            print("Bot:", ask(question), "\n")
        except Exception as e:
            # Remove the unanswered question so history stays valid
            history.pop()
            print(f"Error from API: {e}\n")


if __name__ == "__main__":
    main()