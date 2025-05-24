# Sistema Bancário em Python

Este é um sistema bancário simples implementado em Python que permite gerenciar clientes, contas correntes e realizar operações bancárias básicas como depósitos, saques e consulta de extratos.

## Funcionalidades

- **Cadastro de clientes** (pessoas físicas com CPF, nome, data de nascimento e endereço)
- **Criação de contas correntes** vinculadas a clientes existentes
- **Operações bancárias**:
  - Depósitos
  - Saques (com limites configuráveis)
  - Consulta de extrato
- **Listagem de contas** cadastradas

## Estrutura do Código

O sistema está organizado em classes que representam os principais conceitos do domínio bancário:

- `Transacao`: Classe abstrata base para operações bancárias
  - `Deposito`: Implementação de transação de depósito
  - `Saque`: Implementação de transação de saque
- `Historico`: Registra as transações realizadas em uma conta
- `Conta`: Classe base para contas bancárias
  - `ContaCorrente`: Implementação específica de conta corrente com limites
- `Cliente`: Representa um cliente do banco
  - `PessoaFisica`: Implementação para clientes pessoas físicas

## Como Executar

1. Certifique-se de ter Python instalado (versão 3.6 ou superior recomendada)
2. Execute o arquivo principal:
   ```
   python app.py
   ```
3. Siga o menu interativo para utilizar as funcionalidades do sistema

## Requisitos

- Python 3.x
- Nenhuma dependência externa necessária

## Limitações

- Os dados são armazenados apenas em memória (não persistem após encerrar o programa)
- Não há autenticação de usuários
- Interface apenas por linha de comando

## Melhorias Possíveis

- Persistência dos dados em arquivo ou banco de dados
- Implementação de outros tipos de contas (poupança, investimento)
- Interface gráfica ou web
- Autenticação de usuários
- Transferências entre contas
