// 这是一个测试文件,包含一些示例代码

// 定义一个简单的类
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    sayHello() {
        console.log(`你好,我是${this.name},今年${this.age}岁`);
    }
}

// 创建一个数组处理函数
const processArray = (arr) => {
    return arr.map(item => item * 2)
            .filter(item => item > 10)
            .reduce((acc, curr) => acc + curr, 0);
};

// 异步函数示例
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('获取数据失败:', error);
    }
}

// 使用示例
const person = new Person('张三', 25);
person.sayHello();

const numbers = [2, 4, 6, 8, 10];
console.log('数组处理结果:', processArray(numbers));

// 导出一些工具函数
export const utils = {
    formatDate: (date) => {
        return new Date(date).toLocaleDateString('zh-CN');
    },
    randomNumber: (min, max) => {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
};



console.log("hello, world!");


console.log("Not a world!");


console.log("This is world!");


