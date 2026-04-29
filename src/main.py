#!/usr/bin/env python
"""Ponto de entrada do TaskAgent"""

from src.agents.task_agent import run_agent


def main():
    """Função principal do agente"""
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ['exit', 'quit', 'sair']:
                print("Até logo!")
                break
            result = run_agent(user_input)
            print(result)
        except KeyboardInterrupt:
            print("\n\nAté logo!")
            break
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")


if __name__ == "__main__":
    main()
