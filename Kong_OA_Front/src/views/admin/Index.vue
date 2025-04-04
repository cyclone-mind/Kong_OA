

<template>
    <div>
    <el-row>
      <el-col :span="12">
        <div class="grid-content bg-purple">
          <!--                    饼形图-->
          <div id="main2" style="height: 400px;width: 100%;"></div>

        </div>
      </el-col>
      <el-col :span="12">
        <div class="grid-content bg-purple-light">

          <!--                    柱状图-->
          <div id="main1" style="height: 400px;width: 100%;"></div>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="24">
        <div class="grid-content bg-purple-dark">
          <!--                    折线图-->
          <div id="main3" style="height: 400px;width: 100%;"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script setup>
import * as echarts from 'echarts'
import {onMounted, ref, reactive} from "vue";

const option_1 = reactive({
  title: {
    text: '访问统计'
  },
  tooltip: {},
  legend: {
    data: ['访问量']
  },
  xAxis: {
    data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06"]
  },
  yAxis: {},
  series: [{
    name: '销量',
    type: 'bar',
    data: [5, 20, 36, 10, 10, 20]
  }]
})
const option_2 = reactive({
  title: {
    text: '用户访问来源',
    subtext: '纯属虚构',
    left: 'center'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
  },
  series: [
    {
      name: '访问来源',
      type: 'pie',
      radius: '50%',
      data: [
        {value: 1048, name: '手机'},
        {value: 735, name: '谷歌浏览器'},
        {value: 580, name: 'IE浏览器'},
        {value: 484, name: '火狐浏览器'},
        {value: 300, name: '苹果浏览器'}
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
})
const option_3 = reactive({
  title: {
    text: '访问人数统计'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['实际访问人数', '预测人数']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '实际访问人数',
      type: 'line',
      stack: '总量',
      data: [120, 182, 101, 234, 190, 330, 110]
    },
    {
      name: '预测人数',
      type: 'line',
      stack: '总量',
      data: [220, 303, 89, 134, 290, 330, 310]
    },


  ]
})

onMounted(() => {
  // 基于准备好的dom，初始化echarts实例
  var myChart_1 = echarts.init(document.getElementById('main1'));
  var myChart_2 = echarts.init(document.getElementById('main2'));
  var myChart_3 = echarts.init(document.getElementById('main3'));

  // 使用刚指定的配置项和数据显示图表。
  myChart_1.setOption(option_1);
  myChart_2.setOption(option_2);
  myChart_3.setOption(option_3);
});


</script>
<style scoped>

</style>