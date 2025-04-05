# Aula 1: Introdução à POO, Diagramas de Classes, SoC e SSOT

## O que é Programação Orientada a Objetos (POO)?

POO é um paradigma de programação que organiza o código em torno de **objetos**, que combinam dados (**atributos**) e ações que podem ser executadas nesses dados (**métodos**).  Isso permite uma melhor organização, reutilização e manutenção do código.

**Pilares da POO:**

* **Abstração:** Ocultar a complexidade da implementação, expondo apenas a interface essencial para o usuário. _Exemplo: você interage com um caixa eletrônico sem saber como o sistema bancário funciona por trás._
* **Encapsulamento:** Agrupar dados e métodos relacionados dentro de uma classe, protegendo os dados de acesso externo indevido. _Exemplo: a classe `Conta` encapsula o saldo e os métodos para depósito e saque._
* **Herança:** Criar novas classes (filhas) a partir de classes existentes (pais), herdando seus atributos e métodos. _Exemplo: a classe `Cliente` herda atributos da classe `PessoaFisica`._
* **Polimorfismo:** A capacidade de objetos de diferentes classes responderem ao mesmo método de maneiras diferentes. _Exemplo: as classes `Deposito` e `Saque` implementam o método `registrar` de forma específica para cada tipo de transação._

## Classes e Objetos

* **Classe:** Um modelo ou _blueprint_ para criar objetos. Define os atributos e métodos que os objetos terão.  _Analogia: a planta de uma casa._
* **Objeto:** Uma instância de uma classe.  _Analogia: a casa construída a partir da planta._

## Atributos e Métodos

* **Atributos:** Características ou dados associados a um objeto. _Exemplo: o saldo de uma conta._
* **Métodos:** Ações que um objeto pode realizar. _Exemplo: depositar dinheiro em uma conta._

## Princípios de Design: SoC e SSOT

* **Separação de Preocupações (SoC):** Dividir o código em partes independentes com responsabilidades específicas. _Exemplo: no nosso sistema, `PessoaFisica` gerencia dados pessoais, `Conta` gerencia transações e saldos, e `Banco` gerencia clientes e contas._  No diagrama de classes, cada classe representa uma preocupação separada.
* **Responsabilidade Única (SSOT - Single Source of Truth):** Cada informação deve ter apenas uma fonte no sistema. _Exemplo: os dados do cliente são armazenados apenas na classe `PessoaFisica`, evitando duplicação e inconsistências._ No diagrama, o relacionamento entre `Cliente` e `Conta` demonstra o SSOT, pois `Conta` referencia os dados do cliente em `Cliente`, sem duplicá-los.

## Exercício de Codificação

1. Crie um objeto `PessoaFisica` com nome, CPF e endereço.
2. Crie um objeto `Cliente` utilizando a classe `PessoaFisica`.
3. Imprima os dados de ambos os objetos.
4. **Pense:** Como o princípio SSOT está sendo aplicado neste exercício?  Onde estão os dados da pessoa armazenados?