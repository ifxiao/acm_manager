<template>
  <div class="app-container">
    <h3 class="title">请假单</h3>
    <el-form label-width="120px">

      <el-form-item label="请假时间">
        <el-date-picker
            v-model="data.time"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
        </el-date-picker>
      </el-form-item>

      <el-form-item label="请假原因">
        <el-input
            type="textarea"
            :rows="5"
            placeholder="请输入内容"
            v-model="data.info">
        </el-input>
      </el-form-item>

      <el-form-item>
        <el-button
          :disabled="saveBtnDisabled"
          type="primary"
          @click="saveOrUpdate"
          >提交请假单</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import management from "@/api/acm/management";
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters([
      'token'
    ])
  },
  data() {
    return {
      data: {token:this.token},
      saveBtnDisabled: false, //保存按钮是否禁用
      BASE_API: process.env.BASE_API,   //获取dev.env.js里面地址
    };
  },
  methods: {
    saveOrUpdate() {
      this.saveLeave();
    },

    saveLeave() {
        console.log("saveLeave");
        this.data.token = this.token;
        // date.start_time = date.time[0]
        // console.log(this.data.time[0]);
        var a = this.data.time[0];
        console.log(this.data);
        // console.log(a.format("YYYY-MM-DD HH:mm:ss"));
         
      management.addManagement(this.data).then((response) => {

        if(response.Success == true){
          this.$message({
                type: "success",
                message:response.message
            }
          ) 
          //回到列表页面  路由跳转
          this.$router.push({ path: "/management/leave_list" });
        }
        else{
          this.$message({
                type: "false",
                message:response.message
            })
        }
      });
    },
  },
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#111111;
$light_gray:rgb(59, 67, 104);
.title {
    font-size: 26px;
    font-weight: 400;
    color: $light_gray;
    margin: 0px auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
</style>