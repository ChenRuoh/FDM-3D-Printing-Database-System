<template>
  <div class="materials-page">
    <div class="glass-card page-header">
      <h1>材料管理</h1>
      <button class="btn-primary glass-card" @click="showAddForm = !showAddForm">
        {{ showAddForm ? '取消' : '添加材料' }}
      </button>
    </div>

    <!-- 添加材料表单 -->
    <div v-if="showAddForm" class="glass-card add-form">
      <h3>{{ editingMaterial ? '编辑材料' : '添加新材料' }}</h3>
      <form @submit.prevent="saveMaterial">
        <div class="form-row">
          <div class="form-group">
            <label for="name">材料名称</label>
            <input type="text" id="name" v-model="currentMaterial.name" required>
          </div>
          <div class="form-group">
            <label for="brand">品牌</label>
            <input type="text" id="brand" v-model="currentMaterial.brand">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="filamentDiameter">耗材直径 (mm)</label>
            <input type="number" id="filamentDiameter" v-model.number="currentMaterial.filament_diameter" step="0.1" required>
          </div>
          <div class="form-group">
            <label for="density">密度 (g/cm³)</label>
            <input type="number" id="density" v-model.number="currentMaterial.density" step="0.01">
          </div>
        </div>
        
        <div class="form-group">
          <label for="description">描述</label>
          <textarea id="description" v-model="currentMaterial.description"></textarea>
        </div>
        
        <button type="submit" class="btn-primary glass-card">{{ editingMaterial ? '更新' : '保存' }}</button>
      </form>
    </div>

    <!-- 材料搜索 -->
    <div class="glass-card filter-section">
      <div class="form-group">
        <input type="text" v-model="searchTerm" placeholder="搜索材料...">
      </div>
    </div>

    <!-- 材料列表 -->
    <div class="materials-list">
      <div v-for="material in filteredMaterials" :key="material.id" class="glass-card material-item">
        <div class="material-header">
          <h3>{{ material.name }}</h3>
          <div class="material-brand">{{ material.brand || '未知品牌' }}</div>
        </div>
        <div class="material-details">
          <div class="detail-row">
            <span><strong>耗材直径:</strong> {{ material.filament_diameter }}mm</span>
            <span v-if="material.density"><strong>密度:</strong> {{ material.density }} g/cm³</span>
          </div>
          <p v-if="material.description">{{ material.description }}</p>
        </div>
        <div class="material-actions">
          <button class="btn-edit glass-card" @click="editMaterial(material)">编辑</button>
          <button class="btn-delete glass-card" @click="deleteMaterial(material.id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 模拟数据
const materials = ref([
  {
    id: 1,
    name: 'PLA',
    brand: 'Generic',
    filament_diameter: 1.75,
    density: 1.24,
    description: '聚乳酸，最常用的3D打印材料之一，易于打印，环保可降解'
  },
  {
    id: 2,
    name: 'ABS',
    brand: 'Generic',
    filament_diameter: 1.75,
    density: 1.04,
    description: '丙烯腈丁二烯苯乙烯，强度高，耐热性好，但需要加热床'
  },
  {
    id: 3,
    name: 'PETG',
    brand: 'Overture',
    filament_diameter: 1.75,
    density: 1.27,
    description: '聚对苯二甲酸乙二醇酯，结合了PLA和ABS的优点，强度高且易于打印'
  },
  {
    id: 4,
    name: 'TPU',
    brand: 'SainSmart',
    filament_diameter: 1.75,
    density: 1.2,
    description: '热塑性聚氨酯，柔性材料，适用于制作弹性部件'
  }
])

const showAddForm = ref(false)
const editingMaterial = ref(false)
const searchTerm = ref('')

const currentMaterial = ref({
  id: 0,
  name: '',
  brand: '',
  filament_diameter: 1.75,
  density: null as number | null,
  description: ''
})

const filteredMaterials = computed(() => {
  return materials.value.filter(material => {
    return material.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
           material.brand?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
           material.description?.toLowerCase().includes(searchTerm.value.toLowerCase())
  })
})

const saveMaterial = () => {
  if (editingMaterial.value) {
    // 更新现有材料
    const index = materials.value.findIndex(m => m.id === currentMaterial.value.id)
    if (index !== -1) {
      materials.value[index] = { ...currentMaterial.value }
    }
  } else {
    // 添加新材料
    const newId = Math.max(...materials.value.map(m => m.id), 0) + 1
    materials.value.push({ ...currentMaterial.value, id: newId })
  }
  
  resetForm()
}

const editMaterial = (material: any) => {
  currentMaterial.value = { ...material }
  editingMaterial.value = true
  showAddForm.value = true
}

const deleteMaterial = (id: number) => {
  if (confirm('确定要删除这个材料吗？')) {
    const index = materials.value.findIndex(m => m.id === id)
    if (index !== -1) {
      materials.value.splice(index, 1)
    }
  }
}

const resetForm = () => {
  currentMaterial.value = {
    id: 0,
    name: '',
    brand: '',
    filament_diameter: 1.75,
    density: null,
    description: ''
  }
  editingMaterial.value = false
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

.materials-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.material-item {
  padding: 1.5rem;
}

.material-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.material-header h3 {
  margin: 0;
  color: var(--vt-c-blue-dark);
}

.material-brand {
  font-size: 0.9rem;
  color: var(--vt-c-gray);
}

.material-details .detail-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.material-details p {
  margin: 0;
  color: var(--vt-c-gray);
}

.material-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
</style>