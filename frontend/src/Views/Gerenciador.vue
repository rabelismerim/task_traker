<template>
  <div class="page-container">
    <div class="content-wrapper">
      
      <!-- CABEÇALHO -->
      <div class="card header-card">
        <div class="brand">
          <div class="brand-icon">✓</div>
          <h1 class="brand-title">Task Tracker</h1>
        </div>
        <button @click="handleLogout" class="btn btn-secondary">
          Sair
        </button>
      </div>

      <!-- FORMULÁRIO DE TAREFA -->
      <div class="card form-card">
        <h2 class="card-title">
          {{ isEditing ? 'Editar Tarefa' : 'Nova Tarefa' }}
        </h2>

        <form @submit.prevent="handleSubmit" class="form-grid">
          <input 
            v-model="form.title" 
            type="text" 
            placeholder="Título da tarefa" 
            required
            class="form-control"
          />

          <select v-model="form.priority" class="form-control">
            <option value="low">Baixa Prioridade</option>
            <option value="medium">Média Prioridade</option>
            <option value="high">Alta Prioridade</option>
          </select>

          <input 
            v-model="form.category" 
            type="text" 
            placeholder="Categoria" 
            class="form-control"
          />

          <input 
            v-model="form.due_date" 
            type="date" 
            class="form-control"
          />

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">
              {{ isEditing ? 'Atualizar Tarefa' : 'Criar Tarefa' }}
            </button>
            
            <button v-if="isEditing" type="button" @click="resetForm" class="btn btn-secondary">
              Cancelar
            </button>
          </div>
        </form>
      </div>

      <!-- TABELA DE TAREFAS -->
      <div class="card table-card">
        <div class="table-header">
          <h2 class="card-title">Suas Tarefas</h2>
        </div>

        <div class="table-responsive">
          <table class="custom-table">
            <thead>
              <tr>
                <th style="width: 50px;" class="text-center">DONE</th>
                <th>STATUS</th>
                <th>TAREFA</th>
                <th>PRIORIDADE</th>
                <th>CATEGORIA</th>
                <th>VENCIMENTO</th>
                <th class="text-right">AÇÕES</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="task in tasks" 
                :key="task.id" 
                :class="{ 'row-completed': isCompleted(task) }"
              >
                <!-- CHECKBOX DE CONCLUSÃO -->
                <td class="text-center">
                  <input 
                    type="checkbox" 
                    :checked="isCompleted(task)"
                    @change="toggleTaskStatus(task)"
                    class="task-checkbox"
                    title="Marcar como concluída/pendente"
                  />
                </td>

                <!-- BADGE DE STATUS -->
                <td>
                  <span 
                    class="badge" 
                    :class="isCompleted(task) ? 'badge-completed' : 'badge-pending'"
                  >
                    {{ isCompleted(task) ? 'Concluída' : 'Pendente' }}
                  </span>
                </td>

                <!-- TÍTULO DA TAREFA (COM STRIKETHROUGH) -->
                <td class="font-bold task-title-cell">
                  <span :class="{ 'line-through': isCompleted(task) }">
                    {{ task.title }}
                  </span>
                </td>

                <td class="text-priority">{{ task.priority }}</td>
                <td class="text-muted">{{ task.category || '-' }}</td>
                <td class="text-muted">{{ task.due_date || '-' }}</td>

                <!-- AÇÕES -->
                <td class="text-right actions-cell">
                  <button @click="startEdit(task)" class="icon-btn edit-btn" title="Editar">
                    ✏️
                  </button>
                  <button @click="openDeleteModal(task)" class="icon-btn delete-btn" title="Excluir">
                    🗑️
                  </button>
                </td>
              </tr>

              <tr v-if="tasks.length === 0">
                <td colspan="7" class="empty-state">
                  Nenhuma tarefa encontrada.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- MODAL DE CONFIRMAÇÃO DE REMOÇÃO -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal-card">
        <h3 class="modal-title">Confirmar Exclusão</h3>
        <p class="modal-body">
          Tem certeza que deseja remover a tarefa <strong>"{{ taskToDelete?.title }}"</strong>? Esta ação não pode ser desfeita.
        </p>
        <div class="modal-actions">
          <button @click="showDeleteModal = false" class="btn btn-secondary">Cancelar</button>
          <button @click="confirmDelete" class="btn btn-danger">Excluir</button>
        </div>
      </div>
    </div>

    <!-- MODAL DE SUCESSO -->
    <div v-if="showSuccessModal" class="modal-overlay">
      <div class="modal-card modal-center">
        <div class="success-icon">✓</div>
        <h3 class="modal-title">Sucesso!</h3>
        <p class="modal-body">{{ successMessage }}</p>
        <button @click="showSuccessModal = false" class="btn btn-primary btn-full">OK</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const tasks = ref([])
const isEditing = ref(false)
const editingTaskId = ref(null)

const form = ref({
  title: '',
  priority: 'medium',
  category: '',
  due_date: ''
})

const showDeleteModal = ref(false)
const showSuccessModal = ref(false)
const successMessage = ref('')
const taskToDelete = ref(null)

const fetchTasks = async () => {
  try {
    const response = await api.get('tasks/')
    tasks.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao buscar tarefas:', error)
  }
}

// Verifica se a tarefa está concluída
const isCompleted = (task) => {
  if (typeof task.status === 'string') {
    return task.status.toLowerCase() === 'concluída' || task.status.toLowerCase() === 'completed'
  }
  return !!task.completed
}

// Alterna o status via PATCH
const toggleTaskStatus = async (task) => {
  const currentlyCompleted = isCompleted(task)
  const newStatus = currentlyCompleted ? 'Pendente' : 'Concluída'

  // Atualização otimista local para resposta instantânea na UI
  const previousStatus = task.status
  task.status = newStatus

  try {
    await api.patch(`tasks/${task.id}/`, {
      status: newStatus
    })
  } catch (error) {
    console.error('Erro ao alterar status da tarefa:', error)
    // Reverte em caso de erro no servidor
    task.status = previousStatus
    alert('Não foi possível alterar o status da tarefa.')
  }
}

const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      await api.put(`tasks/${editingTaskId.value}/`, form.value)
      successMessage.value = 'Tarefa alterada com sucesso!'
    } else {
      await api.post('tasks/', form.value)
      successMessage.value = 'Tarefa criada com sucesso!'
    }
    resetForm()
    showSuccessModal.value = true
    fetchTasks()
  } catch (error) {
    console.error('Erro ao salvar tarefa:', error)
  }
}

const startEdit = (task) => {
  isEditing.value = true
  editingTaskId.value = task.id
  form.value = {
    title: task.title,
    priority: task.priority || 'medium',
    category: task.category || '',
    due_date: task.due_date || ''
  }
}

const resetForm = () => {
  isEditing.value = false
  editingTaskId.value = null
  form.value = { title: '', priority: 'medium', category: '', due_date: '' }
}

const openDeleteModal = (task) => {
  taskToDelete.value = task
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await api.delete(`tasks/${taskToDelete.value.id}/`)
    showDeleteModal.value = false
    successMessage.value = 'Tarefa removida com sucesso!'
    showSuccessModal.value = true
    fetchTasks()
  } catch (error) {
    console.error('Erro ao excluir tarefa:', error)
  }
}

const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background-color: #f4f6f9;
  padding: 24px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #eef2f6;
}

.header-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background-color: #2563eb;
  color: #fff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.brand-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-top: 0;
  margin-bottom: 16px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.form-control {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #f8fafc;
  font-size: 0.9rem;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #2563eb;
  background-color: #fff;
}

.form-actions {
  grid-column: 1 / -1;
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.btn {
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary { background-color: #2563eb; color: #fff; }
.btn-primary:hover { background-color: #1d4ed8; }

.btn-secondary { background-color: #f1f5f9; color: #475569; }
.btn-secondary:hover { background-color: #e2e8f0; }

.btn-danger { background-color: #dc2626; color: #fff; }
.btn-danger:hover { background-color: #b91c1c; }

.btn-full { width: 100%; }

.table-responsive {
  overflow-x: auto;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;
}

.custom-table th {
  background-color: #f8fafc;
  padding: 12px 16px;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 700;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e2e8f0;
}

.custom-table td {
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  transition: all 0.2s ease;
}

/* CHECKBOX PERSONALIZADO */
.task-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #16a34a;
}

/* ESTILOS DE TAREFA CONCLUÍDA */
.row-completed {
  background-color: #f8fafc;
}

.row-completed td {
  color: #94a3b8 !important;
}

.line-through {
  text-decoration: line-through;
  color: #94a3b8;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  display: inline-block;
}

.badge-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-completed {
  background-color: #dcfce7;
  color: #15803d;
}

.font-bold { font-weight: 600; color: #0f172a; }
.text-priority { color: #d97706; font-weight: 600; }
.text-muted { color: #64748b; }
.text-right { text-align: right; }
.text-center { text-align: center; }

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px;
}

.empty-state {
  text-align: center;
  color: #94a3b8;
  padding: 24px;
}

/* MODAIS */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.modal-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.modal-center { text-align: center; }

.modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
  margin-top: 0;
  margin-bottom: 8px;
}

.modal-body {
  font-size: 0.9rem;
  color: #475569;
  margin-bottom: 20px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.success-icon {
  width: 48px;
  height: 48px;
  background-color: #dcfce7;
  color: #16a34a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 12px auto;
}
</style>