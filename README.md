# Async Bank API

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-API_Docs-85EA2D?logo=swagger&logoColor=black)

API assíncrona para simulação de operações bancárias, desenvolvida como projeto em um bootcamp de python. O sistema permite cadastro de usuários e realização de transações financeiras garantindo integridade.

O deploy deste projeto foi realizado no render.com e você pode testar pelo Swagger
**[aqui](https://transactions-api-1d7y.onrender.com/docs)**

## Funcionalidades

- **Autenticação Segura:** Registro e Login de usuários com OAuth2/JWT
- **Gestão de Contas:** Criação automática de conta corrente ao registrar usuário.
- **Operações Financeiras:**
  - **Depósito:** Incremento de saldo.
  - **Saque:** Decremento de saldo.
  - **Transferência:** Envio entre contas.
- **Extrato:** Consulta de histórico de movimentações.

## Stack Tecnológico

- **Linguagem:** Python 3.12+
- **Framework Web:** FastAPI (Async)
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy 2.0 (Async/Await)
- **Migrações:** Alembic
- **Gerenciador de Pacotes:** Poetry


