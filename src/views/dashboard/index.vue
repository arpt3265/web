<template>
  <div class="dashboard-container">
    <div class="header">
      <h1>欢迎医生</h1>
      <div class="search-and-button">
        <!-- 搜索框 -->
        <el-input
          v-model="searchName"
          placeholder="请输入名字"
          suffix-icon="el-icon-search"
          @input="searchPatients"
          class="custom-search-input"
        ></el-input>

        <!-- 添加病人按钮 -->
        <el-button class="green-button add-patient-button" @click="showAddPatientDialog">添加病人</el-button>
      </div>
    </div>

    <!-- 添加病人对话框 -->
    <el-dialog
      title="添加病人"
      :visible.sync="isAddPatientDialogVisible"
      @close="resetAddPatientForm"
    >
      <el-form :model="newPatient" ref="addPatientForm">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="newPatient.name" />
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input v-model="newPatient.age" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="newPatient.gender">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>
        <el-form-item label="病历" prop="medical_history">
          <el-input type="textarea" v-model="newPatient.medical_history" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="newPatient.email" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button class="red-button" @click="isAddPatientDialogVisible = false">取消</el-button>
        <el-button class="green-button" @click="addPatient">确定</el-button>
      </div>
    </el-dialog>

    <!-- 编辑病人对话框 -->
    <el-dialog
      title="编辑病人"
      :visible.sync="isEditPatientDialogVisible"
      @close="resetEditPatientForm"
    >
      <el-form :model="editPatient" ref="editPatientForm">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="editPatient.name" />
        </el-form-item>
        <el-form-item label="年龄" prop="age">
          <el-input v-model="editPatient.age" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="editPatient.gender">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>
        <el-form-item label="病历" prop="medical_history">
          <el-input type="textarea" v-model="editPatient.medical_history" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editPatient.email" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button class="red-button" @click="isEditPatientDialogVisible = false">取消</el-button>
        <el-button class="green-button" @click="updatePatient">确定</el-button>
      </div>
    </el-dialog>

    <!-- 病人列表 -->
    <div class="patient-cards">
      <div class="patient-card-wrapper" v-for="patient in patients" :key="patient.id"  @click="goToPatientDetails(patient.id)">
        <el-card class="patient-card" :style="getCardStyle(patient)">
          <div class="card-header">
            <img :src="patient.gender === 'male' ? maleAvatar : femaleAvatar" alt="头像" class="patient-avatar" />
            <h3><strong>姓名:</strong>{{ patient.name }}</h3>
          </div>
          <div class="card-body">
            <p><strong>年龄:</strong> {{ patient.age }}</p>
            <p><strong>性别:</strong> {{ patient.gender === 'male' ? '男' : '女' }}</p>
            <p><strong>病历:</strong> {{ patient.medical_history }}</p>
            <p><strong>邮箱:</strong> {{ patient.email }}</p>
          </div>
          <div class="card-footer">
            <el-button class="blue-button" @click.stop="showEditPatientDialog(patient)" size="small">编辑</el-button>
            <el-button class="red-button" @click.stop="deletePatient(patient.id)" size="small">删除</el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { searchPatients as searchPatientsAPI ,getPatients as getPatientsAPI, addPatient as addPatientAPI, updatePatient as updatePatientAPI, deletePatient as deletePatientAPI } from '@/api/patients'
import { mapState } from 'vuex'
import { Message } from 'element-ui';
import { MessageBox } from 'element-ui';
import maleAvatar from '@/assets/avatar/male-avatar.png'  // Import male avatar
import femaleAvatar from '@/assets/avatar/female-avatar.png'  // Import female avatar


export default {
  data() {
    return {
      isAddPatientDialogVisible: false,
      isEditPatientDialogVisible: false,
      newPatient: {
        name: '',
        age: '',
        gender: '',
        medical_history: '',
        email: ''
      },
      editPatient: {
        id: null,
        name: '',
        age: '',
        gender: '',
        medical_history: '',
        email: ''
      },
      patients: [],
      searchName: '', // 搜索框的值
      maleAvatar,  // Add male avatar to data
      femaleAvatar  // Add female avatar to data
    }
  },

  computed: {
    ...mapState({
      doctor_id: state => state.user.doctor_id
    })
  },

  methods: {
    showAddPatientDialog() {
      this.isAddPatientDialogVisible = true
    },
    resetAddPatientForm() {
      this.newPatient = {
        name: '',
        age: '',
        gender: '',
        medical_history: '',
        email: ''
      }
    },
    addPatient() {
      this.$refs.addPatientForm.validate((valid) => {
        if (valid) {
          addPatientAPI({ ...this.newPatient, doctor_id: this.doctor_id })
            .then(response => {
              if (response.code === 'success') {
                this.isAddPatientDialogVisible = false
                this.resetAddPatientForm()
                this.fetchPatients()
                Message.success('成功添加病人');
              } else {
                console.error('Unexpected response code:', response.code)
                Message.error(response.message || 'Error');
              }
            })
            .catch(error => {
              Message.error('Failed to add patient. Please check the console for details.');
            })
        } else {
          Message.warning('Form validation failed. Please check the input fields.');
        }
      })
    },
    showEditPatientDialog(patient) {
      this.editPatient = { ...patient }
      this.isEditPatientDialogVisible = true
    },
    resetEditPatientForm() {
      this.editPatient = {
        id: null,
        name: '',
        age: '',
        gender: '',
        medical_history: '',
        email: ''
      }
    },
    updatePatient() {
      this.$refs.editPatientForm.validate((valid) => {
        if (valid) {
          updatePatientAPI(this.editPatient.id, this.editPatient).then(() => {
            this.isEditPatientDialogVisible = false
            this.resetEditPatientForm()
            this.fetchPatients()
          }).catch((error) => {
            console.error(error)
          })
        }
      })
    },
    deletePatient(id) {
      MessageBox.confirm('你是否确定要删除这位病人的信息?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: '提示',
      }).then(() => {
        // 用户确认删除操作后执行
        deletePatientAPI(id).then(() => {
          this.fetchPatients();
        }).catch((error) => {
          console.error('Error deleting patient:', error.response ? error.response.data : error.message);
        });
      }).catch(() => {
        // 用户取消删除操作
        console.log('Delete operation cancelled');
      });
    },
    searchPatients() {
      if (!this.doctor_id || !this.searchName.trim()) {
        this.fetchPatients();
        return;
      }
    


    // 使用 this.doctor_id 获取 doctor_id
    searchPatientsAPI(this.doctor_id, this.searchName).then(response => {
         console.log('API response:', response.patients);
      if (response && response.patients) {
        this.patients = response.patients;
      } else {
        this.patients = [];
        Message.error('没找到此病人');
      }
    }).catch(error => {
      //console.error('Error searching patients:', error);
      //Message.error('Failed to search patients. Please check the console for details.');
    });
    },

    fetchPatients() {
      if (!this.doctor_id) {
        this.$message.error('Doctor ID is not available.');
        return;
      }

      getPatientsAPI(this.doctor_id).then(response => {
        if (response && response.patients) {
          this.patients = response.patients;
        } else {
          this.patients = []; // 确保清空当前病人列表
          console.error('No data in response:', response);
        }
      }).catch(error => {
        console.error('Error fetching patients:', error);
      })
    },

    async goToPatientDetails(id) {
    console.log('Card clicked, patient ID:', id);
    if (id) {
      try {
        await this.$router.push({ name: 'patient-details', params: { id } });
        console.log('Navigation successful');
      } catch (error) {
        console.error('Navigation error:', error);
      }
    } else {
      console.error('No patient ID provided');
    }
  },

    getCardStyle(patient) {
      return {
        backgroundColor: patient.status === '已就诊' ? '#67e2a2' : '#eae8e8bd',
        color: 'white', // 确保文本在灰色背景上可读
      };
    },
  },

  


  watch: {
    doctor_id(newValue) {
      if (newValue) {
        this.fetchPatients();
      }
    }
  },

  mounted() {
  this.$nextTick(() => {
    console.log('Doctor ID at creation:', this.doctor_id);
    if (this.doctor_id) {
      this.fetchPatients();
    } else {
      console.warn('Doctor ID is not available at the time of mounting.');
    }
  });
  }
}
</script>




<style scoped>
/* 确保背景颜色覆盖整个页面 */
.dashboard-container {
  background-color: #E8F7FF; /* 浅蓝色背景 */
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 确保页面内容占满视窗高度 */
}


/* 为内容块添加分隔线 */
.header, .dashboard-overview {
  padding-bottom: 20px;
  margin-bottom: 0px;
}

/* 搜索框和按钮的容器 */
.search-and-button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.custom-search-input {
  width: 400px; /* 控制搜索框的宽度 */
  border-radius: 8px; /* 设置圆角 */
  border: 2px solid #007bff; /* 边框颜色 */
  padding: 10px; /* 内边距 */
  background-color: #f0faff; /* 背景颜色 */
  position: relative;
}

.custom-search-input .el-input__inner {
  border-radius: inherit; /* 确保内部输入框的圆角与外部匹配 */
  height: 10px; /* 控制搜索框的高度 */
}

.custom-search-input .el-input__suffix {
  color: #007bff; /* 图标颜色 */
  position: absolute;
  right: 90px; /* 图标距离右侧的距离 */
  top: 50%; /* 图标相对于输入框垂直居中 */
  transform: translateY(-50%); /* 垂直居中 */
  pointer-events: none; /* 确保点击图标时不会影响输入框的焦点 */
}

.custom-search-input:hover .el-input__inner {
  border-color: #0056b3; /* 悬停时的边框颜色 */
}

.custom-search-input .el-input__inner:focus {
  border-color: #0056b3; /* 聚焦时的边框颜色 */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* 聚焦时的阴影效果 */
}

/* 添加病人按钮样式 */
.add-patient-button {
  margin-left: auto; /* 按钮靠右 */
}

/* 为表单添加卡片样式 */
.el-dialog__body {
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.el-form {
  background-color: #fff; /* 卡片背景颜色 */
  border-radius: 10px; /* 圆角边框 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 卡片阴影 */
  padding: 20px; /* 内边距 */
}

.el-form-item {
  margin-bottom: 15px; /* 表单项底部间距 */
}

/* 修改输入框的样式 */
.el-input {
  border-radius: 5px; /* 圆角 */
  border: 1px solid #D3DCE6;
  padding: 10px;
  background-color: #F5F7FA;
}

/* 按钮样式 */
.el-button {
  color: #fff;
  border-radius: 5px;
  padding: 10px 20px;
  border: none;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* 绿色按钮 */
.green-button {
  background-color: #28a745;
}

.green-button:hover {
  background-color: #218838;
}

/* 红色按钮 */
.red-button {
  background-color: #dc3545;
}

.red-button:hover {
  background-color: #c82333;
}

/* 蓝色按钮 */
.blue-button {
  background-color: #007bff;
}

.blue-button:hover {
  background-color: #0069d9;
}

/* 修改标题样式 */
.header h1 {
  font-size: 28px;
  color: #4A4A4A;
  font-weight: bold;
}



/* 卡片容器样式 */
.patient-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
}

/* 单个病人卡片样式 */
.patient-card {
  width: 100%;
  max-width: 300px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 卡片阴影 */
  transition: background-color 0.3s; /* 卡片背景颜色 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%; /* 确保卡片填满容器 */
}

/* 卡片标题样式 */
.card-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #dcdcdc; /* 分隔线 */
}

/* 卡片标题样式 */
.card-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.patient-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}



/* 卡片内容样式 */
.card-body p {
  margin: 10px 0;
  font-size: 14px;
  color: #555;
}

/* 卡片底部按钮样式 */
.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
</style>
