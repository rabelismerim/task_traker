<script setup>
import { ref, onMounted } from 'vue';
import Login from './views/Login.vue';
import Gerenciador from './views/Gerenciador.vue';

const isAuthenticated = ref(false);

const checkAuth = () => {
  const token = localStorage.getItem('token');
  isAuthenticated.value = !!token;
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken');
  isAuthenticated.value = false;
};

onMounted(checkAuth);
</script>

<template>
  <Login 
    v-if="!isAuthenticated" 
    @login-success="checkAuth" 
  />
  <Gerenciador 
    v-else 
    @logout="handleLogout" 
  />
</template>