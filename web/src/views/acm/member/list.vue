<template>
  <div class="app-container">
      <!-- 查询表单-->
      <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="memberQuery.user_id" placeholder="学号"/>
      </el-form-item>

      <el-form-item>
        <el-input v-model="memberQuery.user_name" placeholder="姓名"/>
      </el-form-item>

      <el-form-item>
        <el-input v-model="memberQuery.grade" placeholder="年级"/>
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
      <el-table-column label="序号" width="70" align="center">
        <template slot-scope="scope">
          {{ (page - 1) * limit + scope.$index + 1 }}
        </template>
      </el-table-column>

      <el-table-column prop="user_id" label="学号" width="100" />

      <el-table-column prop="user_name" label="姓名" width="80" />

      <el-table-column prop="contact" label="联系方式" />

      <el-table-column prop="school" label="学校" width="100" />

      <el-table-column prop="grade" label="年级" width="80" />

      <el-table-column prop="position" label="成员类别" width="80" />

      <el-table-column prop="score" label="得分" width="60" />

      <el-table-column label="操作" width="300" align="cejnter">
        <template slot-scope="scope">
          <router-link :to="'/member/edit/' + scope.row.user_id">
            <el-button type="primary" size="mini" icon="el-icon-edit"
              >修改</el-button
            >
          </router-link>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="removeDataById(scope.row.user_id)"
            >删除</el-button
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

import member from "@/api/acm/member";

export default {
  //写核心代码的位置
  //   data: {

  //   },
  data() {
    //定义变量和初始值
    return {
      list: null, //条件查询之后接口返回集合
      page: 1, //当前页，默认值为1
      limit: 10, //每页记录数
      total: 0, //总记录数
      memberQuery: {}, //条件封装对象
      listLoading:false,
    };
  },
  created() {
    //页面渲染之前执行，一般调用methods定义的方法

    this.getList();
  },
  methods: {
    //创建具体方法
    getList(page = 1) {
        this.page = page
        this.listLoading = true
      member
        .getMemberListPage(this.page, this.limit, this.memberQuery)
        .then((response) => {
          //请求成功
          console.log(response)
          this.list = response.data.rows;
          this.total = response.data.total;
          this.listLoading = false
        })
    },//清空方法
    resetData() {
        //表单输入项数据清空
        this.memberQuery = {}

        //查询所有数据
        this.getList()
    },
    removeDataById(id) {
        this.$confirm('此操作将永久删除该成员, 是否继续?', '提示', {
            cancelButtonText: '取消',
            confirmButtonText: '确定',
          type: 'warning'
        }).then(() => {
            member.deleteMemberById(id)
            .then(response => {//删除成功
                //提示信息
                this.$message({
                type: 'success',
                message: '删除成功!'
                });
                //查询所有数据
                this.getList()
            })
        });
    }
  },
};
</script>