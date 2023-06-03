<template>
<div class = "contain">
    <main class="container">
        <div class="bg-light p-4 rounded mt-3">
            <h3>欢迎使用
            <a-button type="primary" ghost @click="showModal2">抢座</a-button>
            </h3>
            <p class="lead">自习室预约管理系统</p>
            <a-table :dataSource="recommend" :columns="columns">
                <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'set'">
                    <a-button type="primary" ghost @click="showModal(record.seat_id,record.room_id)">预约</a-button>
                </template>
                </template>
            </a-table>
        </div>
    </main>
    </div>
    <a-modal v-model:visible="visible2" title="抢座结果" @ok="handleOK2">
        {{get}}
    </a-modal>
    <a-modal v-model:visible="visible" title="选择时间" @ok="handleOK">
    <div class="box">
            <div>预约情况</div>                                       <!--disable前面记得加：-->
            <a-button type="primary" :disabled="sbook[0]">00:00:00-01:00:00</a-button>
            <a-button type="primary" :disabled="sbook[1]">01:00:00-02:00:00</a-button>
            <a-button type="primary" :disabled="sbook[2]">02:00:00-03:00:00</a-button>
            <a-button type="primary" :disabled="sbook[3]">03:00:00-04:00:00</a-button>
            <a-button type="primary" :disabled="sbook[4]">04:00:00-05:00:00</a-button>
            <a-button type="primary" :disabled="sbook[5]">05:00:00-06:00:00</a-button>
            <a-button type="primary" :disabled="sbook[6]">06:00:00-07:00:00</a-button>
            <a-button type="primary" :disabled="sbook[7]">07:00:00-08:00:00</a-button>
            <a-button type="primary" :disabled="sbook[8]">08:00:00-09:00:00</a-button>
            <a-button type="primary" :disabled="sbook[9]">09:00:00-10:00:00</a-button>
            <a-button type="primary" :disabled="sbook[10]">10:00:00-11:00:00</a-button>
            <a-button type="primary" :disabled="sbook[11]">11:00:00-12:00:00</a-button>
            <a-button type="primary" :disabled="sbook[12]">12:00:00-13:00:00</a-button>
            <a-button type="primary" :disabled="sbook[13]">13:00:00-14:00:00</a-button>
            <a-button type="primary" :disabled="sbook[14]">14:00:00-15:00:00</a-button>
            <a-button type="primary" :disabled="sbook[15]">15:00:00-16:00:00</a-button>
            <a-button type="primary" :disabled="sbook[16]">16:00:00-17:00:00</a-button>
            <a-button type="primary" :disabled="sbook[17]">17:00:00-18:00:00</a-button>
            <a-button type="primary" :disabled="sbook[18]">18:00:00-19:00:00</a-button>
            <a-button type="primary" :disabled="sbook[19]">19:00:00-20:00:00</a-button>
            <a-button type="primary" :disabled="sbook[20]">20:00:00-21:00:00</a-button>
            <a-button type="primary" :disabled="sbook[21]">21:00:00-22:00:00</a-button>
            <a-button type="primary" :disabled="sbook[22]">22:00:00-23:00:00</a-button>
            <a-button type="primary" :disabled="sbook[23]">23:00:00-24:00:00</a-button>
        </div>
        <a-range-picker
                :show-time="{ format: 'HH' }"
                format="YYYY-MM-DD HH"
                :placeholder="['开始时间', '结束时间']"
                @change="onRangeOk"                                         
        />
    </a-modal>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
    name: "index",
    date: [],
    
    data() {
        return {
            recommend: '',
            visible: false,
            visible2: false,
            seat_id:'',       //当前预约的座位号
            room_id:'',
            get:'抢到的座位',
            open:8,
            close:20,
            book:[true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true],    
            sbook:[],    //每个座位被预定的情况
            columns: [
                {
                    title: '座位id',
                    dataIndex: 'seat_id',
                    key: 'seat_id',
                },
                {
                    title: '位置',
                    dataIndex: 'pos',
                    key: 'pos',
                },
                {
                    title: '类型',
                    dataIndex: 'type',
                    key: 'type',
                },
                {
                    title: '状态',
                    dataIndex: 'state',
                    key: 'state',
                },
                {
                    title: '预约',
                    dataIndex: 'set',
                    key: 'set',
                },
            ],
        }
    },
    created () {
    this.getr()
    },
    methods: {
        //显示预约
        showModal(seat_id,room_id) {
            this.seat_id = seat_id
            this.room_id = 1 //room_id
            this.visible = true;
            console.log(seat_id,room_id)
            try {
                let inputTime= new Date().getTime()
                const offset = (new Date()).getTimezoneOffset();
                let localTime = (new Date(inputTime - offset * 60000)).toISOString()
                localTime = (new Date(inputTime - offset * 60000)).toISOString();
                localTime = localTime.substr(0, localTime.lastIndexOf('.'));
	            localTime = localTime.replace('T', ' ');        //去除了t&z后得到的结果

                const data = {
                room_id: this.room_id,
                seat_id: seat_id,
                time:localTime    
                }
                console.log("data",data)
                axios.post('http://localhost:8080/index/view_time/', data)      
                    .then(response => {
                        console.log(response.data.time); // 打印响应数据
                        
                        this.sbook =this.book           //先完成初始化
                        for(let j=0 ; j < response.data.time.length;j++)
                        {
                            
                            let times = response.data.time[j]
                            //let begin = moment(times.begin).format('YYYY-MM-DD HH:mm:ss')
                            console.log(times,times.end)
                            for(let i=times.begin;i<times.end;i++)    
                                this.sbook[i] = true            //被预约的时间段需要关闭
                        }

                        })   
            } catch (error) {
                console.error(error); // 打印请求错误信息
            }
        },

        //抢座
        showModal2() {        
            this.visible2 = true;
            let inputTime= new Date().getTime()
            const offset = (new Date()).getTimezoneOffset();
            let localTime = (new Date(inputTime - offset * 60000)).toISOString()
            localTime = (new Date(inputTime - offset * 60000)).toISOString();
            localTime = localTime.substr(0, localTime.lastIndexOf('.'));
	        localTime = localTime.replace('T', ' ');        //去除了t&z后得到的结果
            const data = {
                sid:1,             //先写死，后面换成全局变量
                time:localTime,        //当前时间
            };
            // 发送请求(改)
            axios.post('http://localhost:8080/index/get/', data)      
                    .then(response => {
                        console.log("get seat",response.data);
                        //this.recommend = response.data.seat_list
                        this.get = response.data.msg
                        })
        },

        async getr() {
            // 创建要发送的数据对象
            const data = {
                sid:1,             //先写死，后面换成全局变量
            };
            //const params = qs.stringify(data);
            console.log("s data",data)
            
            // 发送请求(改)
            axios.post('http://localhost:8080/index/recommend/', data)      
                    .then(response => {
                        console.log("get recommend",response.data);
                        this.recommend = response.data.seat_list
                        //理论上需要room的情况，暂时先这样吧
                        for(let i=this.open;i<this.close;i++)
                        {
                            //console.log(i)
                            this.book[i] = false
                        }
                        this.sbook =this.book
                        
                        })
        },

        
        onRangeOk(value,dateString) {                    //进行一定的调整
            console.log("time",value,dateString)
            this.date = dateString;
        },

        handleOK2()
        {
            this.visible2 = false
        },

        //和seat中匹配
        async handleOK() {
            console.log("????????")
            const startDateString = moment(this.date[0]).format('YYYY-MM-DD HH:mm:ss');
            const endDateString = moment(this.date[1]).format('YYYY-MM-DD HH:mm:ss');
            console.log("time",startDateString)
            const data = {
                room_id: parseInt(this.room_id),
                seat_id: parseInt(this.seat_id),
                start_time: startDateString,
                end_time: endDateString,
                sid:1            //学生的uid（理论上应该用个全局变量，先凑合一下吧，出错就改成测试账号的id）
            };
            console.log(data)
            try {
                //const response = await apiClient.post('/index/reservation/', data);
                //console.log(response.data); // 打印响应数据
                console.log("data:",data)
                //console.log(this.GLOBAL.uid)
                axios.post('http://localhost:8080/index/reservation/', data)      
                    .then(response => {
                        console.log(response.data); // 打印响应数据
                        let zhuangtai = '占用'

                        //this.seat_list[this.seat_id-1].state = zhuangtai
                        this.visible = false      //关闭窗口
                        })   
            } catch (error) {
                console.error(error); // 打印请求错误信息
            }
        }
        }

}
</script>

<style scoped>
.contain{
    background-image: url('../../assets/img/7.jpg');
    width:100%;
    height:700px;
    background-size: contain;
    margin-top:-20px;
    padding-top:20px;
}

.box{
    padding:10px;
}


</style>