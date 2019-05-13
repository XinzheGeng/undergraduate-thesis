import './plugins/element'
import 'normalize.css'
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// 按需加载
// import { faSearch } from '@fortawesome/free-solid-svg-icons'
// import { library } from '@fortawesome/fontawesome-svg-core'
import App from './App.vue'
import Vue from 'vue'
import router from './router'

// library.add(faSearch)
// template 里直接用 <font-awesome-icon icon="user"/> 即可
// Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')
