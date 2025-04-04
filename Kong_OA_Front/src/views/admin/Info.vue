<template>
  <div class="system-info-container">
    <div class="system-info-header">
      <h1>操作系统:{{ systemInfo.os }}</h1>
    </div>
    <div class="system-info-content">
      <div class="chart-card">
        <div class="chart-card-title">CPU 使用率</div>
        <div ref="cpuChart" class="chart-container" id="cpu-chart"></div>
      </div>
      <div class="chart-card">
        <div class="chart-card-title">磁盘使用情况</div>
        <div ref="diskChart" class="chart-container" id="disk-chart"></div>
      </div>
      <div class="chart-card">
        <div class="chart-card-title">内存使用情况</div>
        <div ref="memoryChart" class="chart-container" id="memory-chart"></div>
      </div>
      <div class="chart-card">
        <div class="chart-card-title">网络流量</div>
        <div ref="networkChart" class="chart-container" id="network-chart"></div>
      </div>
    </div>
  </div>
</template>

<script setup>



// 定时，每隔 5 秒请求一次数据

// 1 导入依赖
import { ref, onMounted, onBeforeUnmount, render } from 'vue';
import { reqServerData } from '../../api/home';
import * as echarts from 'echarts';
const systemInfo = ref({});
let pollInterval = null;
// 2 写一个async函数，用于请求数据
async function getServerData() {
  let res = await reqServerData();
  systemInfo.value = res.data;
  renderCharts();
}

// 3 渲染页面--》echars--》百度--》柱状图，饼形图，折线图
const renderCharts = () => {

// CPU Chart
if (systemInfo.value.cpu) {

  const cpuChart = echarts.init(document.getElementById('cpu-chart'));
  const cpuOption = {
    title: {
      text: 'CPU 使用率 (%)',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}%'
    },
    series: [
      {
        name: 'CPU',
        type: 'pie',
        radius: '70%',
        data: [
          { value: systemInfo.value.cpu.percent, name: '已使用' },
          { value: 100 - systemInfo.value.cpu.percent, name: '空闲' }
        ],
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  cpuChart.setOption(cpuOption);
}

// Disk Chart
if (systemInfo.value.disk) {
  const diskChart = echarts.init(document.getElementById('disk-chart'));
  const diskOption = {
    title: {
      text: '磁盘使用情况 (GB)',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} GB'
    },
    series: [
      {
        name: '磁盘',
        type: 'pie',
        radius: '70%',
        data: [
          { value: systemInfo.value.disk.used, name: '已使用' },
          { value: systemInfo.value.disk.free, name: '空闲' }
        ],
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  diskChart.setOption(diskOption);
}

// Memory Chart
if (systemInfo.value.memory) {

  const memoryChart = echarts.init(document.getElementById('memory-chart'));
  const memoryOption = {
    title: {
      text: '内存使用情况 (GB)',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} GB'
    },
    series: [
      {
        name: '内存',
        type: 'pie',
        radius: '70%',
        data: [
          { value: systemInfo.value.memory.used, name: '已使用' },
          { value: systemInfo.value.memory.free, name: '空闲' }
        ],
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  memoryChart.setOption(memoryOption);
}

// Network Chart
if (systemInfo.value.network) {
const networkChart = echarts.init(document.getElementById('network-chart'));
  const networkOption = {
    title: {
      text: '网络流量 (Bytes)',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c} Bytes'
    },
    xAxis: {
      type: 'time',
      boundaryGap: false
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '发送',
        type: 'line',
        data: [],
        smooth: true,
        showSymbol: false,
        areaStyle: {}
      },
      {
        name: '接收',
        type: 'line',
        data: [],
        smooth: true,
        showSymbol: false,
        areaStyle: {}
      }
    ]
  };
  // 假设存储历史数据
  if (!networkChart._networkData) {
    networkChart._networkData = {
      sent: [],
      recv: []
    };
  }
  networkChart._networkData.sent.push([new Date().getTime(), systemInfo.value.network.sent_packets]);
  networkChart._networkData.recv.push([new Date().getTime(), systemInfo.value.network.recv_packets]);
  // 只保留最近的 10 个数据点
  if (networkChart._networkData.sent.length > 10) {
    networkChart._networkData.sent.shift();
  }
  if (networkChart._networkData.recv.length > 10) {
    networkChart._networkData.recv.shift();
  }
  networkOption.series[0].data = networkChart._networkData.sent;
  networkOption.series[1].data = networkChart._networkData.recv;
  networkChart.setOption(networkOption);
}
};

// 4 定时请求数据
const startPolling = () => {
  getServerData();
  pollInterval = setInterval(getServerData, 5000)
};
// 5 组价挂载时开启定时器
onMounted(() => {
  startPolling();
});
// 6 组件销毁时清理定时器
onBeforeUnmount(() => {
  if (pollInterval) clearInterval(pollInterval);
});

</script>


<style scoped>
.system-info-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}
.system-info-header {
  margin-bottom: 20px;
}
.system-info-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
}
.info-card {
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}
.chart-card {
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}
.chart-container {
  width: 100%;
  height: 300px;
}
</style>