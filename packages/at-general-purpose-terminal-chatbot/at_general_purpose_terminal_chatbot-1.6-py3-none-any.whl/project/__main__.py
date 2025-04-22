import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from rich import print

# Load environment variables
load_dotenv(dotenv_path=".env")

print("Chave:", os.getenv("OPENAI_API_KEY"))

# Start the large language model
chat = ChatOpenAI(
    temperature=0.7,  # Controle de criatividade (0 = mais objetivo, 1 = mais criativo)
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"
)

# Chatbot scope
def main():
    print("[bold #FF8700]Chatbot:[/bold #FF8700] Olá! Eu sou seu assistente. Pergunte-me qualquer coisa. Digite 'sair' para encerrar.\n")

    # Creates variable to store message history
    messages = [SystemMessage(content="Você é um assistente útil e amigável.")]

    while True:
        print("[bold blue]Você:[/bold blue] ", end=" ")
        user_input = input().strip()

        if user_input.lower() in ["sair", "exit", "quit"]:
            print("[bold #FF8700]Chatbot:[/bold #FF8700] Até logo!")
            break

        # Adds the user's message to the message history
        messages.append(HumanMessage(content=user_input))

        # Generates the chatbot response
        try:
            response = chat.invoke(messages)
            chatbot_reply = response.content
            print(f"[bold #FF8700]Chatbot:[/bold #FF8700] {chatbot_reply}")

            # Adds AI response to message history
            messages.append(AIMessage(content=chatbot_reply))
        except Exception as e:
            print(f"[bold red]Erro:[/bold red] {e}")

if __name__ == "__main__":
    main()