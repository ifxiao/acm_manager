import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app'
import user from './modules/user'
import getters from './getters'
// import constantRouterMap from '../router/modules/map'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    user,
    // router: constantRouterMap
  },
  getters
})

export default store
