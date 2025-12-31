# 🏦 Async Bank API

API robusta e assíncrona para simulação de operações bancárias, desenvolvida como projeto final de curso. O sistema gerencia contas correntes, realiza transações financeiras com validação de saldo e garante a integridade dos dados através de transações atômicas no banco de dados.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)

## 🚀 Funcionalidades

- **Autenticação Segura:** Registro e Login de usuários via JWT (JSON Web Tokens).
- **Gestão de Contas:** Criação automática de conta corrente ao registrar usuário.
- **Operações Financeiras:**
  - **Depósito:** Incremento de saldo.
  - **Saque:** Decremento de saldo.
- **Extrato:** Consulta de histórico de movimentações.

## 🛠️ Stack Tecnológico

- **Linguagem:** Python 3.12+
- **Framework Web:** FastAPI (Async)
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy 2.0 (Async/Await)
- **Migrações:** Alembic
- **Gerenciador de Pacotes:** Poetry


