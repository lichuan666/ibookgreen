<template>
<div class = "contain">
    <main class="container">
    <div class="text-center">
        <hr class="my-4">
        <h4 style="font-weight: bold;">当前预约情况</h4>
        <hr class="my-4">
    </div>
        <div class="row">
            <div class="col-3 mt-3 bg" v-for="reservation in reservation_list">
            <div class="reservation-card">
                <div class="p-4 rounded mt-3 h-100">
                    <!--
                    <h5>座位号：{{ reservation.seat_id }}
                    <a-button type="button" @click="sign(reservation.seat_id,reservation.create_time)" style="margin-left: 35px;border-radius:20px">签到</a-button>
                    </h5>
                    <h5>开始时间：{{ reservation.start_time }}</h5>
                    <h5>结束时间：{{ reservation.end_time }}</h5>
                    -->
                    <h5 style="font-size: 20px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">座位号：{{ reservation.seat_id }}
                    <a-button type="button" @click="sign(reservation.seat_id,reservation.create_time)" style="margin-left: 35px;border-radius:20px">签到</a-button>
                    </h5>
                    <h5 style="font-size: 20px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">开始时间：<br>{{ reservation.start_time }}</h5>
                    <h5 style="font-size: 20px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">结束时间：<br>{{ reservation.end_time }}</h5>
                    
                    <h5>状态：<span style="font-weight: bold;">{{ reservation.status == 1 ? '已签到':'未签到' }}</span></h5>

                    <p class="lead text-center">请保持良好的学习环境！</p>
                    <p class="text-center">
                        <a type="button" class="btn btn-outline-success" data-bs-toggle="modal"
                           data-bs-target="#exampleModal-1" @click="choooser(reservation.id)">取消预约</a>
                    </p>


                    <!-- Button trigger modal -->

                    <!-- Modal 原版-->
                    <!--
                    <div class="modal fade" id="exampleModal-1" tabindex="-1"
                         aria-labelledby="exampleModalLabel"
                         aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="exampleModalLabel">请确认一下信息！</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <p class="h5">你确定取消吗？</p>


                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                        取消
                                    </button>
                                    <a class="btn btn-danger" @click="cancel" data-bs-dismiss="modal">确定</a>
                                </div>
                            </div>
                        </div>
                    </div>
                -->    
                        <div class="modal fade" id="exampleModal-1" tabindex="-1"
                            aria-labelledby="exampleModalLabel"
                            aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered" style="max-width: 23%">
                                <div class="modal-content">

                                    <div class="modal-body text-center">
                                        <p class="h5">是否取消当前预约？</p>
                                    </div>
                                    <div class="modal-footer d-flex justify-content-center">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                            否，我再想想
                                        </button>
                                        <a class="btn btn-danger" @click="cancel" data-bs-dismiss="modal">是，确定取消</a>
                                    </div>
                                </div>
                            </div>
                        </div>

                </div>
            </div>
            </div>
        </div>
        <div class="text-center">
        <hr class="my-4">
        <h4 style="font-weight: bold;">历史预约情况</h4>
        <hr class="my-4">
        </div>

        <div class="row">
            <div class="col-3 mt-3 bg" v-for="reservation in history_list">
                <!--历史记录-->
                <div class="reservation-card2">
                <div class="p-4 rounded mt-3 h-100">
                    <!--
                    <p style="font-size: 14px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">
                    座位号：{{ reservation.seat_id }}
                    </p>
                    <a-card title="开始时间：">
                    {{ reservation.start_time }}
                    </a-card>
                    <a-card title="结束时间：">
                    {{ reservation.end_time }}
                    </a-card>
                    -->
                    <h5 style="font-size: 20px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">座位号：{{ reservation.seat_id }}</h5>
                    <h5 style="font-size: 20px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">开始时间：<br>{{ reservation.start_time }}</h5>
                    <h5 style="font-size: 20px; color: rgba(0, 0, 0, 0.85); margin-bottom: 16px; font-weight: 500">结束时间：<br>{{ reservation.end_time }}</h5>
                    
                    <p class="text-center">
                        <a type="button" class="btn btn-outline-success"  @click="again(reservation)">再次预约</a>
                    </p>
                </div>
                </div>
            </div>
        </div>    
        
    </main>
    <!--2.0
    <a-modal v-model:visible="visible" title="请再次进行确认" @ok="cancel">
        <h5>是否需要取消预约</h5>
    </a-modal>
    <a-alert v-model:visible = "visible3" message="Warning"
    description="warn"
    type="warning"
    show-icon
    closable
    />
    -->
</div>
</template>

<script>
import axios from 'axios';
import router from "@/router";
import moment from 'moment';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8080/',
});
apiClient.interceptors.request.use(config => {
    config.headers['token'] = localStorage.getItem('token');
    config.headers['username'] = localStorage.getItem('username');
    return config;
});




export default {
    name: "Recording",
    data() {
        return {
            rid:'',       //选择的预约记录
            warn:'',         //警告信息
            visible3:false,
            reservation_list: [
                /*
                {
                    "seat_id": 1,
                    "start_time": "2023-04-15T21:19:56.824734",
                    "end_time": "2023-04-15T22:19:56.824734",
                    "status": "2"
                },
                {
                    "seat_id": 4,
                    "start_time": "2023-04-14T10:00:00",
                    "end_time": "2023-04-14T11:00:00",
                    "status": "1"
                }
                */
            ],
            history_list:[],            //历史预约情况
        }
    },
    
    created () {
    this.getr()
    },

    methods: {
        choooser(id) {
            //console.log("Recording cancel")
            console.log("value",id)
            this.rid = id;
            this.visible = false
        },

        async cancel() {
            let rid = this.rid
            const data = {
                rid:rid,             
            };
            // 发送请求(改)
            axios.post('http://localhost:8080/index/cancel/', data)      
                    .then(response => {
                        console.log("cancel",response.data)
                        //this.hidden = false
                        //this.visible = true
                        console.log("cancel",this.hidden)
                        this.getr()         //刷新页面
                        })   
        },

        //再次预约
        async again(reservation,) {
            let seat_id = reservation.seat_id         //唯一标识符
            let sid = 1      //先写死
            let start_time = reservation.start_time
            let end_time = reservation.end_time
            let time = new Date()
            let inputTime= new Date().getTime()

            const offset = (new Date()).getTimezoneOffset();

            let localTime = (new Date(inputTime - offset * 60000)).toISOString()

            localTime = (new Date(inputTime - offset * 60000)).toISOString();

            localTime = localTime.substr(0, localTime.lastIndexOf('.'));

	        localTime = localTime.replace('T', ' ');        //去除了t&z后得到的结果
            

            const data = {
                sid:1,             //先写死，后面换成全局变量
                start_time:start_time,
                seat_id:seat_id,
                end_time:end_time,
                time:localTime       //当前时间
            };
            console.log("again data",data)
            // 发送请求
            axios.post('http://localhost:8080/index/again_reservation/', data)      
                    .then(response => {
                        console.log("sign",response.data);
                    })
        },

        async sign(seat_id,create_time) {
            
            
            /*
            var map = new BMapGL.Map("allmap");
            var point = new BMapGL.Point(116.331398,39.897445);
            map.centerAndZoom(point,12);
        
            var geolocation = new BMapGL.Geolocation();
            geolocation.getCurrentPosition(function(r){
                if(this.getStatus() == BMAP_STATUS_SUCCESS){
                var mk = new BMapGL.Marker(r.point);
                map.addOverlay(mk);
                map.panTo(r.point);
                alert('您的位置：' + r.point.lng + ',' + r.point.lat);
                }
                else {
                    alert('failed' + this.getStatus());
                }        
            });
            */
            //总之就是需要一个定位，再说吧

        var map, geolocation;
        //加载地图，调用浏览器定位服务
        map = new AMap.Map('container', {
        resizeEnable: true
        });
        map.plugin('AMap.Geolocation', function() {
             geolocation = new AMap.Geolocation({
                 enableHighAccuracy: true,//是否使用高精度定位，默认:true
                timeout: 10000,          //超过10秒后停止定位，默认：无穷大
                buttonOffset: new AMap.Pixel(10, 20),//定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
                zoomToAccuracy: true,      //定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
                buttonPosition:'RB'
            });
           map.addControl(geolocation);
            geolocation.getCurrentPosition();
            AMap.event.addListener(geolocation, 'complete', onComplete);//返回定位信息
            AMap.event.addListener(geolocation, 'error', onError);      //返回定位出错信息
         });

        //解析定位错误信息
        function onError(data) {
            console.log('失败',data)
        }

        //解析定位结果
        function onComplete(data) {
            //var str=['定位成功'];
            //str.push('经度：' + data.position.getLng());
            let jing = data.position.getLng()
            let wei = data.position.getLat()
            console.log('经纬度：' , data.position,data.position.getLat())
            if(Math.abs(jing-121.52)<0.01&Math.abs(wei-31.34)<0.01)
            {
                console.log('可以打卡')
                console.log('相差：',Math.abs(jing-121.52),Math.abs(wei-31.34)<0.1)
                // 创建要发送的数据对象
                let time  = new Date()
                time = moment(time).format('YYYY-MM-DD HH:mm:ss');
                const para = {
                    sid:1,             //先写死，后面换成全局变量
                    time:time,
                    seat_id:seat_id,
                    createtime:create_time
                };
                console.log("sign",data)
                // 发送请求(改)
                axios.post('http://localhost:8080/index/sign/', para)      
                    .then(response => {
                        console.log("sign",response.data);
                        })
            }
            else
            {
                console.log('相差：',jing-121.52,wei-31.34)
                let info = '当前位置太远'
                this.visible3 = true
                this.warn = info
                
            }
            
            /*
           if(data.accuracy){
                 str.push('精度：' + data.accuracy + ' 米');
             }//如为IP精确定位结果则没有精度信息
           str.push('是否经过偏移：' + (data.isConverted ? '是' : '否'));
            document.getElementById('tip').innerHTML = str.join('<br>');
            */
        }
        },

        async getr() {
        try {
            const data = {
                sid:1,             //先写死，后面换成全局变量
                method:'getall',
            };
            //const response = await apiClient.get('/index/view_reservation/', {});
            // 发送请求(改)
            axios.post('http://localhost:8080/index/view_reservation/', data)      
                    .then(response => {
                        console.log("sign",response.data);
                        this.reservation_list = response.data.reservation_list
                        for(let i=0;i<this.reservation_list.length;i++)
                        {
                            this.reservation_list[i].start_time = this.reservation_list[i].start_time.replace('T',' ')
                            this.reservation_list[i].end_time = this.reservation_list[i].end_time.replace('T',' ')
                        }
                        let history = response.data.history

                        //response.data.reservation_list.filter.exclude(status=3)     //!=的写法好像不行
                        console.log("history",history)
                        for(let i=0;i<history.length;i++)
                        {
                            history[i].start_time = history[i].start_time.replace('T',' ')
                            history[i].end_time = history[i].end_time.replace('T',' ')
                        }
                        this.history_list = history
                        })
            
        } catch (error) {
            console.error(error); // 打印请求错误信息
        }
        },
    }
    
}
</script>

<style scoped>
.reservation-card {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  padding: 1rem;
  border-radius: 1rem;
  margin-bottom: 0.5rem;
  background-color: #ececf0;        /*#f8f8f8*/
  height: 100%; /* 设置高度为100%以充满父容器 */
}
.reservation-card2 {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  padding: 1rem;
  border-radius: 1rem;
  margin-bottom: 5rem;
  background-color: #ececf0;
  height: 80%; /* 设置高度为100%以充满父容器 */
}


.contain{
    background-image: url('../../assets/img/7.jpg');
    width:100%;
    height:1050px;
    background-size: contain;
    margin-top:-20px;
}

</style>