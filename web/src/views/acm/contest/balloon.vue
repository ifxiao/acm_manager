<template>
  <div class="app-container">

    <el-table
      v-loading="listLoading"
      :data="list"
      :default-sort="{prop: 'submit_id', order: 'descending'}"
      border
      fit
      highlight-current-row
    >
      <!-- <el-table-column label="序号" width="70" align="center">
        <template slot-scope="scope">
          {{ (page - 1) * limit + scope.$index + 1 }}
        </template>
      </el-table-column> -->

      <el-table-column prop="submit_id" label="提交号" width="100" />

      <el-table-column prop="user_id" label="user_id" width="150" />

      <el-table-column prop="nick" label="nick" width="120"/>

      <el-table-column prop="colour" label="颜色" width="100" />

      <el-table-column prop="ip" label="提交代码ip" width="180" />

      <el-table-column prop="comment" label="ip是否正常" />

      <el-table-column prop="input_time" label="提交时间" />

      <el-table-column prop="index" label="地点" />

      <el-table-column prop="balloon" label="发气球" width="80" >
        <template scope="scope">
          <span v-if="scope.row.balloon=== true">已经发放气球</span>
          <span v-else-if="scope.row.balloon=== false" style="color: red">未发气球</span>
          <span v-else style="color: red">出错了</span>
        </template>  
      </el-table-column>/>

      <el-table-column label="操作" width="300" align="cejnter">
        <template scope="scope">
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="addBalloonById(scope.row.user_id, scope.row.submit_id)"
            >发气球</el-button
          >
          </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-pagination
      :current-page="page"
      :page-size="limit"
      :total="total"
      style="padding: 30px 0; text-align: center"
      layout="total, prev, pager, next, jumper"
      @current-change="getList"
    />
  </div>
</template>
<script>

import balloon from "@/api/acm/balloon";
import { mapGetters } from 'vuex'

export default {
  //写核心代码的位置
  //   data: {

  //   },
  computed: {
    ...mapGetters([
      'token'
    ])
  },
  data() {
    //定义变量和初始值
    return {
      list: null, //条件查询之后接口返回集合
      page: 1, //当前页，默认值为1
      limit: 10, //每页记录数
      total: 0, //总记录数
      balloonQuery: {token:this.token}, //条件封装对象
      listLoading:false,
      intervalTimer:null
    };
  },
  created() {
    //页面渲染之前执行，一般调用methods定义的方法
    this.getList(1)
    this.play()
    // this.getList();

  },
  methods: {
    //创建具体方法
    getList(page = this.page) {
        // this.listLoading = true

        this.page = page
        console.log("test");
        this.balloonQuery.token = this.token
      balloon
        .getballoonListPage(this.page, this.limit, this.balloonQuery)
        .then((response) => {
          //请求成功
          console.log(response)
          if(this.list != response.data.rows){
              this.list = response.data.rows
          }
          this.total = response.data.total;
        //   this.listLoading = false
        })
    },//清空方法
    addBalloonById(user_id, submit_id) {
        console.log(user_id);
        console.log(submit_id);
        this.balloonQuery.token = this.token
        this.balloonQuery.user_id = user_id
        this.balloonQuery.submit_id = submit_id
        balloon
          .addBalloonById(this.balloonQuery)
          .then((response) => {
            this.getList()
          })
    },
    test(){
        console.log(1);
    },
    play(){
        this.intervalTimer = setInterval(this.getList, 10*1000)
        console.log("开始定时任务");
        // this.intervalTimer = setInterval(this.test, 1*1000)
    },
  },
  beforeDestroy(){
      clearInterval(this.intervalTimer)
      console.log("清除定时");
  }
};
</script>