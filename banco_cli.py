"""Introdução à POO com Python - Sistema Bancário Simplificado"""

import textwrap
from abc import ABC, abstractmethod

# Importar date e datetime
from datetime import datetime, date


class PessoaFisica:
    """Classe base para representar uma pessoa física."""

    def __init__(self, nome: str, cpf: str, endereco: str):
        if not isinstance(cpf, str) or not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome inválido.")
        if not endereco or not isinstance(endereco, str):
            raise ValueError("Endereço inválido.")

        self._nome = nome
        self._cpf = cpf
        self._endereco = endereco

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def endereco(self) -> str:
        return self._endereco

    def __str__(self) -> str:
        return f"Nome: {self.nome}, CPF: {self.cpf}, Endereço: {self.endereco}"

    def __hash__(self):
        return hash(self._cpf)

    def __eq__(self, other):
        if not isinstance(other, PessoaFisica):
            return NotImplemented
        return self._cpf == other._cpf


class Cliente(PessoaFisica):
    """Representa um cliente do banco, herdando de PessoaFisica
    e adicionando informações específicas do relacionamento com o banco."""

    def __init__(self, nome: str, cpf: str, endereco: str):
        super().__init__(nome, cpf, endereco)
        # Adiciona a data de cadastro como informação específica do Cliente
        self._data_cadastro: date = (
            date.today()
        )  # Guarda a data atual no momento da criação
        print(f"Cliente '{nome}' criado em {self._data_cadastro.strftime('%d/%m/%Y')}.")

    @property
    def data_cadastro(self) -> date:
        """Retorna a data em que o cliente foi cadastrado."""
        return self._data_cadastro

    def __str__(self) -> str:
        """Representação em string do Cliente, incluindo data de cadastro."""
        # Chama o __str__ da classe pai e adiciona a informação extra
        pf_str = super().__str__()
        return f"Cliente desde: {self.data_cadastro.strftime('%d/%m/%Y')} | {pf_str}"


# --- Hierarquia de Transações (sem alterações) ---
class Transacao(ABC):
    def __init__(self):
        self._timestamp = datetime.now()

    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("Valor de depósito inválido.")
        super().__init__()
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.depositar(self.valor)
        return sucesso

    def __str__(self) -> str:
        return f"{self.timestamp.strftime('%d-%m-%Y %H:%M:%S')} - Depósito: R$ {self.valor:.2f}"


class Saque(Transacao):
    def __init__(self, valor: float):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("Valor de saque inválido.")
        super().__init__()
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> bool:
        sucesso = conta.sacar(self.valor)
        return sucesso

    def __str__(self) -> str:
        return f"{self.timestamp.strftime('%d-%m-%Y %H:%M:%S')} - Saque   : R$ {self.valor:.2f}"


# --- Classe Conta (sem alterações) ---
class Conta:
    _numero_conta_global = 0

    def __init__(self, cliente: Cliente, agencia: str = "0001"):
        if not isinstance(cliente, Cliente):
            raise TypeError("O titular da conta deve ser um objeto Cliente.")
        self._saldo: float = 0.0
        Conta._numero_conta_global += 1
        self._numero: int = Conta._numero_conta_global
        self._agencia: str = agencia
        self._cliente: Cliente = cliente
        self._historico_transacoes: list[Transacao] = []

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> list[Transacao]:
        return self._historico_transacoes[:]

    def _registrar_transacao(self, transacao: Transacao):
        if isinstance(transacao, Transacao):
            self._historico_transacoes.append(transacao)
        else:
            print("@@@ Tentativa de registrar objeto inválido como transação @@@")

    def sacar(self, valor: float) -> bool:
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("\n@@@ Operação falhou! Valor de saque inválido. @@@")
            return False
        if self.saldo >= valor:
            try:
                transacao_saque = Saque(valor)
                self._saldo -= valor
                self._registrar_transacao(transacao_saque)
                print(
                    f"\n=== Saque de R$ {valor:.2f} realizado com sucesso (Conta {self.numero})! ==="
                )
                return True
            except ValueError as e:
                print(f"\n@@@ Erro interno ao processar saque: {e} @@@")
                return False
        else:
            print(
                f"\n@@@ Operação falhou! Saldo insuficiente (Conta {self.numero}). @@@"
            )
            print(
                f"    Saldo atual: R$ {self.saldo:.2f}, Tentativa de saque: R$ {valor:.2f}"
            )
            return False

    def depositar(self, valor: float) -> bool:
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("\n@@@ Operação falhou! Valor de depósito inválido. @@@")
            return False
        try:
            transacao_deposito = Deposito(valor)
            self._saldo += valor
            self._registrar_transacao(transacao_deposito)
            print(
                f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso (Conta {self.numero})! ==="
            )
            return True
        except ValueError as e:
            print(f"\n@@@ Erro interno ao processar depósito: {e} @@@")
            return False

    def transferir(self, valor: float, conta_destino: "Conta") -> bool:
        if not isinstance(conta_destino, Conta):
            print("\n@@@ Operação falhou! Conta de destino inválida. @@@")
            return False
        if self == conta_destino:
            print("\n@@@ Operação falhou! Conta de origem e destino são as mesmas. @@@")
            return False
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("\n@@@ Operação falhou! Valor de transferência inválido. @@@")
            return False

        saque_bem_sucedido = self.sacar(valor)
        if saque_bem_sucedido:
            deposito_bem_sucedido = conta_destino.depositar(valor)
            if not deposito_bem_sucedido:
                print(
                    "\n@@@ ATENÇÃO: Falha ao depositar na conta destino. Estornando saque da origem... @@@"
                )
                estorno_ok = self.depositar(valor)  # Registra Deposito de estorno
                if estorno_ok:
                    print(
                        f"=== Estorno de R$ {valor:.2f} realizado na conta {self.numero}. ==="
                    )
                else:
                    print(
                        f"@@@ FALHA CRÍTICA: Não foi possível estornar R$ {valor:.2f} para a conta {self.numero}! Contatar suporte. @@@"
                    )
                return False
            else:
                print(
                    f"\n=== Transferência de R$ {valor:.2f} de {self.cliente.nome} para {conta_destino.cliente.nome} realizada com sucesso! ==="
                )
                return True
        else:
            print(
                f"\n@@@ Transferência de R$ {valor:.2f} falhou (origem: {self.numero}). @@@"
            )
            return False

    def exibir_extrato(self):
        print(f"\n================ EXTRATO CONTA {self.numero} ================")
        # Agora exibimos também a data de cadastro do cliente
        print(
            f"Cliente: {self.cliente.nome} (CPF: {self.cliente.cpf}) - Cliente desde: {self.cliente.data_cadastro.strftime('%d/%m/%Y')}"
        )
        print(f"Agência: {self.agencia}\tConta: {self.numero}")
        print("-" * 55)
        if not self._historico_transacoes:
            print("Não foram realizadas movimentações.")
        else:
            print("Histórico de Transações:")
            for transacao in self._historico_transacoes:
                print(transacao)
        print("-" * 55)
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("======================================================")

    def __str__(self) -> str:
        return textwrap.dedent(f"""\
            Agência:\t{self.agencia}
            Conta:\t\t{self.numero}
            Titular:\t{self.cliente.nome} (CPF: {self.cliente.cpf}) - Cadastrado em: {self.cliente.data_cadastro.strftime("%d/%m/%Y")}
            Saldo:\t\tR$ {self.saldo:.2f}
        """)


# --- Classe Banco (sem alterações na lógica principal) ---
# Apenas o método listar_clientes agora se beneficia do __str__ atualizado do Cliente.
class Banco:
    def __init__(self, nome: str, agencia: str = "0001"):
        self._nome: str = nome
        self._agencia: str = agencia
        self._clientes: dict[str, Cliente] = {}
        self._contas: dict[str, Conta] = {}
        print(f"Banco '{self._nome}', Agência {self._agencia} inicializado.")

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def agencia(self) -> str:
        return self._agencia

    def adicionar_cliente(self, cliente: Cliente) -> bool:
        if not isinstance(cliente, Cliente):
            print(
                "\n@@@ Erro: Tentativa de adicionar objeto inválido como cliente. @@@"
            )
            return False
        cpf = cliente.cpf
        if cpf in self._clientes:
            print(f"\n@@@ Erro: Cliente com CPF {cpf} já cadastrado. @@@")
            return False
        else:
            self._clientes[cpf] = cliente
            return True

    def criar_abrir_conta(self, cpf_cliente: str) -> Conta | None:
        cliente = self.buscar_cliente(cpf_cliente)
        if not cliente:
            return None
        if cpf_cliente in self._contas:
            print(
                f"\n@@@ Erro: Cliente {cliente.nome} (CPF: {cpf_cliente}) já possui uma conta ({self._contas[cpf_cliente].numero}). @@@"
            )
            return None
        nova_conta = Conta(cliente=cliente, agencia=self._agencia)
        self._contas[cpf_cliente] = nova_conta
        print(
            f"\n=== Conta {nova_conta.numero} criada com sucesso para o cliente {cliente.nome} (CPF: {cpf_cliente})! ==="
        )
        return nova_conta

    def buscar_cliente(self, cpf: str) -> Cliente | None:
        cliente = self._clientes.get(cpf)
        if not cliente:
            print(f"\n@@@ Erro: Cliente com CPF {cpf} não encontrado. @@@")
        return cliente

    def buscar_conta_por_cpf(self, cpf: str) -> Conta | None:
        conta = self._contas.get(cpf)
        if not conta:
            if cpf in self._clientes:
                print(
                    f"\n@@@ Erro: Cliente {self._clientes[cpf].nome} (CPF: {cpf}) encontrado, mas não possui conta associada. @@@"
                )
            elif cpf not in self._clientes:
                print(
                    f"\n@@@ Erro: Cliente com CPF {cpf} não encontrado (e, portanto, sem conta). @@@"
                )
        return conta

    def realizar_deposito(self, cpf: str, valor: float) -> bool:
        conta = self.buscar_conta_por_cpf(cpf)
        if conta:
            return conta.depositar(valor)
        else:
            return False

    def realizar_saque(self, cpf: str, valor: float) -> bool:
        conta = self.buscar_conta_por_cpf(cpf)
        if conta:
            return conta.sacar(valor)
        else:
            return False

    def realizar_transferencia(
        self, cpf_origem: str, cpf_destino: str, valor: float
    ) -> bool:
        conta_origem = self.buscar_conta_por_cpf(cpf_origem)
        if not conta_origem:
            print(
                f"\n@@@ Transferência falhou: Conta de origem (CPF: {cpf_origem}) não encontrada. @@@"
            )
            return False
        conta_destino = self.buscar_conta_por_cpf(cpf_destino)
        if not conta_destino:
            print(
                f"\n@@@ Transferência falhou: Conta de destino (CPF: {cpf_destino}) não encontrada. @@@"
            )
            return False
        return conta_origem.transferir(valor, conta_destino)

    def consultar_extrato(self, cpf: str):
        conta = self.buscar_conta_por_cpf(cpf)
        if conta:
            conta.exibir_extrato()  # Exibirá o extrato com a data de cadastro

    def listar_clientes(self):
        print("\n--- Lista de Clientes ---")
        if not self._clientes:
            print("Nenhum cliente cadastrado.")
            return
        for cpf, cliente in self._clientes.items():
            print(cliente)  # Usa o __str__ atualizado do Cliente
        print("-" * 25)

    def listar_contas(self):
        print("\n--- Lista de Contas ---")
        if not self._contas:
            print("Nenhuma conta aberta.")
            return
        for cpf, conta in self._contas.items():
            print("-" * 40)
            print(
                conta
            )  # Usa o __str__ atualizado da Conta (que mostra data cadastro do cliente)
        print("-" * 40)


# --- Funções Auxiliares da CLI (sem alterações) ---
def limpar_cpf(cpf_input: str) -> str:
    return "".join(filter(str.isdigit, cpf_input))


def solicitar_cpf(
    mensagem: str = "Informe o CPF do cliente (apenas números): ",
) -> str | None:
    while True:
        cpf_input = input(mensagem).strip()
        cpf_limpo = limpar_cpf(cpf_input)
        if len(cpf_limpo) == 11 and cpf_limpo.isdigit():
            return cpf_limpo
        else:
            print("@@@ CPF inválido. Por favor, informe 11 dígitos numéricos. @@@")
            continuar = input("Tentar novamente? (s/n): ").lower()
        if continuar != "s":
            return None


def solicitar_valor(mensagem: str = "Informe o valor: R$ ") -> float | None:
    while True:
        try:
            valor_input = input(mensagem).strip().replace(",", ".")
            valor = float(valor_input)
            if valor > 0:
                return valor
            else:
                print("@@@ Valor inválido. Deve ser um número positivo. @@@")
        except ValueError:
            print("@@@ Entrada inválida. Por favor, informe um número. @@@")
        continuar = input("Tentar novamente? (s/n): ").lower()
        if continuar != "s":
            return None


def menu() -> str:
    menu_texto = """\n
    ================ MENU ================
    [nc]\tNovo Cliente
    [ac]\tAbrir Conta (para cliente existente)
    [lc]\tListar Clientes
    [la]\tListar Contas
    [d]\tDepositar
    [s]\tSacar
    [t]\tTransferir
    [e]\tExtrato
    [q]\tSair
    ======================================
    => """
    return input(textwrap.dedent(menu_texto)).strip().lower()


# --- Função Principal (main - sem alterações na lógica) ---
def main():
    banco = Banco(nome="Banco Digital OOP Bank")
    while True:
        opcao = menu()
        if opcao == "nc":
            print("\n--- Novo Cliente ---")
            nome = input("Nome completo: ").strip()
            if not nome:
                print("@@@ Nome não pode ser vazio. @@@")
                continue
            cpf = solicitar_cpf()
            if not cpf:
                continue
            endereco = input(
                "Endereço (logradouro, nro - bairro - cidade/UF): "
            ).strip()
            if not endereco:
                print("@@@ Endereço não pode ser vazio. @@@")
                continue
            try:
                novo_cliente = Cliente(nome=nome, cpf=cpf, endereco=endereco)
                banco.adicionar_cliente(novo_cliente)
            except ValueError as e:
                print(f"\n@@@ Erro ao criar cliente: {e} @@@")
        elif opcao == "ac":
            print("\n--- Abrir Conta ---")
            cpf = solicitar_cpf()
            if not cpf:
                continue
            banco.criar_abrir_conta(cpf_cliente=cpf)
        elif opcao == "lc":
            banco.listar_clientes()
        elif opcao == "la":
            banco.listar_contas()
        elif opcao == "d":
            print("\n--- Depósito ---")
            cpf = solicitar_cpf()
            if not cpf:
                continue
            valor = solicitar_valor()
            if valor is not None:
                banco.realizar_deposito(cpf, valor)
        elif opcao == "s":
            print("\n--- Saque ---")
            cpf = solicitar_cpf()
            if not cpf:
                continue
            valor = solicitar_valor()
            if valor is not None:
                banco.realizar_saque(cpf, valor)
        elif opcao == "t":
            print("\n--- Transferência ---")
            cpf_origem = solicitar_cpf("Informe o CPF da conta de ORIGEM: ")
            if not cpf_origem:
                continue
            cpf_destino = solicitar_cpf("Informe o CPF da conta de DESTINO: ")
            if not cpf_destino:
                continue
            valor = solicitar_valor()
            if valor is not None:
                banco.realizar_transferencia(cpf_origem, cpf_destino, valor)
        if valor is not None:
            banco.realizar_transferencia(cpf_origem, cpf_destino, valor)
        elif opcao == "e":
            print("\n--- Extrato ---")
            cpf = solicitar_cpf()
            if not cpf:
                continue
            banco.consultar_extrato(cpf)
        elif opcao == "q":
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\n@@@ Opção inválida! Por favor, escolha uma opção do menu. @@@")


if __name__ == "__main__":
    main()
