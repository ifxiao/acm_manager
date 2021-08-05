<template>
  <div class="app-container">
    <el-form label-width="120px">
      <el-form-item label="学号">
        <el-input v-model="member.user_id" />
      </el-form-item>
      
      <!-- <el-form-item label="讲师排序">
        <el-input-number
          v-model="member.sort"
          controls-position="right"
          :min="0"
        />
      </el-form-item> -->

      <el-form-item label="姓名">
        <el-input v-model="member.user_name" />
      </el-form-item>

      <el-form-item label="联系方式">
        <el-input v-model="member.contact"  />
      </el-form-item>

      <el-form-item label="学校">
        <el-input v-model="member.school" :disabled="true" />
      </el-form-item>

      <el-form-item label="年级">
        <el-input v-model="member.grade" />
      </el-form-item>
      <el-form-item label="成员类别">
        <el-input v-model="member.position" :disabled="true" />
      </el-form-item>

      <el-form-item>
        <el-button
          :disabled="saveBtnDisabled"
          type="primary"
          @click="saveOrUpdate"
          >保存</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import member from "@/api/acm/member";
export default {
  data() {
    return {
      member: {},
      saveBtnDisabled: false, //保存按钮是否禁用
      imagecropperShow: false, //上传弹框组件是否显示
      BASE_API: process.env.BASE_API,   //获取dev.env.js里面地址
      imagecropperKey: 0
    };
  },
  created() {
    this.init();
  },
  watch: {
    //监听
    $route(to, from) {
      //路由变化方式，路由发生变化，方法就会执行
      this.init();
    },
  },
  methods: {
    init() {
      if (this.$route.params && this.$route.params.user_id) {
        const user_id = this.$route.params.user_id;
        this.queryMember(user_id);
      } else {
        this.member = {
          school:"黑龙江大学",
          position:"成员"
        };
      }
    },
    saveOrUpdate() {
      //判断修改还是添加
      // if (!this.member.id) {
      //   this.saveMember();
      // } else {
      //   this.updateMember();
      // }
      this.saveMember();
    },

    saveMember() {
      member.addMember(this.member).then((response) => {
        // //提示信息
        // this.$message({
        //   type: "success",
        //   message: "添加成功!",
        // });

        if(response.Success == true){
          this.$message({
            type: "success",
            message:response.message
            }
          ) 
          //回到列表页面  路由跳转
          this.$router.push({ path: "/member/table" });
        }
        else{
          this.$message({
            type: "false",
            message:response.message
            }
          ) 
        }

        
      });
    },
    queryMember(id) {
      member.getMemberInfo(id).then((response) => {
        this.member = response.data.member;
      });
    },
    //关闭上传弹框的方法
    close() {
      //关闭弹框
      this.imagecropperShow = false;
      //上传组件初始化，可以再次上传
      this.imagecropperKey = this.imagecropperKey + 1;
    },
    //上传成功的方法
    cropSuccess(data) {
      this.imagecropperShow = false;
      this.member.avatar = data.url
      //上传组件初始化，可以再次上传
      this.imagecropperKey = this.imagecropperKey + 1;
    }
  },
};
</script>