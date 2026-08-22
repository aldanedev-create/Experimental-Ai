from ai import ask_ai
from rag import index_documents


def main():

    print("Indexing Flaxon documentation...")
    index_documents()

    print()
    print("=" * 50)
    print("              MY AI")
    print("=" * 50)
    print("Flaxon knowledge: ENABLED")
    print("Type 'exit' to quit.")
    print()

    while True:

        try:
            message = input("You: ")

            if message.lower().strip() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not message.strip():
                continue

            answer = ask_ai(message)

            print()
            print("AI:", answer)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()