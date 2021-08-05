<template>
  <div class="app-container">
    <el-form label-width="120px">
      
      <el-form-item label="年级">
        <el-input v-model="data.grade"/>
      </el-form-item>
      
      <el-form-item label="队名">
        <el-input v-model="data.team_name" />
      </el-form-item>

      <el-form-item label="队长学号">
        <el-input v-model="data.member1" />
      </el-form-item>

      <el-form-item label="队长姓名">
        <el-input v-model="data.member1_name" :disabled="true" />
      </el-form-item>

      <el-form-item label="队员1学号">
        <el-input v-model="data.member2" />
      </el-form-item>

      <el-form-item label="队员1姓名">
        <el-input v-model="data.member2_name" :disabled="true" />
      </el-form-item>

      <el-form-item label="队员2学号">
        <el-input v-model="data.member3" />
      </el-form-item>

      <el-form-item label="队员2姓名">
        <el-input v-model="data.member3_name" :disabled="true" />
      </el-form-item>

      <el-form-item label="教练">
        <el-input v-model="data.coach"  />
      </el-form-item>

      <el-form-item>
        <el-button
    z      :disabled="saveBtnDisabled"
          type="primary"
          v-text="save_text"
          @click="saveOrUpdate"
          >
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import team from "@/api/acm/team";
export default {
  data() {
    return {
      data: {},
      flag:'none',
      saveBtnDisabled: false, //保存按钮是否禁用
      imagecropperShow: false, //上传弹框组件是否显示
      BASE_API: process.env.BASE_API,   //获取dev.env.js里面地址
      imagecropperKey: 0,
      options: null,
      save_text: "校验"
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
      this.flag = false;
      this.save_text = "校验成员"
      if (this.$route.params && this.$route.params.team_id) {
        const id = this.$route.params.team_id;
        this.data.team_id = id;
        this.queryTeam(id);
        
      }
    },
    saveOrUpdate() {
      //判断修改还是添加
      // if (!this.link.id) {
      //   this.saveMember();
      // } else {
      //   this.updateMember();
      // }
      if(this.flag == false){
        this.check_member()
      }
      else{this.saveTeam();}
      
    },

    saveTeam() {
      team.addTeam(this.data).then((response) => {
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
          this.$router.push({ path: "/team/team_list" });
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
    check_member(){
      team.checkMember(this.data).then((response) => {
        this.flag = false;
        this.save_text = "校验成员"
        this.data.member1_name = response.data.member.member1_name;
        this.data.member2_name = response.data.member.member2_name;
        this.data.member3_name = response.data.member.member3_name;
        if (response.Success == true){
          this.flag = true;
          this.save_text = "提交"
        }
        // console.log(this.data);
      });
    },
    queryTeam(id) {
      team.getTeamInfo(id).then((response) => {
        this.data = response.data.team;
        console.log(this.data);
      });
    }
  },
};
</script>