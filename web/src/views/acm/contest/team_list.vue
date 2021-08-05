<template>

  <div class="app-container">
      <!-- 查询表单-->
    <h3 class="title">{{contest_name}}</h3>
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

      <el-table-column prop="team_id" label="队伍号" width="50" />

      <el-table-column prop="grade" label="年级" width="85" />

      <el-table-column prop="team_name" label="队伍名" width="350" />

      <el-table-column prop="member1_name" label="队长" width = "100" />

      <el-table-column prop="member2_name" label="队员" width="100" />

      <el-table-column prop="member3_name" label="队员" width="100" />

      <el-table-column prop="coach" label="教练" width="100" />

      <el-table-column prop="modify_time" label="上次修改时间" />

      <el-table-column label="操作" width="300" align="cejnter">
        <template slot-scope="scope">
          <router-link :to="'/team/edit/' + scope.row.team_id">
            <el-button type="primary" size="mini" icon="el-icon-edit"
              >修改</el-button
            >
          </router-link>
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="removeDataById(scope.row.Fid)"
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

import contest from "@/api/acm/contest";
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
      teamQuery: {token:this.token}, //条件封装对象
      listLoading:false,
      contest_name:"",
      contest:null
    };
  },
  created() {
    //页面渲染之前执行，一般调用methods定义的方法
    this.init();
    this.getList();
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
      if (this.$route.params && this.$route.params.id) {
        // console.log("this is test");
        const id = this.$route.params.id;
        this.contest_id = id;
        this.queryContest(id);
      }
    },
    //创建具体方法
    handleSizeChange(val) {
        this.limit = val;
        this.getList();
    },
    getList(page = 1) {
        this.page = page
        this.listLoading = true
        // console.log(this.token);
        this.teamQuery.token = this.token
        // this.contest_id
      contest
        .getTeams(this.page, this.limit, this.contest_id)
        .then((response) => {
          this.list = response.data.rows;
          this.total = response.data.total;
          this.listLoading = false;
        })
    },//清空方法
    resetData() {
        //表单输入项数据清空
        this.teamQuery = {}

        //查询所有数据
        this.getList()
    },
    removeDataById(id) {
        this.$confirm('此操作将永久删除该成员, 是否继续?', '提示', {
            cancelButtonText: '取消',
            confirmButtonText: '确定',
          type: 'warning'
        }).then(() => {
            console.log(id);
            contest.deleteTeamById(id)
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
    },
    queryContest(id) {
    //   console.log("queryLint(id)");
      contest.getcontestInfo(id).then((response) => {
        this.flag = true;
        this.contest_name = response.data.contest.contest_name;
        // console.log(this.data);
        // console.log(this.options);
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