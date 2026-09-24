<script setup>
import { ref } from 'vue';
import api from '../services/api';

const emit = defineEmits(['login-success']);

const username = ref('');
const password = ref('');
const loginError = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
  if (!username.value || !password.value) return;
  
  isLoading.value = true;
  loginError.value = '';

  try {
    const response = await api.post('token/', {
      username: username.value,
      password: password.value
    });
    
    localStorage.setItem('token', response.data.access);
    localStorage.setItem('refreshToken', response.data.refresh);
    
    username.value = '';
    password.value = '';
    emit('login-success');
  } catch (error) {
    loginError.value = 'Usuário ou senha incorretos.';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-wrapper">
    <div class="login-card">
      
      <!-- Cabeçalho -->
      <div class="card-header">
        <div class="icon-box">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1>Task Tracker</h1>
        <p>Faça login para gerenciar suas tarefas</p>
      </div>

      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Usuário</label>
          <input 
            v-model="username" 
            type="text" 
            required
            placeholder="Seu usuário"
          />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input 
            v-model="password" 
            type="password" 
            required
            placeholder="••••••••"
          />
        </div>

        <div v-if="loginError" class="error-banner">
          {{ loginError }}
        </div>

        <button type="submit" :disabled="isLoading" class="btn-submit">
          {{ isLoading ? 'Entrando...' : 'Acessar Painel' }}
        </button>
      </form>

    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
  box-sizing: border-box;
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
  border: 1px solid #e2e8f0;
  padding: 2.5rem 2rem;
  box-sizing: border-box;
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.icon-box {
  width: 56px;
  height: 56px;
  background-color: #2563eb;
  color: #ffffff;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem auto;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.icon-svg {
  width: 28px;
  height: 28px;
}

.card-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.card-header p {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.35rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  text-align: left;
}

.form-group label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  background-color: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  background-color: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.error-banner {
  padding: 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 8px;
  font-size: 0.8125rem;
  text-align: center;
  font-weight: 500;
}

.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background-color: #2563eb;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.875rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.btn-submit:hover {
  background-color: #1d4ed8;
}

.btn-submit:active {
  transform: scale(0.98);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>