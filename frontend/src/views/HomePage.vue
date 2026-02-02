<template>
  <div class="home">
    <div class="glass-card hero-section">
      <h1>欢迎使用FDM 3D打印工艺参数数据库与匹配系统</h1>
      <p>专业的FDM 3D打印参数管理与智能匹配平台</p>
      <div class="stats-grid">
        <div class="stat-item glass-card">
          <h3>150+</h3>
          <p>参数模板</p>
        </div>
        <div class="stat-item glass-card">
          <h3>50+</h3>
          <p>材料类型</p>
        </div>
        <div class="stat-item glass-card">
          <h3>30+</h3>
          <p>打印机型号</p>
        </div>
      </div>
    </div>

    <div class="glass-card features-section">
      <h2>系统特色功能</h2>
      <div class="features-grid">
        <div class="feature-item glass-card">
          <h3>智能参数匹配</h3>
          <p>根据您的材料和打印机自动推荐最佳参数组合</p>
        </div>
        <div class="feature-item glass-card">
          <h3>参数库管理</h3>
          <p>轻松管理、编辑和分享您的打印参数</p>
        </div>
        <div class="feature-item glass-card">
          <h3>数据可视化</h3>
          <p>直观展示参数使用情况和打印成功率</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 首页逻辑
</script>

<style scoped>
.hero-section {
  text-align: center;
  padding: 2rem;
  margin-bottom: 2rem;
}

.hero-section h1 {
  color: var(--vt-c-blue-dark);
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
}

.features-section {
  padding: 2rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-item {
  padding: 1.5rem;
  text-align: center;
}
</style>