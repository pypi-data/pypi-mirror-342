import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from rich import print
print(os.path.dirname(__file__))
# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
print(dotenv_path)
print(os.getenv("OPENAI_API_KEY"))

# Start the large language model
chat = ChatOpenAI(
    temperature=0.7,  # Creativity control (0 = more objective, 1 = more creative)
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"
)

# Chatbot scope
def main():
    args = sys.argv[1:] # Ignore the project command cbcli
    user_input = ""

    if len(args) == 0:
        print("[bold #FF8700]Chatbot:[/bold #FF8700] Olá! Eu sou seu assistente. Pergunte-me qualquer coisa. Digite 'sair' para encerrar.\n")
    else:
        user_input = " ".join(args)

    # Creates variable to store message history
    messages = [SystemMessage(content="Você é um assistente útil e amigável.")]

    try:

        while True:

            if len(user_input) == 0:
                print("[bold blue]Você:[/bold blue]", end=" ")
                user_input = input().strip()

                if user_input.lower() in ["sair", "exit", "quit"]:
                    print("[bold #FF8700]Chatbot:[/bold #FF8700] Até logo!")
                    break

            # Adds the user's message to the message history
            messages.append(HumanMessage(content=user_input))

            user_input = ""

            # Generates the chatbot response
            try:
                response = chat.invoke(messages)
                chatbot_reply = response.content
                print(f"[bold #FF8700]Chatbot:[/bold #FF8700] {chatbot_reply}")

                # Adds AI response to message history
                messages.append(AIMessage(content=chatbot_reply))
            except Exception as e:
                print(f"[bold red]Erro:[/bold red] {e}")

    except KeyboardInterrupt:
        print(f"\n[bold #00FFFF][!] Finalizado com Ctrl+C.[/bold #00FFFF]")
        sys.exit(0)

if __name__ == "__main__":
    main()