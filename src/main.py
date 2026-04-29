from src.agents.task_agent import run_agent


def main():
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ['exit', 'quit', 'quit']:
                print("Goodbye!")
                break
            result = run_agent(user_input)
            print(result)
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
