<template>
  <div class="parameters-page">
    <div class="glass-card page-header">
      <h1>参数库管理</h1>
      <button class="btn-primary glass-card" @click="showAddForm = !showAddForm">
        {{ showAddForm ? '取消' : '添加参数' }}
      </button>
    </div>

    <!-- 添加参数表单 -->
    <div v-if="showAddForm" class="glass-card add-form">
      <h3>{{ editingParam ? '编辑参数' : '添加新参数' }}</h3>
      <form @submit.prevent="saveParameter">
        <div class="form-row">
          <div class="form-group">
            <label for="name">参数名称</label>
            <input type="text" id="name" v-model="currentParam.name" required>
          </div>
          <div class="form-group">
            <label for="layerHeight">层高 (mm)</label>
            <input type="number" id="layerHeight" v-model.number="currentParam.layer_height" step="0.01" required>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="printSpeed">打印速度 (mm/s)</label>
            <input type="number" id="printSpeed" v-model.number="currentParam.print_speed" required>
          </div>
          <div class="form-group">
            <label for="infillDensity">填充密度 (%)</label>
            <input type="number" id="infillDensity" v-model.number="currentParam.infill_density" required>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="printTemp">打印温度 (°C)</label>
            <input type="number" id="printTemp" v-model.number="currentParam.print_temperature" required>
          </div>
          <div class="form-group">
            <label for="bedTemp">热床温度 (°C)</label>
            <input type="number" id="bedTemp" v-model.number="currentParam.bed_temperature" required>
          </div>
        </div>
        
        <div class="form-group">
          <label for="description">描述</label>
          <textarea id="description" v-model="currentParam.description"></textarea>
        </div>
        
        <button type="submit" class="btn-primary glass-card">{{ editingParam ? '更新' : '保存' }}</button>
      </form>
    </div>

    <!-- 参数搜索和过滤 -->
    <div class="glass-card filter-section">
      <div class="form-row">
        <div class="form-group">
          <input type="text" v-model="searchTerm" placeholder="搜索参数...">
        </div>
        <div class="form-group">
          <select v-model="filterMaterial">
            <option value="">所有材料</option>
            <option v-for="material in materials" :key="material.id" :value="material.id">
              {{ material.name }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- 参数列表 -->
    <div class="parameters-list">
      <div v-for="param in filteredParameters" :key="param.id" class="glass-card parameter-item">
        <div class="param-header">
          <h3>{{ param.name }}</h3>
          <div class="actions">
            <button class="btn-edit glass-card" @click="editParameter(param)">编辑</button>
            <button class="btn-delete glass-card" @click="deleteParameter(param.id)">删除</button>
          </div>
        </div>
        <div class="param-details">
          <div class="detail-row">
            <span>层高: {{ param.layer_height }}mm</span>
            <span>打印速度: {{ param.print_speed }}mm/s</span>
            <span>填充密度: {{ param.infill_density }}%</span>
          </div>
          <div class="detail-row">
            <span>打印温度: {{ param.print_temperature }}°C</span>
            <span>热床温度: {{ param.bed_temperature }}°C</span>
          </div>
          <p v-if="param.description">{{ param.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 模拟数据 - 在实际应用中这将来自API
const parameters = ref([
  {
    id: 1,
    name: 'PLA标准参数',
    layer_height: 0.2,
    print_speed: 60,
    infill_density: 20,
    print_temperature: 200,
    bed_temperature: 60,
    travel_speed: 120,
    retraction_distance: 1,
    retraction_speed: 45,
    description: '适用于大多数PLA材料的标准打印参数'
  },
  {
    id: 2,
    name: 'PETG高速参数',
    layer_height: 0.25,
    print_speed: 80,
    infill_density: 15,
    print_temperature: 240,
    bed_temperature: 80,
    travel_speed: 150,
    retraction_distance: 1.5,
    retraction_speed: 45,
    description: '适用于PETG材料的高速打印参数'
  }
])

const materials = ref([
  { id: 1, name: 'PLA' },
  { id: 2, name: 'ABS' },
  { id: 3, name: 'PETG' },
  { id: 4, name: 'TPU' }
])

const showAddForm = ref(false)
const editingParam = ref(false)
const searchTerm = ref('')
const filterMaterial = ref('')

const currentParam = ref({
  id: 0,
  name: '',
  layer_height: 0.2,
  print_speed: 60,
  infill_density: 20,
  print_temperature: 200,
  bed_temperature: 60,
  travel_speed: 120,
  retraction_distance: 1,
  retraction_speed: 45,
  description: ''
})

const filteredParameters = computed(() => {
  return parameters.value.filter(param => {
    const matchesSearch = param.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                          param.description?.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesMaterial = !filterMaterial.value || param.id % 2 === parseInt(filterMaterial.value) % 2 // 简单模拟关联
    return matchesSearch && matchesMaterial
  })
})

const saveParameter = () => {
  if (editingParam.value) {
    // 更新现有参数
    const index = parameters.value.findIndex(p => p.id === currentParam.value.id)
    if (index !== -1) {
      parameters.value[index] = { ...currentParam.value }
    }
  } else {
    // 添加新参数
    const newId = Math.max(...parameters.value.map(p => p.id), 0) + 1
    parameters.value.push({ ...currentParam.value, id: newId })
  }
  
  resetForm()
}

const editParameter = (param: any) => {
  currentParam.value = { ...param }
  editingParam.value = true
  showAddForm.value = true
}

const deleteParameter = (id: number) => {
  if (confirm('确定要删除这个参数吗？')) {
    const index = parameters.value.findIndex(p => p.id === id)
    if (index !== -1) {
      parameters.value.splice(index, 1)
    }
  }
}

const resetForm = () => {
  currentParam.value = {
    id: 0,
    name: '',
    layer_height: 0.2,
    print_speed: 60,
    infill_density: 20,
    print_temperature: 200,
    bed_temperature: 60,
    travel_speed: 120,
    retraction_distance: 1,
    retraction_speed: 45,
    description: ''
  }
  editingParam.value = false
  showAddForm.value = false
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.add-form {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.3);
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.btn-primary {
  background-color: var(--vt-c-blue);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-edit {
  background-color: var(--vt-c-green);
  color: white;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-delete {
  background-color: #ff4757;
  color: white;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.filter-section {
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.parameters-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.parameter-item {
  padding: 1.5rem;
}

.param-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.param-header h3 {
  margin: 0;
  color: var(--vt-c-blue-dark);
}

.actions {
  display: flex;
}

.param-details .detail-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.param-details p {
  margin-top: 1rem;
  color: var(--vt-c-gray);
}
</style>