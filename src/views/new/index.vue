<template>
  <div class="patient-detail">
    <!-- 左半部分：病人信息和视频 -->
    <div class="left-section">
      <div v-if="patient">
        <h2>病人基本信息</h2>
        <div class="info-block">
          <p><strong>姓名:</strong> {{ patient.name || '暂无信息' }}</p>
          <p><strong>年龄:</strong> {{ patient.age || '暂无信息' }}</p>
          <p><strong>性别:</strong> {{ patient.gender ? (patient.gender === 'male' ? '男' : '女') : '暂无信息' }}</p>
          <p><strong>病历:</strong> {{ patient.medical_history || '暂无信息' }}</p>
        </div>
        <div class="video-container">
          <h3>病人视频</h3>
          <video controls>
            <source src="your-video-url.mp4" type="video/mp4">
            您的浏览器不支持视频标签。请下载视频以查看。
          </video>
        </div>
      </div>
      <div v-else>
        <p>正在加载病人信息...</p>
      </div>
    </div>
    
    <!-- 右半部分：AI中医的诊断结果 -->
    <div class="right-section">
      <h2>AI中医诊断结果</h2>
      <div class="diagnosis-block">
        <p>根据AI中医的分析，该病人的症状可能表明他有热邪入侵，建议使用清热解毒的中药进行治疗，如黄连解毒汤。同时，建议密切观察病情变化，如有加重情况，需及时复诊。</p>
      </div>

      <h3>建议</h3>
      <ul class="suggestions-block">
        <li>多喝温水，保持体内水分。</li>
        <li>注意休息，避免过度劳累。</li>
        <li>避免进食辛辣、油腻的食物。</li>
        <li>如症状加重，请及时就医。</li>
      </ul>

      <!-- 分析按钮 -->
      <div class="analysis-button-container">
        <el-button type="primary" @click="analyzePatient">分析</el-button>
      </div>
    </div>
  </div>
</template>


<script>
import { getPatientById as getPatientByIdAPI, updatePatientStatus as updatePatientStatusAPI } from '@/api/patients'; // 假设有一个 updatePatientStatus API

export default {
  data() {
    return {
      patient: null // 初始状态为 null
    };
  },
  created() {
    this.fetchPatientDetail(); // 组件创建时调用方法
  },
  methods: {
    fetchPatientDetail() {
      const id = this.$route.params.id; // 从路由中获取 ID
      if (id) {
        getPatientByIdAPI(id) // 调用 API 获取数据
          .then(response => {
            console.log('API response:', response); // 打印 API 响应
            this.patient = response.patient; // 更新组件状态
          })
          .catch(error => {
            console.error('Error fetching patient details:', error); // 捕获错误
          });
      } else {
        console.error('No patient ID in route parameters');
      }
    },
    
    analyzePatient() {
      const id = this.$route.params.id; // 获取病人的 ID
      if (id) {
        updatePatientStatusAPI(id, '已就诊') // 调用 API 更新病人状态为 '已就诊'
          .then(response => {
            console.log('Patient status updated:', response); // 打印更新结果
            this.fetchPatientDetail(); // 重新获取病人详情，更新页面
          })
          .catch(error => {
            console.error('Error updating patient status:', error); // 捕获错误
          });
      } else {
        console.error('No patient ID in route parameters');
      }
    }
  }
}
</script>

<style scoped>
.patient-detail {
  display: flex;
  height: 100vh;
  background-color: #E8F7FF;
}

.left-section, .right-section {
  flex: 1;
  padding: 20px;
  overflow-y: auto; /* 如果内容超出页面高度，可以滚动 */
}

.left-section {
  background-color: #E8F7FF;
  border-right: 1px solid #dee2e6;
}

.right-section {
  background-color: #E8F7FF;
}

.info-block, .diagnosis-block, .suggestions-block {
  background-color: #ffffff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.video-container {
  margin-top: 20px;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

video {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

/* 分析按钮容器样式 */
.analysis-button-container {
  margin-top: 20px;
  text-align: center;
}
</style>
