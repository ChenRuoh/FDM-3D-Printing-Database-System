<template>
  <div class="matching-page">
    <div class="glass-card page-header">
      <h1>参数智能匹配</h1>
    </div>

    <div class="glass-card matching-form">
      <h3>选择匹配条件</h3>
      <form @submit.prevent="performMatching">
        <div class="form-row">
          <div class="form-group">
            <label for="material">材料类型</label>
            <select id="material" v-model="matchingRequest.material_id">
              <option value="">请选择材料</option>
              <option v-for="material in materials" :key="material.id" :value="material.id">
                {{ material.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="printer">打印机型号</label>
            <select id="printer" v-model="matchingRequest.printer_id">
              <option value="">请选择打印机</option>
              <option v-for="printer in printers" :key="printer.id" :value="printer.id">
                {{ printer.name }}
              </option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="layerHeight">期望层高 (mm)</label>
            <input type="number" id="layerHeight" v-model.number="matchingRequest.layer_height" step="0.01" placeholder="可选">
          </div>
          <div class="form-group">
            <label for="infillDensity">期望填充密度 (%)</label>
            <input type="number" id="infillDensity" v-model.number="matchingRequest.infill_density" placeholder="可选">
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="printSpeed">期望打印速度 (mm/s)</label>
            <input type="number" id="printSpeed" v-model.number="matchingRequest.print_speed" placeholder="可选">
          </div>
        </div>
        
        <button type="submit" class="btn-primary glass-card" :disabled="isMatching">
          {{ isMatching ? '匹配中...' : '开始匹配' }}
        </button>
      </form>
    </div>

    <!-- 匹配结果显示 -->
    <div v-if="matchingResults.length > 0" class="results-section">
      <div class="glass-card results-header">
        <h3>匹配结果</h3>
        <p>找到 {{ matchingResults.length }} 个匹配的参数组合</p>
      </div>
      
      <div class="results-list">
        <div 
          v-for="(result, index) in matchingResults" 
          :key="index" 
          class="glass-card result-item slide-fade-enter-active"
        >
          <div class="result-header">
            <h4>{{ result.parameter.name }}</h4>
            <div class="score-badge">匹配度: {{ Math.round(result.score * 100) }}%</div>
          </div>
          
          <div class="result-details">
            <div class="detail-row">
              <span>层高: {{ result.parameter.layer_height }}mm</span>
              <span>打印速度: {{ result.parameter.print_speed }}mm/s</span>
              <span>填充密度: {{ result.parameter.infill_density }}%</span>
            </div>
            <div class="detail-row">
              <span>打印温度: {{ result.parameter.print_temperature }}°C</span>
              <span>热床温度: {{ result.parameter.bed_temperature }}°C</span>
            </div>
            <p class="reason"><strong>推荐理由:</strong> {{ result.reason }}</p>
          </div>
          
          <div class="result-actions">
            <button class="btn-primary glass-card">使用此参数</button>
            <button class="btn-secondary glass-card">查看详情</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 模拟数据
const materials = ref([
  { id: 1, name: 'PLA' },
  { id: 2, name: 'ABS' },
  { id: 3, name: 'PETG' },
  { id: 4, name: 'TPU' }
])

const printers = ref([
  { id: 1, name: 'Ender 3' },
  { id: 2, name: 'Prusa MK3S' },
  { id: 3, name: 'Creality CR-10' },
  { id: 4, name: 'Anycubic Mega' }
])

const matchingRequest = ref({
  material_id: null as number | null,
  printer_id: null as number | null,
  layer_height: null as number | null,
  infill_density: null as number | null,
  print_speed: null as number | null
})

const matchingResults = ref<any[]>([])
const isMatching = ref(false)

const performMatching = async () => {
  isMatching.value = true
  
  // 模拟API调用延迟
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  // 模拟匹配结果
  matchingResults.value = [
    {
      parameter: {
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
      score: 0.95,
      reason: '完美匹配所选材料和打印机配置'
    },
    {
      parameter: {
        id: 5,
        name: 'PLA快速参数',
        layer_height: 0.25,
        print_speed: 80,
        infill_density: 15,
        print_temperature: 205,
        bed_temperature: 60,
        travel_speed: 150,
        retraction_distance: 1,
        retraction_speed: 45,
        description: '适用于快速打印的PLA参数'
      },
      score: 0.87,
      reason: '适合快速打印，质量略有降低'
    },
    {
      parameter: {
        id: 8,
        name: 'PLA精细参数',
        layer_height: 0.1,
        print_speed: 40,
        infill_density: 20,
        print_temperature: 195,
        bed_temperature: 60,
        travel_speed: 100,
        retraction_distance: 1,
        retraction_speed: 40,
        description: '适用于高精度打印的PLA参数'
      },
      score: 0.82,
      reason: '适合精细模型，打印时间较长'
    }
  ]
  
  isMatching.value = false
}
</script>

<style scoped>
.page-header {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.matching-form {
  padding: 1.5rem;
  margin-bottom: 2rem;
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
.form-group select {
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.3);
}

.btn-primary {
  background-color: var(--vt-c-blue);
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-secondary {
  background-color: var(--vt-c-green);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.results-header {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.results-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.result-item {
  padding: 1.5rem;
  animation: fadeInUp 0.5s ease forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

.score-badge {
  background-color: var(--vt-c-green);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
}

.result-details .detail-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
}

.reason {
  margin: 1rem 0;
  padding: 0.8rem;
  background: rgba(64, 158, 255, 0.1);
  border-radius: 4px;
  font-style: italic;
}

.result-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
</style>