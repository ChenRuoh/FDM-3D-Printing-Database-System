<template>
  <div class="printers-page">
    <div class="glass-card page-header">
      <h1>打印机管理</h1>
      <button class="btn-primary glass-card" @click="showAddForm = !showAddForm">
        {{ showAddForm ? '取消' : '添加打印机' }}
      </button>
    </div>

    <!-- 添加打印机表单 -->
    <div v-if="showAddForm" class="glass-card add-form">
      <h3>{{ editingPrinter ? '编辑打印机' : '添加新打印机' }}</h3>
      <form @submit.prevent="savePrinter">
        <div class="form-row">
          <div class="form-group">
            <label for="name">打印机名称</label>
            <input type="text" id="name" v-model="currentPrinter.name" required>
          </div>
          <div class="form-group">
            <label for="manufacturer">制造商</label>
            <input type="text" id="manufacturer" v-model="currentPrinter.manufacturer">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="nozzleDiameter">喷嘴直径 (mm)</label>
            <input type="number" id="nozzleDiameter" v-model.number="currentPrinter.nozzle_diameter" step="0.1" required>
          </div>
          <div class="form-group">
            <label for="maxPrintTemp">最高打印温度 (°C)</label>
            <input type="number" id="maxPrintTemp" v-model.number="currentPrinter.max_print_temp" required>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="maxBedTemp">最高热床温度 (°C)</label>
            <input type="number" id="maxBedTemp" v-model.number="currentPrinter.max_bed_temp" required>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="buildVolumeX">构建体积 X (mm)</label>
            <input type="number" id="buildVolumeX" v-model.number="currentPrinter.build_volume_x" required>
          </div>
          <div class="form-group">
            <label for="buildVolumeY">构建体积 Y (mm)</label>
            <input type="number" id="buildVolumeY" v-model.number="currentPrinter.build_volume_y" required>
          </div>
          <div class="form-group">
            <label for="buildVolumeZ">构建体积 Z (mm)</label>
            <input type="number" id="buildVolumeZ" v-model.number="currentPrinter.build_volume_z" required>
          </div>
        </div>
        
        <div class="form-group">
          <label for="description">描述</label>
          <textarea id="description" v-model="currentPrinter.description"></textarea>
        </div>
        
        <button type="submit" class="btn-primary glass-card">{{ editingPrinter ? '更新' : '保存' }}</button>
      </form>
    </div>

    <!-- 打印机搜索 -->
    <div class="glass-card filter-section">
      <div class="form-group">
        <input type="text" v-model="searchTerm" placeholder="搜索打印机...">
      </div>
    </div>

    <!-- 打印机列表 -->
    <div class="printers-list">
      <div v-for="printer in filteredPrinters" :key="printer.id" class="glass-card printer-item">
        <div class="printer-header">
          <h3>{{ printer.name }}</h3>
          <div class="printer-manufacturer">{{ printer.manufacturer || '未知制造商' }}</div>
        </div>
        <div class="printer-details">
          <div class="detail-row">
            <span><strong>喷嘴直径:</strong> {{ printer.nozzle_diameter }}mm</span>
            <span><strong>最高打印温度:</strong> {{ printer.max_print_temp }}°C</span>
          </div>
          <div class="detail-row">
            <span><strong>最高热床温度:</strong> {{ printer.max_bed_temp }}°C</span>
          </div>
          <div class="detail-row">
            <span><strong>构建体积:</strong> {{ printer.build_volume_x }}×{{ printer.build_volume_y }}×{{ printer.build_volume_z }}mm</span>
          </div>
          <p v-if="printer.description">{{ printer.description }}</p>
        </div>
        <div class="printer-actions">
          <button class="btn-edit glass-card" @click="editPrinter(printer)">编辑</button>
          <button class="btn-delete glass-card" @click="deletePrinter(printer.id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 模拟数据
const printers = ref([
  {
    id: 1,
    name: 'Ender 3',
    manufacturer: 'Creality',
    nozzle_diameter: 0.4,
    max_print_temp: 270,
    max_bed_temp: 100,
    build_volume_x: 220,
    build_volume_y: 220,
    build_volume_z: 250,
    description: '经济实惠的FDM 3D打印机，适合初学者和爱好者'
  },
  {
    id: 2,
    name: 'Prusa MK3S',
    manufacturer: 'Prusa Research',
    nozzle_diameter: 0.4,
    max_print_temp: 300,
    max_bed_temp: 120,
    build_volume_x: 250,
    build_volume_y: 210,
    build_volume_z: 210,
    description: '高质量的开源3D打印机，以可靠性和打印质量著称'
  },
  {
    id: 3,
    name: 'CR-10',
    manufacturer: 'Creality',
    nozzle_diameter: 0.4,
    max_print_temp: 270,
    max_bed_temp: 100,
    build_volume_x: 300,
    build_volume_y: 300,
    build_volume_z: 400,
    description: '大尺寸打印床的FDM 3D打印机，适合打印大型模型'
  },
  {
    id: 4,
    name: 'Anycubic Mega',
    manufacturer: 'Anycubic',
    nozzle_diameter: 0.4,
    max_print_temp: 260,
    max_bed_temp: 100,
    build_volume_x: 210,
    build_volume_y: 210,
    build_volume_z: 205,
    description: '紧凑型3D打印机，具有良好的性价比'
  }
])

const showAddForm = ref(false)
const editingPrinter = ref(false)
const searchTerm = ref('')

const currentPrinter = ref({
  id: 0,
  name: '',
  manufacturer: '',
  nozzle_diameter: 0.4,
  max_print_temp: 270,
  max_bed_temp: 100,
  build_volume_x: 220,
  build_volume_y: 220,
  build_volume_z: 250,
  description: ''
})

const filteredPrinters = computed(() => {
  return printers.value.filter(printer => {
    return printer.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
           printer.manufacturer?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
           printer.description?.toLowerCase().includes(searchTerm.value.toLowerCase())
  })
})

const savePrinter = () => {
  if (editingPrinter.value) {
    // 更新现有打印机
    const index = printers.value.findIndex(p => p.id === currentPrinter.value.id)
    if (index !== -1) {
      printers.value[index] = { ...currentPrinter.value }
    }
  } else {
    // 添加新打印机
    const newId = Math.max(...printers.value.map(p => p.id), 0) + 1
    printers.value.push({ ...currentPrinter.value, id: newId })
  }
  
  resetForm()
}

const editPrinter = (printer: any) => {
  currentPrinter.value = { ...printer }
  editingPrinter.value = true
  showAddForm.value = true
}

const deletePrinter = (id: number) => {
  if (confirm('确定要删除这个打印机吗？')) {
    const index = printers.value.findIndex(p => p.id === id)
    if (index !== -1) {
      printers.value.splice(index, 1)
    }
  }
}

const resetForm = () => {
  currentPrinter.value = {
    id: 0,
    name: '',
    manufacturer: '',
    nozzle_diameter: 0.4,
    max_print_temp: 270,
    max_bed_temp: 100,
    build_volume_x: 220,
    build_volume_y: 220,
    build_volume_z: 250,
    description: ''
  }
  editingPrinter.value = false
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

.printers-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.printer-item {
  padding: 1.5rem;
}

.printer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.printer-header h3 {
  margin: 0;
  color: var(--vt-c-blue-dark);
}

.printer-manufacturer {
  font-size: 0.9rem;
  color: var(--vt-c-gray);
}

.printer-details .detail-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.printer-details p {
  margin: 0;
  color: var(--vt-c-gray);
}

.printer-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
</style>