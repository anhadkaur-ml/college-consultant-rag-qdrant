"""Interactive College Consultant chatbot backed by Qdrant."""

from services import get_ai_output


EXIT_COMMANDS = {"exit", "quit"}


def run_chatbot() -> None:
    conversation_history: list[dict] = []
    print("=" * 50)
    print("🎓✨ ASTRA — QDRANT COLLEGE CONSULTANT ✨🎓")
    print("=" * 50)
    print("💬 Ask about colleges, courses, fees, or eligibility.")
    print('🚪 Type "exit" to close.')

    while True:
        # Keep the editable input prompt ASCII-only. Combined emoji can make
        # the Windows CMD cursor overwrite or hide characters while typing.
        user_message = input("\nYou: ").strip()
        if user_message.lower() in EXIT_COMMANDS:
            print("👋 Astra: Thank you for using College Consultant!")
            break
        if not user_message:
            print("⚠️ Astra: Please enter a question.")
            continue

        try:
            result = get_ai_output(user_message, conversation_history)
            print(f"\n🤖 Astra: {result.answer}")
            if result.sources:
                print("📚 Sources: " + "; ".join(result.sources))
            conversation_history.extend(
                [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": result.answer},
                ]
            )
        except Exception as error:
            print(f"❌ Astra: I could not complete the request: {error}")


if __name__ == "__main__":
    run_chatbot()
