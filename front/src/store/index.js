import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const auth = {
    state: {
        logined: false
    },
    getters: {
        logined(state) {
            console.log('getters')
            return state.logined
        }
    },
    mutations: {
        login(state) {
            console.log('login')
            state.logined = true
        },
        logout(state) {
            state.logined = false
        }
    }
}

export default new Vuex.Store({
    modules: {
        auth
    }
})