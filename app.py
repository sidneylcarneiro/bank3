
from abc import ABC, abstractmethod
from datetime import date, datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        return conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        return conta.sacar(self.valor)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero: int, agencia: str = "0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(cliente, numero)

    def sacar(self, valor: float) -> bool:
        if valor <= 0 or valor > self.saldo:
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        self.saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, cliente, numero: int, limite: float, limite_saques: int):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        if transacao.registrar(conta):
            conta.historico.adicionar_transacao(transacao)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento



def main():
    clientes = []
    contas = []
    numero_conta = 1 

    def filtrar_cliente(cpf, clientes):
        return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

    def recuperar_conta_cliente(cliente):
        if not cliente.contas:
            print("\nCliente não possui contas!")
            return None
        
        print("\nContas disponíveis:")
        for i, conta in enumerate(cliente.contas):
            print(f"{i + 1} - Agência: {conta.agencia} Número: {conta.numero}")
        
        while True:
            try:
                opcao = int(input("Selecione a conta (número): "))
                if 1 <= opcao <= len(cliente.contas):
                    return cliente.contas[opcao - 1]
                print("Opção inválida!")
            except ValueError:
                print("Digite um número válido!")

    def depositar(clientes):
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente:
            print("\nCliente não encontrado!")
            return
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        while True:
            try:
                valor = float(input("Informe o valor do depósito: "))
                if valor <= 0:
                    print("Valor deve ser positivo!")
                    continue
                
                transacao = Deposito(valor)
                cliente.realizar_transacao(conta, transacao)
                print("\nDepósito realizado com sucesso!")
                break
            except ValueError:
                print("Valor inválido!")

    def sacar(clientes):
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente:
            print("\nCliente não encontrado!")
            return
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        if isinstance(conta, ContaCorrente):
            saques_hoje = sum(
                1 for transacao in conta.historico.transacoes 
                if isinstance(transacao, Saque) and transacao.data.date() == datetime.today().date()
            )
            
            if saques_hoje >= conta.limite_saques:
                print(f"\nLimite diário de saques atingido ({conta.limite_saques})!")
                return
        
        while True:
            try:
                valor = float(input("Informe o valor do saque: "))
                
                if valor <= 0:
                    print("Valor deve ser positivo!")
                    continue
                
                if isinstance(conta, ContaCorrente) and valor > conta.limite:
                    print(f"\nValor excede o limite por saque de R$ {conta.limite:.2f}!")
                    continue
                
                transacao = Saque(valor)
                cliente.realizar_transacao(conta, transacao)
                print("\nSaque realizado com sucesso!")
                break
            except ValueError:
                print("Valor inválido!")

    def exibir_extrato(clientes):
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente:
            print("\nCliente não encontrado!")
            return
        
        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return
        
        print("\n================ EXTRATO ================")
        if not conta.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in conta.historico.transacoes:
                tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
                valor = transacao.valor
                print(f"{tipo}: R$ {valor:.2f}")
        
        print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
        print("=========================================")

    def criar_cliente(clientes):
        cpf = input("Informe o CPF (somente números): ")
        if filtrar_cliente(cpf, clientes):
            print("\nJá existe cliente com esse CPF!")
            return
        
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        
        try:
            dia, mes, ano = map(int, data_nascimento.split('-'))
            data_nascimento = date(ano, mes, dia)
            cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
            clientes.append(cliente)
            print("\nCliente criado com sucesso!")
        except (ValueError, IndexError):
            print("\nData de nascimento inválida!")

    def criar_conta(numero_conta, clientes, contas):
        cpf = input("Informe o CPF do cliente (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)
        
        if not cliente:
            print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
            return numero_conta
        
        limite = 500 
        limite_saques = 3 
        
        conta = ContaCorrente(cliente, numero_conta, limite, limite_saques)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        
        print("\nConta criada com sucesso!")
        print(f"Agência: {conta.agencia} Número: {conta.numero}")
        return numero_conta + 1

    def listar_contas(contas):
        if not contas:
            print("\nNenhuma conta cadastrada!")
            return
        
        print("\n============= CONTAS CADASTRADAS =============")
        for conta in contas:
            print(f"Agência: {conta.agencia}")
            print(f"Número: {conta.numero}")
            print(f"Titular: {conta.cliente.nome}")
            print(f"Saldo: R$ {conta.saldo:.2f}")
            print("=" * 50)

    while True:
        print("\n=== Sistema Bancário ===")
        print("1. Novo cliente")
        print("2. Nova conta")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Extrato")
        print("6. Listar contas")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            criar_cliente(clientes)
        elif opcao == "2":
            numero_conta = criar_conta(numero_conta, clientes, contas)
        elif opcao == "3":
            depositar(clientes)
        elif opcao == "4":
            sacar(clientes)
        elif opcao == "5":
            exibir_extrato(clientes)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
