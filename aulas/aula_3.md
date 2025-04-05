# Aula 3: Trabalhando com as Classes `Conta` e `Banco`

## Revisão da Aula 2

* Revisão de herança e `super()`.
* Revisão de polimorfismo e classes abstratas.

## A Classe `Conta`

* **Gerenciando o Saldo (`_saldo`):** Como depósitos e saques afetam o saldo. Importância da encapsulação para proteger o saldo de modificações diretas.
* **Histórico de Transações (`_historico_transacoes`):** Armazenando e acessando o histórico de transações.
* **`exibir_extrato()`:** Gerando um extrato da conta com todas as transações e saldo atual.

## A Classe `Banco`

* **Gerenciando Clientes (`_clientes`):** Adicionando, buscando e gerenciando clientes.
* **Gerenciando Contas (`_contas`):** Abrindo, buscando e gerenciando contas.
* **Operações Bancárias:** Implementando métodos para depósito, saque e transferência entre contas.

## Exercício de Codificação

1. Crie um objeto `Banco`.
2. Adicione alguns clientes ao banco.
3. Abra contas para esses clientes.
4. Realize depósitos, saques e transferências entre as contas.
5. Imprima os extratos das contas para verificar as transações.