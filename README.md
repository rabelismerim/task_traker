# 🚀 Task Tracker

Uma aplicação Full-Stack para gerenciamento dinâmico de tarefas com autenticação de usuários, métricas em tempo real e controle de prazos de vencimento.

---

## 🛠️ Tecnologias Utilizadas

### **Frontend**
- **Vue.js 3** (Composition API `<script setup>`)
- **Vue Router 4** (Navegação e proteção de rotas)
- **Axios** (Consumo de API REST e interceptores HTTP)
- **CSS3 / Flexbox & Grid** (Interface responsiva)

### **Backend**
- **Python 3.11+** & **Django 5.x**
- **Django REST Framework (DRF)**
- **Token / JWT Authentication** (Segurança e sessões)
- **SQLite** (Banco de dados de desenvolvimento)

---

## ✨ Funcionalidades Principais

- 🔐 **Autenticação & Isolamento de Dados:** Cada usuário visualiza e gerencia apenas suas próprias tarefas.
- 📋 **CRUD Completo:** Criação, listagem, edição, atualização parcial (`PATCH`) e exclusão de tarefas.
- ⚡ **Atualização de Status Instantânea:** Marcação de concluída/pendente em tempo real.
- 📊 **Dashboard & Métricas:** Indicadores de progresso geral, tarefas concluídas, pendentes e atrasadas.
- 📄 **Paginação & Ordenação Server-Side:** Paginação de resultados pela API para melhor performance.
- 🚨 **Alerta de Vencimento:** Cálculo automático de prazos ultrapassados para tarefas pendentes.

---

## 🚀 Como Executar

### **1. Backend (Django REST)**
cd backend
python -m venv venv
# No Windows: venv\Scripts\activate | No Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

### **1. Front-end**
# Abra um novo terminal
cd frontend
npm install
npm run dev

👨‍💻 Autor
Desenvolvido por Robert Abel Ismerim

GitHub: @rabelismerim

