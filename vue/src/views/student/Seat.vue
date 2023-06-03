<template>
<div class="contain">
    <main class="mb-5">
        <div class="container px-2 py-3" id="custom-cards">
            <h3 class="pb-2 m-1">请选择条件</h3>
            <form action="" class="row pb-2 g-3 border-bottom">

                <div class="col-md-6">
                    <label for="inputState" class="form-label">类型</label>
                    <a-select class="form-select"
                              ref="select"
                              v-model:value="value2"
                              @change="handleChange2"
                    >
                        <a-select-option value='普通'>普通</a-select-option>
                        <a-select-option value='靠电'>靠电</a-select-option>
                    </a-select>
                </div>

            </form>
        </div>
    </main>

  <!--    <a-space>-->
  <!--        <a-select-->
  <!--            ref="select"-->
  <!--            v-model:value="value1"-->
  <!--            style="width: 30%"-->
  <!--            @focus="focus"-->
  <!--            @change="handleChange"-->
  <!--        >-->
  <!--            <a-select-option value="jack">Jack</a-select-option>-->
  <!--            <a-select-option value="lucy">Lucy</a-select-option>-->
  <!--            <a-select-option value="disabled" disabled>Disabled</a-select-option>-->
  <!--            <a-select-option value="Yiminghe">yiminghe</a-select-option>-->
  <!--        </a-select>-->
  <!--        <a-select v-model:value="value2" style="width: 120px" disabled>-->
  <!--            <a-select-option value="lucy">Lucy</a-select-option>-->
  <!--        </a-select>-->
  <!--        <a-select v-model:value="value3" style="width: 120px" loading>-->
  <!--            <a-select-option value="lucy">Lucy</a-select-option>-->
  <!--        </a-select>-->
  <!--    </a-space>-->

    <div class="m-1 mb-5">
        <div class="accordion-item border-0">
            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo"
                 data-bs-parent="#accordionExample">
                <div class="accordion-body">

                    <input type="text" name="room" value="">
                    <input type="text" name="day" value="">
                    <input type="text" name="time" value="">


                </div>
            </div>

            <h5 class="m-2 mt-5 text-center">请选择座位：

                <div class="col-12">

                    <div class="row">
                        <div class="col-1" v-for="seat in seat_list">
                            <button class="btn btn-outline-success m-1 w-100 h-85 bg-light" @click="showModal(seat.seat_id)">
                                {{ seat.pos }}
                                <br/>
                                {{ seat.state }} <br/> {{ seat.type }}
                            </button>
                        </div>
                    </div>
                </div>

            </h5>
        </div>

    </div>
</div>
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
                :show-time="{ format: 'HH:mm' }"
                format="YYYY-MM-DD HH:mm"
                :placeholder="['开始时间', '结束时间']"
                @change="onRangeOk"  
        />
    </a-modal>

</template>

<script>
import apiClient from '../../axios';
import moment from 'moment';
import axios from "axios";

export default {
    name: "Seat",
    data() {
        return {
            date: '',
            seat_id: 1,
            visible: false,
            pos: [],
            value1: '',
            value2: '',
            open:8,
            close:20,
            book:[true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true,true],    
            sbook:[],    //每个座位被预定的情况
            //book:[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],        //该座位的预约情况
            options1: [{
                value: 'jack',
                label: 'Jack',
            }, {
                value: 'lucy',
                label: 'Lucy',
            }, {
                value: 'disabled',
                label: 'Disabled',
                disabled: true,
            }, {
                value: 'yiminghe',
                label: 'Yiminghe',
            }],
            seat_list: [],
                /*
                {
                    "seat_id": 1,
                    "pos": "1",
                    "type": "普通",
                    "state": "空闲"
                },
                {
                    "seat_id": 2,
                    "pos": "4",
                    "type": "普通",
                    "state": "关闭"
                },
                {
                    "seat_id": 3,
                    "pos": "5",
                    "type": "靠电",
                    "state": "空闲"
                },
                {
                    "seat_id": 4,
                    "pos": "6",
                    "type": "普通",
                    "state": "空闲"
                },
                {
                    "seat_id": 5,
                    "pos": "7",
                    "type": "靠电",
                    "state": "空闲"
                },
                {
                    "seat_id": 6,
                    "pos": "8",
                    "type": "普通",
                    "state": "空闲"
                },
                {
                    "seat_id": 7,
                    "pos": "9",
                    "type": "靠电",
                    "state": "空闲"
                },
                {
                    "seat_id": 8,
                    "pos": "10",
                    "type": "普通",
                    "state": "空闲"
                },
                {
                    "seat_id": 9,
                    "pos": "11",
                    "type": "普通",
                    "state": "空闲"
                },
                {
                    "seat_id": 10,
                    "pos": "12",
                    "type": "靠电",
                    "state": "空闲"
                },
                {
                    "seat_id": 11,
                    "pos": "13",
                    "type": "普通",
                    "state": "空闲"
                },
                {
                    "seat_id": 12,
                    "pos": "14",
                    "type": "靠电",
                    "state": "空闲"
                },
                {
                    "seat_id": 13,
                    "pos": "15",
                    "type": "普通",
                    "state": "空闲"
                }
            ]
            */
        }
    },
    async mounted() {
        try {
            //console.log("114514")
            console.log(this.$route.params)
            console.log(this.$route.params.id)
            const data={
                room_id:this.$route.params.id
            }
            /*
            const response = await apiClient.get('/index/seat/', {params: {room_id: parseInt(this.$route.params.id)}});
            console.log(response.data); // 打印响应数据
            this.seat_list = response.data.seat_list
            for (var i = 0; i < this.seat_list.length; i++) {
                this.pos.push({"value": this.seat_list[i].pos, "label": this.seat_list[i].pos})

            }
            */
            axios.post('http://localhost:8080/index/seat/', data)      
                    .then(response => {
                        console.log(response.data); // 打印响应数据
                        this.seat_list = response.data.seat_list
                        this.open = response.data.open
                        this.close = response.data.close
                        console.log(response.data.open,response.data.close)
                        for(let i=this.open;i<this.close;i++)
                        {
                            //console.log(i)
                            this.book[i] = false
                        }
                        this.sbook =this.book
                        })  
            //console.log(this.pos)
        } catch (error) {
            console.error(error); // 打印请求错误信息
        }
    },
    methods: {
        async showModal(seat_id) {
            this.seat_id = seat_id
            this.visible = true;
            
            try {
                let inputTime= new Date().getTime()
                const offset = (new Date()).getTimezoneOffset();
                let localTime = (new Date(inputTime - offset * 60000)).toISOString()
                localTime = (new Date(inputTime - offset * 60000)).toISOString();
                localTime = localTime.substr(0, localTime.lastIndexOf('.'));
	            localTime = localTime.replace('T', ' ');        //去除了t&z后得到的结果

                const data = {
                room_id: parseInt(this.$route.params.id),
                seat_id: parseInt(this.seat_id),
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
        async handleOK() {
            console.log("rtime:",this.date,this.date[0])
            const startDateString = moment(this.date[0]).format('YYYY-MM-DD HH:mm:ss');
            const endDateString = moment(this.date[1]).format('YYYY-MM-DD HH:mm:ss');
            console.log("time:",startDateString,endDateString)
            const data = {
                room_id: parseInt(this.$route.params.id),
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
                        let zhuangtai = '占用'    //考虑占满了再说
                        //this.seat_list[this.seat_id-1].state = zhuangtai
                        this.visible = false      //关闭窗口
                        })   
            } catch (error) {
                console.error(error); // 打印请求错误信息
            }
        },
        onRangeOk(value,dateString) {                    //进行一定的调整
            console.log("time",value,dateString)
            this.date = dateString;
        },
        async handleChange2() {
            /*
            try {
                const response = await apiClient.get('/index/seat/', {
                    params: {
                        params: {
                            room_id: parseInt(this.$route.params.id),
                            type: this.value2
                        }
                    }
                });
                console.log(response.data); // 打印响应数据
                this.seat_list = response.data.seat_list
                console.log(this.seat_list)
            } catch (error) {
                console.error(error); // 打印请求错误信息
            }
            */
            try {
            console.log('seat type:',this.value2)
            const data={
                room_id:this.$route.params.id,
                type:this.value2
            }
            axios.post('http://localhost:8080/index/cseat/', data)      
                    .then(response => {
                        console.log(response.data); // 打印响应数据
                        this.seat_list = response.data.seat_list
                        })  
            } catch (error) {
            console.error(error); // 打印请求错误信息
            }
        },

        async handleChange1() {
            try {
                const response = await apiClient.get('/index/seat/', {
                    params: {
                        params: {
                            room_id: parseInt(this.$route.params.id),
                            pos: this.value1,
                            type: this.value2,
                        }
                    }
                });
                console.log(response.data); // 打印响应数据
                this.seat_list = response.data.seat_list
                console.log(this.seat_list)
            } catch (error) {
                console.error(error); // 打印请求错误信息
            }
        }
    },
}
</script>

<style scoped>
.contain{
    background-image: url('../../assets/img/7.jpg');
    width:100%;
    height:700px;
    background-size: contain;

}
.box{
    padding:10px;
}
</style>