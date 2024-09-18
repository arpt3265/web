<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <!-- 第一列: ID -->
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>

      <!-- 第二列: Patient ID -->
      <el-table-column label="Patient ID" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.patient_id }}
        </template>
      </el-table-column>

      <!-- 第三列: Description -->
      <el-table-column label="Description">
        <template slot-scope="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>

      <!-- 第四列: Suggestion -->
      <el-table-column label="Suggestion">
        <template slot-scope="scope">
          {{ scope.row.suggestion }}
        </template>
      </el-table-column>

      <!-- 新增: 第六列: Video Path -->
    <el-table-column label="Video Path" width="200" align="center">
      <template slot-scope="scope">
        <!-- 直接显示 video 字段的路径 -->
        <span>{{ scope.row.video || '暂无视频路径' }}</span>
      </template>
    </el-table-column>

      <!-- 第六列: Date -->
      <el-table-column align="center" prop="date" label="Date" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.date }}</span>
        </template>
      </el-table-column>

      <!-- 第七列: Status -->
      <el-table-column class-name="status-col" label="Status" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getDiagnoses } from '@/api/table'
import { getPatientById } from '@/api/patients'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        active: 'success',
        inactive: 'warning',
        archived: 'danger'
      }
      return statusMap[status] || 'info'
    }
  },
  data() {
    return {
      list: [],
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
  async fetchData() {
    this.listLoading = true
    try {
      const response = await getDiagnoses()
      const diagnoses = response.diagnoses
      
      // 遍历每个诊断，获取对应患者的 status
      const diagnosesWithStatus = await Promise.all(diagnoses.map(async (diagnosis) => {
        // 判断 patient_id 是否为空
        if (diagnosis.patient_id) {
          const patientResponse = await getPatientById(diagnosis.patient_id)
          diagnosis.status = patientResponse.patient.status  // 添加 status 字段
        } else {
          // 如果 patient_id 为空，则设置 status 为 "未就诊"
          diagnosis.status = "未就诊"
        }
        return diagnosis
      }))
      
      this.list = diagnosesWithStatus
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      this.listLoading = false
    }
  }
}
}
</script>

<style scoped>
.app-container {
  background-color: #E8F7FF; /* 页面背景颜色 */
  min-height: 100vh; /* 确保页面高度填充整个视口 */
  padding: 20px; /* 页面内边距 */
}


/* 自定义表格样式 */
.custom-table {
  background-color: #658ea4; /* 背景颜色 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  margin-top: 0px; /* 顶部间距 */
}

/* 修改表格单元格样式 */
.custom-table .el-table th,
.custom-table .el-table td {
  font-size: 16px; /* 字体大小 */
  color: #333; /* 文本颜色 */
}

/* 调整表头样式 */
.custom-table .el-table th {
  background-color: #010101; /* 表头背景色 */
  font-weight: bold; /* 加粗表头文本 */
}

/* 调整行的间距和边框 */
.custom-table .el-table td {
  padding: 12px; /* 单元格内边距 */
  border-bottom: 1px solid #d52828; /* 单元格底部边框 */
}
</style>