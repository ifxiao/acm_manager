<template>
  <div class="app-container">
      <!-- 查询表单-->
      <el-form :inline="true" class="demo-form-inline">
      <el-form-item>
        <el-input v-model="linkQuery.user_id" placeholder="学号"/>
      </el-form-item>

      <el-form-item>
        <el-input v-model="linkQuery.user_name" placeholder="姓名"/>
      </el-form-item>

      <el-select v-model="linkQuery.platform_id" placeholder="平台">
        <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
        </el-option>
      </el-select>

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

      <el-table-column prop="link" label="链接号" width="50" />

      <el-table-column prop="user_id" label="学号" width="85" />

      <el-table-column prop="user_name" label="姓名" width="70" />

      <el-table-column prop="platform_name" label="平台" width = "100" />

      <el-table-column prop="link_id" label="平台id" width="100" />

      <el-table-column prop="modify_time" label="上次修改时间" />

      <el-table-column label="操作" width="300" align="cejnter">
        <template slot-scope="scope">
          <router-link :to="'/submit/link_edit/' + scope.row.link">
            <el-button type="primary" size="mini" icon="el-icon-edit"
              >修改</el-button
            >
          </router-link>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="removeDataById(scope.row.link)"
            >删除</el-button
          >
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

import submit from "@/api/acm/submit";
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
      linkQuery: {token:this.token}, //条件封装对象
      listLoading:false,
      options: null
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
        // console.log(this.token);
        this.linkQuery.token = this.token
      submit
        .getLinkListPage(this.page, this.limit, this.linkQuery)
        .then((response) => {
          //请求成功
        //   console.log(response)
          this.list = response.data.rows;
          this.total = response.data.total;
          this.listLoading = false;
          this.options = response.data.options
        })
    },//清空方法
    resetData() {
        //表单输入项数据清空
        this.linkQuery = {}

        //查询所有数据
        this.getList()
    },
    removeDataById(id) {
        this.$confirm('此操作将永久删除该成员, 是否继续?', '提示', {
            cancelButtonText: '取消',
            confirmButtonText: '确定',
          type: 'warning'
        }).then(() => {
            submit.deleteLinkById(id)
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