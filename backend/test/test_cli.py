from backend.rag.chat_engine import build_agent


def run_cli():
    print("MedAssist (CLI Demo)")
    print('Type "exit" to quit.\n')

    username = "guess_user"
    user_info = "NA"

    try:
        agent = build_agent(username=username, user_info=user_info)
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return

    print("\n✅ Agent ready. Start chatting.\n")
    while True:
        message = input("You: ").strip()
        if message.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        try:
            response = agent.chat(message)
            print(f"MedAssist: {response}\n")
        except Exception as e:
            print(f"❌ Error during chat: {e}\n")


if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nExiting...")
