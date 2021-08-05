<template>

    <div class="app-container">
      <!-- 查询表单-->
      <h3 class="title">{{contest_name}}</h3>
    <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="Query.team_id" placeholder="队伍号"/>
      </el-form-item>

      <el-button type="primary" icon="el-icon-search" @click="queryTeam()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

  <div class="app-container">
    <el-form label-width="120px">
      
      <el-form-item label="年级">
        <el-input v-model="data.grade" :disabled="true"/>
      </el-form-item>
      
      <el-form-item label="队名">
        <el-input v-model="data.team_name" :disabled="true"/>
      </el-form-item>

      <el-form-item label="队长学号">
        <el-input v-model="data.member1" :disabled="true"/>
      </el-form-item>

      <el-form-item label="队长姓名">
        <el-input v-model="data.member1_name" :disabled="true" />
      </el-form-item>

      <el-form-item label="队员1学号">
        <el-input v-model="data.member2" :disabled="true"/>
      </el-form-item>

      <el-form-item label="队员1姓名">
        <el-input v-model="data.member2_name" :disabled="true" />
      </el-form-item>

      <el-form-item label="队员2学号">
        <el-input v-model="data.member3" :disabled="true" />
      </el-form-item>

      <el-form-item label="队员2姓名">
        <el-input v-model="data.member3_name" :disabled="true" />
      </el-form-item>

      <el-form-item label="教练">
        <el-input v-model="data.coach" :disabled="true" />
      </el-form-item>

      <el-form-item>
        <el-button
          :disabled="saveBtnDisabled"
          type="primary"
          v-text="save_text"
          @click="saveTeam"
          >
        </el-button>
      </el-form-item>
    </el-form>
  </div>
   </div>
</template>

<script>
import contest from "@/api/acm/contest";
import team from "@/api/acm/team";
export default {
  data() {
    return {
      data: {},
      Query:{},
      flag:'none',
      saveBtnDisabled: false, //保存按钮是否禁用
      imagecropperShow: false, //上传弹框组件是否显示
      BASE_API: process.env.BASE_API,   //获取dev.env.js里面地址
      imagecropperKey: 0,
      options: null,
      save_text: "添加该队伍",
      contest_id:null,
      contest_name:null
    };
  },
  watch: {
    //监听
    $route(to, from) {
      //路由变化方式，路由发生变化，方法就会执行
      this.init();
    },
  },
  created() {
    this.init();
  },

  methods: {
    init() {
      this.flag = false;
      if (this.$route.params && this.$route.params.id) {
        console.log("this is test");
        const id = this.$route.params.id;
        this.contest_id = id;
        this.queryContest(id);
      }
    },
    getTeam() {
      this.flag = false;
        const id = this.Query.team_id;
        this.queryTeam(id);
    },
    saveTeam() {
      console.log("saveTeam");
        console.log(this.contest_id, this.data.team_id);
        const data = {
            contest_id:this.contest_id,
            team_id:this.data.team_id
        }
        contest.saveTeam(data).then((response) => {
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
          this.$router.push({ path: '/contest/team_list/' + this.contest_id });
        }
        else{
          this.$message({
                type: "false",
                message:response.message
            })
        }
      });
    },
    queryContest(id) {
      console.log("queryLint(id)");
      contest.getcontestInfo(id).then((response) => {
        this.flag = true;
        this.contest_name = response.data.contest.contest_name;
        // console.log(this.data);
        // console.log(this.options);
      });
    },
    queryTeam() {
        if (typeof(this.Query.team_id) == "undefined"){
            this.$message({
                type: "false",
                message:"队伍列表不可为空"
            })
        }
    // console.log("fasdfasdfdsafasdf", this.Query.team_id);
      const id = this.Query.team_id;
      team.getTeamInfo(id).then((response) => {
        this.data = response.data.team;
        console.log(this.data);
      });
    }
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