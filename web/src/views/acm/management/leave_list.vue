
<template>
    
  <div class="app-container">
      <!-- 查询表单-->
      
      <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="Query.user_id" placeholder="学号"/>
      </el-form-item>

      <el-button type="primary" icon="el-icon-search" @click="getList()">查询</el-button>
      <el-button type="default" @click="resetData()">清空</el-button>
    </el-form>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="数据加载中"
      :default-sort="{prop: 'score', order: 'descending'}"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="序号" width="50" align="center">
        <template slot-scope="scope">
          {{ (page - 1) * limit + scope.$index + 1 }}
        </template>
      </el-table-column>

      <el-table-column prop="id" label="请假单id" width="70" />

      <el-table-column prop="user_id" label="请假人学号" width="70" />

      <el-table-column prop="user_name" label="姓名" width = "100" />

      <el-table-column prop="info" label="请假原因" width="100" />

      <el-table-column prop="start_time" label="起始时间" width="200" />

      <el-table-column prop="end_time" label="结束时间" width="200" />

      <el-table-column prop="status" label="状态" />
      
      <el-table-column label="操作" width="400" align="cejnter">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            icon="el-icon-edit"
            @click="update(true, scope.row.id)"
            >同意</el-button>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="update(false, scope.row.id)"
            >驳回</el-button>
        </template>
      </el-table-column>

    </el-table>
    <!-- 分页 -->
    <el-pagination
      :current-page="page"
      :page-size="limit"
      :page-sizes = "[10, 50, 500]"
      :total="total"
      style="padding: 30px 0; text-align: center"
      layout="total, sizes, prev, pager, next, jumper"
      @current-change="getList"
      @size-change="handleSizeChange"
    />
  </div>
</template>
<script>

import management from "@/api/acm/management";
import { mapGetters } from 'vuex'


export default {
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
      Query: {token:this.token}, //条件封装对象
      listLoading:false,
      data: {token:this.token}
    };
  },
  created() {
    //页面渲染之前执行，一般调用methods定义的方法

    this.getList();
  },
  methods: {
    //创建具体方法
    handleSizeChange(val) {
        this.limit = val;
        this.getList();
    },
    getList(page = 1) {
        this.page = page
        this.listLoading = true
        this.Query.token = this.token
      management
        .getLeaveListPage(this.page, this.limit, this.Query)
        .then((response) => {
          this.list = response.data.rows;
          this.total = response.data.total;
          this.listLoading = false;
        })
    },//清空方法
    resetData() {
        //表单输入项数据清空
        this.linkQuery = {}

        //查询所有数据
        this.getList()
    },
    update(flg, id){
      this.data.token = this.token;
      this.data.flg = flg;
      this.data.id = id;
      management
      .updateLeave(this.data)
      .then((response) => {
        if(response.Success == true){
          this.$message({
                type: "success",
                message:response.message
            }
          ) 
        }
        else{
          this.$message({
                type: "false",
                message:response.message
            })
        }
        this.getList()
      })
    },
  },
};
</script>