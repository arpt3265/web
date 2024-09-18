<template>
  <div class="register-container">
    <div class="title-container">
      <h3 class="title">用户注册</h3>
    </div>

    <el-form
      ref="ruleForm"
      :model="ruleForm"
      :rules="rules"
      label-width="100px"
      autocomplete="off"
      :hide-required-asterisk="true"
      size="medium"
      class="register-form"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="ruleForm.username"
          placeholder="请输入用户名"
          name="username"
          type="text"
        />
      </el-form-item>

      <el-form-item label="密码" prop="password">
        <el-input
          v-model="ruleForm.password"
          type="password"
          placeholder="请输入密码"
          name="password"
        />
      </el-form-item>

      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input
          v-model="ruleForm.confirmPassword"
          type="password"
          placeholder="请确认密码"
          name="confirmPassword"
        />
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          style="width: 100%;"
          @click="register"
        >注册</el-button>
      </el-form-item>

      <p class="tips">
        <router-link to="/login">已有账号？立即登录</router-link>
      </p>
    </el-form>

    <div class="error">{{ error }}</div>
  </div>
</template>

<style lang="scss">
/* 基础背景色和光标颜色 */
$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

/* 修复 input 的背景色和光标颜色 */
@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .register-container .el-input input {
    color: $cursor;
  }
}

/* 重置 Element-UI 样式 */
.register-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 95%;

    input {
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      -webkit-appearance: none;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    label {
      font-style: normal;
      font-size: 12px;
      color: $light_gray;
    }
  }

  .el-button {
    width: 100%;
    margin-top: 20px;
  }

  .error {
    color: red;
    text-align: center;
    margin-top: 20px;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.register-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .register-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 60px 35px;
    margin: 0 auto;
    overflow: hidden;
  }

  .title-container {
    text-align: center;
    margin-bottom: 40px;

    .title {
      font-size: 26px;
      color: $light_gray;
      font-weight: bold;
    }
  }

  .tips {
    font-size: 14px;
    color: $light_gray;
    text-align: center;
    margin-top: 10px;

    a {
      color: $dark_gray;
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>

<style scoped>
/* 修改验证器样式 */
::v-deep .el-form-item.is-error .el-input__inner {
  border-color: #889aa4;
}
::v-deep .el-form-item.is-error .el-input__validateIcon {
  color: #889aa4;
}
::v-deep .el-form-item__error {
  color: #e6a23c;
}
</style>



<script>
import { register } from '@/api/register' // 确保导入 register API 函数

export default {
  name: 'Register',
  data() {
    return {
      error: '',
      ruleForm: {
        username: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { type: 'string', message: '用户名必须是字符串', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          {
            min: 6,
            message: '密码长度不能少于 6 位',
            trigger: 'blur'
          }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value === '') {
                callback(new Error('请再次输入密码'))
              } else if (value !== this.ruleForm.password) {
                callback(new Error('两次输入密码不一致'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    register() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          const user = {
            username: this.ruleForm.username,
            password: this.ruleForm.password // 不进行加密，直接使用明文密码
          }
          register(user).then(res => {
            console.log(res)
            this.$message({
              showClose: true,
              message: '注册成功，正在跳转到登录界面...',
              type: 'success'
            })
            setTimeout(() => {
              this.$router.push('/login')
            }, 2000)
          }).catch(err => {
            console.log(err.response.data.message)
            this.error = err.response.data.message || '注册失败'
          })
        }
      })
    }
  }
}
</script>
