import {createApp} from 'vue'
import App from './App.vue'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import router from './router'

const app = createApp(App)

// 导入共用组件
//import global from './global.vue'
//Vue.prototype.global = global


app.use(router)
app.use(Antd)

app.mount('#app')

//高德定位
import AMap from 'vue-amap';
Vue.use(AMap);
// 初始化vue-amap
AMap.initAMapApiLoader({
// 高德key
key: '0796f517e1407c5b5e4d3205220a4410',
// 插件集合 （插件按需引入）
plugin: ['AMap.Geolocation'] 
    //AMap.Geolocation定位服务插件。融合了浏览器定位、高精度IP定位、安卓定位sdk辅助定位等多种            手段，提供了获取当前准确位置、获取当前城市信息、持续定位(浏览器定位)等功能。
});

//新添加
/*

const adamin = require('./components/adamin/Base.vue');
const student = require('./components/student/Base.vue');

const routes = [
    {
        name: 'admin',
        path: '/admin',                   //默认显示页面用/
        component: adamin
    },
    {
        name: 'student',
        path: '/student',
        component: student
    },
];
*/
