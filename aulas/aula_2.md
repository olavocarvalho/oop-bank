# Aula 2: Herança e Polimorfismo em Ação

## Revisão da Aula 1

* Breve revisão dos conceitos de POO: abstração, encapsulamento, herança e polimorfismo.
* Revisão de classes, objetos, atributos e métodos.
* Relembrar os princípios SoC e SSOT e como eles se aplicam ao diagrama de classes.

## Herança em Detalhes

* **`super()`:** Palavra-chave para acessar métodos da classe pai. Permite reutilizar código e evitar redundância. _Exemplo: como `Cliente` usa `super()` para chamar o construtor de `PessoaFisica`._
* **Sobrescrita de Métodos:** Modificar o comportamento de um método herdado da classe pai. _Exemplo: como `__str__` é sobrescrito em `Cliente` e `Conta` para exibir informações específicas._

## Polimorfismo no Sistema Bancário

* **Classes Abstratas (ABC):** Classes que não podem ser instanciadas diretamente, servindo como modelos para classes filhas. _Exemplo: `Transacao` é uma classe abstrata._
* **Métodos Abstratos:** Métodos declarados na classe abstrata, mas sem implementação. Devem ser implementados pelas classes filhas. _Exemplo: `valor` e `registrar` em `Transacao`._
* **Exemplo Prático:** Demonstrar como `Deposito` e `Saque`, apesar de diferentes, podem ser tratados como `Transacao`.

## Exercício de Codificação

1. Crie um objeto `Conta`.
2. Crie objetos `Deposito` e `Saque` e registre-os na conta.
3. Imprima o histórico de transações da conta.  Observe como diferentes tipos de transações são exibidas de forma consistente.