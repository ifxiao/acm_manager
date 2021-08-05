<template>
  <div class="app-container">
    <el-form label-width="120px">
      <el-form-item label="比赛名">
        <el-input v-model="data.contest_name" />
      </el-form-item>

      <!-- <el-form-item label="刷题平台">
        <el-input v-model="data.contact"  />
      </el-form-item> -->

      <el-form-item label="比赛等级">
        <el-select v-model="data.contest_level" placeholder="比赛等级">
          <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="年份">
        <el-input v-model="data.years"  />
      </el-form-item>

      <el-form-item label="队伍数量">
        <el-input v-model="data.team_count"  />
      </el-form-item>

      <el-form-item label="比赛网址">
        <el-input v-model="data.contest_url"  />
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
import contest from "@/api/acm/contest";
export default {
  data() {
    return {
      data: {},
      flag:false,
      saveBtnDisabled: false, //保存按钮是否禁用
      imagecropperShow: false, //上传弹框组件是否显示
      BASE_API: process.env.BASE_API,   //获取dev.env.js里面地址
      imagecropperKey: 0,
      Fid:null,
      options: [
          {
              value: 1,
              label: "校级" 
          },
          {
              value: 2,
              label: "省级" 
          },
          {
              value: 3,
              label: "国家级" 
          },
      ]
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
      this.Fid = this.$route.params.id;
      if (this.$route.params && this.$route.params.id) {
        // console.log("this is test");
        const id = this.$route.params.id;
        this.queryContest(id);
      }
    },
    saveOrUpdate() {
      //判断修改还是添加
      // if (!this.Contest.id) {
      //   this.saveMember();
      // } else {
      //   this.updateMember();
      // }
      this.saveContest();
    },

    saveContest() {
      this.data.Fid = this.Fid;
      contest.addContest(this.data).then((response) => {
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
          this.$router.push({ path: "/contest/list" });
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
        this.data = response.data.contest;
        console.log(this.data);
        // console.log(this.options);
      });
    },
  },
};
</script>