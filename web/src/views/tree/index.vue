<template>
  <div class="app-container">
    <el-input v-model="filterText" placeholder="Filter keyword" style="margin-bottom:30px;" />

    <el-tree
      ref="tree2"
      :data="data2"
      :props="defaultProps"
      :filter-node-method="filterNode"
      class="filter-tree"

    />

  </div>
  <!--       default-expand-all -->
</template>

<script>
import { getTeam } from '@/api/team'

export default {
  data() {
    return {
      filterText: '',
      OpenOrNot:false,
      data2: null,
      TeamQuery: {
        grede:0,
        token:""
      },
      defaultProps: {
        children: 'children',
        label: 'label'
      }
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree2.filter(val)
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    fetchData() {
      this.listLoading = true
      
      getTeam(this.TeamQuery).then(response => {
        this.data2 = response.data.items
        this.listLoading = false
      })
    }
  }
}
</script>

