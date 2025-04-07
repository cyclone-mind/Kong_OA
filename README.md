<p align="center">
  <a href="https://github.com/cyclone-mind/Kong_OA/"><img src="Kong_OA_Front\public\favicon.svg" width="200" height="200" alt="github"></a>
</p>

<div align="center">

# Kong OA

[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)[![github stars](https://img.shields.io/github/stars/cyclone-mind/Kong_OA)](https://github.com/cyclone-mind/Kong_OA)[![github forks](https://img.shields.io/github/forks/cyclone-mind/Kong_OA)](https://github.com/cyclone-mind/Kong_OA)![python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=edb641)![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)

![Pydantic](https://img.shields.io/badge/Pydantic-005571?logo=pydantic&logoColor=white)![Vue.js](https://img.shields.io/badge/Vue.js-35495E?logo=vue.js&logoColor=4FC08D)


<span><a href="./README.en.md">English</a> | 中文</span>

</div>

> [!NOTE]
> 如果您觉得 `Kong_OA` 对您有所帮助，请在 GitHub 上给我们一个 ⭐️。您的支持是我们持续改进的动力！

## 简介

`Kong_OA` 是一个基于 FastAPI 和 Vue3 的 RBAC 权限管理系统，采用前后端分离架构。后端使用 FastAPI 提供高性能 API 服务，前端使用 Vue3 构建响应式用户界面。系统实现了完整的角色-权限-用户管理功能，适合作为企业级权限管理系统的开发基础。

## 特性

- **RBAC 权限控制**：完整的基于角色的访问控制(RBAC)实现
- **前后端分离**：前端 Vue3 + 后端 FastAPI 的现代化架构
- **高性能后端**：基于 FastAPI 的异步 API 服务
- **响应式前端**：Vue3 构建的现代化用户界面
- **完善的API文档**：自动生成的 OpenAPI 文档
- **易于扩展**：模块化设计，便于功能扩展

## 技术栈

### 后端

- Python 3.10+
- FastAPI
- Pydantic
- SQLAlchemy
- JWT 认证

### 前端

- Vue 3
- TypeScript
- Pinia
- Element Plus

## 快速开始

### 环境准备

- Python 3.10+
- Node.js 16+
- MySQL 5.7+

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 后端启动

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## 项目结构

```text
Kong_OA/
├── backend/            # 后端代码
│   ├── app/           # 应用核心
│   ├── models/        # 数据模型
│   ├── routers/       # API路由
│   └── main.py        # 应用入口
├── frontend/          # 前端代码
│   ├── public/        
│   ├── src/
│   └── package.json
└── README.md          # 项目说明
```

## TODO

- [x] 角色管理
- [x] 权限管理
- [x] 用户管理

## 如何贡献

我们欢迎任何形式的贡献！如果您想参与项目开发，请遵循以下步骤：

1. Fork 本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 贡献者

感谢所有为项目做出贡献的开发者：

## Star 趋势

[![Star History Chart](https://api.star-history.com/svg?repos=cyclone-mind/Kong_OA&type=Date)](https://star-history.com/#cyclone-mind/Kong_OA&Date)

## 开源协议

本项目采用 [MIT 许可证](./LICENSE) 开源，详情请参阅 LICENSE 文件。
