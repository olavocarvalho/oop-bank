# Aula 4: Tratamento de Erros e Desenvolvimento de CLI

## Revisão da Aula 3

* Revisão da classe `Conta` e seus métodos.
* Revisão da classe `Banco` e suas operações.

## Tratamento de Erros

* **`try...except`:** Capturando e lidando com erros para evitar que o programa termine abruptamente. _Exemplos: tratamento de `ValueError` para entradas inválidas._
* **`raise`:** Levantando exceções para indicar erros específicos. _Exemplos: levantando `ValueError` para valores de depósito ou saque inválidos._  

## Desenvolvimento da CLI (Command-Line Interface)

* **Função `main`:** O ponto de entrada do programa. Gerencia o loop principal e a interação com o usuário.
* **Validação de Entrada:** Garantir que as entradas do usuário sejam válidas antes de processá-las. _Exemplos: `solicitar_cpf` e `solicitar_valor`._
* **Conectando a CLI ao Banco:** Chamando os métodos do objeto `Banco` com base nas ações do usuário.

## Exercício de Codificação

1. Adicione um novo recurso à CLI, como fechar uma conta.
2. Implemente o tratamento de erros para o novo recurso.
3. **Desafio:** Implemente a funcionalidade de exibir o histórico de transações de um cliente específico, considerando todas as suas contas.