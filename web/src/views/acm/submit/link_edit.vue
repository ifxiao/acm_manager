<template>
  <div class="app-container">
    <el-form label-width="120px">
      <el-form-item label="学号">
        <el-input v-model="data.user_id" :disabled="flag"/>
      </el-form-item>
      

      <el-form-item label="姓名">
        <el-input v-model="data.user_name" :disabled="flag" />
      </el-form-item>

      <!-- <el-form-item label="刷题平台">
        <el-input v-model="data.contact"  />
      </el-form-item> -->
      <el-form-item label="平台">
        <el-select v-model="data.platform_id" placeholder="平台">
          <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="平台id">
        <el-input v-model="data.link_id"  />
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
import submit from "@/api/acm/submit";
export default {
  data() {
    return {
      data: {},
      flag:false,
      saveBtnDisabled: false, //保存按钮是否禁用
      imagecropperShow: false, //上传弹框组件是否显示
      BASE_API: process.env.BASE_API,   //获取dev.env.js里面地址
      imagecropperKey: 0,
      options: null,
      Fid:null
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
      this.queryPlatform()
      this.flag = false;
      this.Fid = this.$route.params.link;
      if (this.$route.params && this.$route.params.link) {
        const id = this.$route.params.link;
        this.queryLink(id);
      }
    },
    saveOrUpdate() {
      //判断修改还是添加
      // if (!this.link.id) {
      //   this.saveMember();
      // } else {
      //   this.updateMember();
      // }
      this.saveLink();
    },

    saveLink() {
      this.data.Fid = this.Fid;
      submit.addLink(this.data).then((response) => {
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
          this.$router.push({ path: "/submit/link_list" });
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
    queryLink(id) {
      submit.getLinkInfo(id).then((response) => {
        this.flag = true;
        this.data = response.data.link;
        // console.log(this.data);
        // console.log(this.options);
      });
    },
    queryPlatform(){
      submit.getPlatform().then((response) =>{
        this.options = response.data.options;
      });
    }
  },
};
</script>