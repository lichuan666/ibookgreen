<template>
<div class='contain'>
    <main class="container">
        <!--
        <div class="bg-danger p-5 rounded mt-3 text-white" v-for="warn in warn_list">
            <p class="lead">{{ warn.title }}</p>
            <p class="lead">{{ warn.text }}</p>
            <p class="lead">{{ warn.time }}</p>
        </div>
        -->
        <div v-for="warn in warn_list">
        <a-alert 
        message="行为警告"
        description="您有一次违约记录     
        2023-04-15 20:19:56"
        type="error"
        show-icon
        />
        </div>
        <!--
        <div class = 'pic'>
        <img class="mb-4" src="../../assets/img/noright.png" alt="" width="350" height="300">
        </div>
        -->
    </main>
</div>
</template>

<script>
import apiClient from "../../axios";
import axios from "axios";
import moment from 'moment';

export default {
    name: "warn",
    data() {
        return {
            warn_list: [

                //{
                  //  "title": "Behavior Warning",
                  //  "text": "Your behavior in class has been unacceptable. Please meet with me to discuss ways to improve.",
                  //  "time": "2023-04-15T20:19:56.854695",
                  //  "is_active": true
                //},
                //{
                  //  "title": "Behavior Warning",
                  //  "text": "Your behavior in class has been unacceptable. Please meet with me to discuss ways to improve.",
                  //  "time": "2023-04-15T20:19:56.854695",
                  //  "is_active": true
                //}

            ]
        }
    },
    created () {
    this.getw()
    },
     methods: {

        async getw() {
            // 创建要发送的数据对象
            const data = {
                sid:1             //先写死，后面换成全局变量
            };
            //const params = qs.stringify(data);
            console.log("s data",data)
            
            // 发送请求(改)
            axios.post('http://localhost:8080/index/warn/', data)      
                    .then(response => {
                        console.log("get warn",response.data);
                        this.warn_list = response.data.warn_list
                        for(let i=0;i<response.data.warn_list.length;i++)
                        {
                            let thewarn =  response.data.warn_list[i]
                            response.data.warn_list[i].time = moment(thewarn.time).format('YYYY-MM-DD HH:mm:ss');       //让显示更加正常一点
                        }
                        })
        }
    }
    

    
    //async mounted() {
      //  try {
            
        //    const response = await apiClient.get('/index/warn/', {});
        //    console.log(response.data); // 打印响应数据
        //    this.warn_list = response.data.warn_list
        //    console.log(this.warn_list)

        //} catch (error) {
        //    console.error(error); // 打印请求错误信息
        //}
    //},

}
</script>

<style scoped>
.container{
    
}


.pic{
    display:flex;
    justify-content:center;
    width:100%;
    margin-top:50px;
}

.contain{
    background-image: url('../../assets/img/7.jpg');
    width:100%;
    height:700px;
    background-size: contain;
    padding-top:20px;
}


</style>