import Layout from '@/views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: '首页',
    hidden: true,
    children: [{
      path: 'dashboard',
      name:'首页',
      component: () => import('@/views/dashboard/index')
    }]
  },
  // tableRouter,
  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/table',
  //   name: 'Example',
  //   meta: { title: 'Example', icon: 'example' },
  //   children: [
  //     {
  //       path: 'table',
  //       name: 'Table',
  //       component: () => import('@/views/table/index'),
  //       meta: { title: 'Table', icon: 'table' }
  //     },
  //     {
  //       path: 'tree',
  //       name: 'Tree',
  //       component: () => import('@/views/tree/index'),
  //       meta: { title: 'Tree', icon: 'tree' }
  //     },

  //   ]
  // },
  {
    path: '/member',
    component: Layout,
    redirect:"/member/table",
    name: '成员管理',
    meta: { title: '成员管理', icon: 'example' },
    children: [
      {
        path: 'table',
        name: '成员列表',
        component: () => import('@/views/acm/member/list'),
        meta: { title: '成员列表', icon: '' }
      },
      {
        path: 'edit/:user_id',
        name: '编辑成员',
        component: () => import('@/views/acm/member/save'),
        meta: { title: '编辑成员', noCache:true},
        hidden: true
      },
      {
        path: 'add',
        name: '添加成员',  
        component: () => import('@/views/acm/member/save'),
        meta: { title: '添加成员', icon: '' }
      },
      // {
      //   path: 'test',
      //   name: 'test',
      //   component: () => import('@/views/acm/member/test'),
      //   meta: { title: 'test', icon: '' }
      // },
    ]
  },
  {
    path: '/contest',
    component: Layout,
    redirect:"/contest/list",
    name: '比赛管理',
    meta: { title: '比赛管理', icon: 'example' },
    children: [
      
      {
        path: 'list',
        name: '比赛列表',
        component: () => import('@/views/acm/contest/contest_list'),
        meta: { title: '比赛列表', icon: '' }
      },
      {
        path: 'add',
        name: '添加比赛',
        component: () => import('@/views/acm/contest/contest_edit'),
        meta: { title: '添加比赛', icon: '' }
      },
      {
        path: 'edit/:id',
        name: '编辑比赛',
        component: () => import('@/views/acm/contest/contest_edit'),
        meta: { title: '编辑比赛', noCache:true},
        hidden: true
      },
      {
        path: 'team_list/:id',
        name: '队伍列表',
        component: () => import('@/views/acm/contest/team_list'),
        meta: { title: '队伍列表', noCache:true},
        hidden: true
      },
      {
        path: 'add_team/:id',
        name: '分配队伍',
        component: () => import('@/views/acm/contest/add_team'),
        meta: { title: '分配队伍', noCache:true},
        hidden: true
      },
      {
        path: 'balloon',
        name: '气球监控',
        component: () => import('@/views/acm/contest/balloon'),
        meta: { title: '气球监控', icon: '' }
      },
      // {
      //   path: 'test',
      //   name: 'test',
      //   component: () => import('@/views/acm/member/test'),
      //   meta: { title: 'test', icon: '' }
      // },
    ]
  },
  {
    path: '/submit',
    component: Layout,
    redirect:"/submit/submit_list",
    name: '训练监控',
    meta: { title: '训练监控', icon: 'example' },
    children: [
      {
        path: 'submit_list',
        name: '刷题记录',
        component: () => import('@/views/acm/submit/submit_list'),
        meta: { title: '刷题记录', icon: '' }
      },
      {
        path: 'link_list',
        name: '关联账号',
        component: () => import('@/views/acm/submit/link_list'),
        meta: { title: '关联账号', icon: '' }
      },
      {
        path: 'link_edit',
        name: '添加关联账号',
        component: () => import('@/views/acm/submit/link_edit'),
        meta: { title: '添加关联账号' },
      },
      {
        path: 'link_edit/:link',
        name: '编辑关联账号',
        component: () => import('@/views/acm/submit/link_edit'),
        meta: { title: '编辑关联账号', noCache:true },
        hidden: true
      },
    ]
  },
  {
    path: '/team',
    component: Layout,
    redirect:"/team/team_list",
    name: '队伍管理',
    meta: { title: '队伍管理', icon: 'example' },
    children: [
      {
        path: 'team_list',
        name: '队伍列表',
        component: () => import('@/views/acm/team/team_list'),
        meta: { title: '队伍列表', icon: '' }
      },
      {
        path: 'add',
        name: '添加队伍',
        component: () => import('@/views/acm/team/team_edit'),
        meta: { title: '添加队伍' },
      },
      {
        path: 'edit/:team_id',
        name: '编辑队伍',
        component: () => import('@/views/acm/team/team_edit'),
        meta: { title: '编辑队伍', noCache:true },
        hidden: true
      },
    ]
  },
  {
    path: '/management',
    component: Layout,
    redirect:"/management/list",
    name: '管理团队',
    meta: { title: '管理团队', icon: 'example' },
    children: [
      // {
      //   path: 'Leave_list',
      //   name: '请假单列表',
      //   component: () => import('@/views/acm/menagement/Leave_list'),
      //   meta: { title: '请假单列表', icon: '' }
      // },
      {
        path: 'edit_Leave',
        name: '请假',
        component: () => import('@/views/acm/management/leave_edit'),
        meta: { title: '请假' },
      },
      // {
      //   path: 'edit/:team_id',
      //   name: '编辑队伍',
      //   component: () => import('@/views/acm/team/team_edit'),
      //   meta: { title: '编辑队伍', noCache:true },
      //   hidden: true
      // },
    ]
  },
  // {
  //   path: '/form',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'Form',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: 'Form', icon: 'form' }
  //     }
  //   ]
  // },


  { path: '*', redirect: '/404', hidden: true }
]
export default constantRouterMap
