<p align="center">
  <a href="https://github.com/cyclone-mind/Kong_OA/"><img src="Kong_OA_Front\public\favicon.svg" width="200" height="200" alt="github"></a>
</p>

<div align="center">

# Kong OA

[![license](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)[![github stars](https://img.shields.io/github/stars/cyclone-mind/Kong_OA)](https://github.com/cyclone-mind/Kong_OA)[![github forks](https://img.shields.io/github/forks/cyclone-mind/Kong_OA)](https://github.com/cyclone-mind/Kong_OA)![python](https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=edb641)![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)

![Pydantic](https://img.shields.io/badge/Pydantic-005571?logo=pydantic&logoColor=white)![Vue.js](https://img.shields.io/badge/Vue.js-35495E?logo=vue.js&logoColor=4FC08D)


<span>English | <a href="./README.md">中文</a></span>

</div>

> [!NOTE]
> If you find `Kong_OA` helpful, please give us a ⭐️ on GitHub. Your support is our motivation to keep improving!

## Introduction

`Kong_OA` is an RBAC permission management system based on FastAPI and Vue3, adopting a front-end and back-end separation architecture. The back-end uses FastAPI to provide high-performance API services, and the front-end uses Vue3 to build responsive user interfaces. The system implements complete role-permission-user management functions, suitable as a development foundation for enterprise-level permission management systems.

## Features

- **RBAC Permission Control**: Complete Role-Based Access Control (RBAC) implementation
- **Front-end and Back-end Separation**: Modern architecture with Vue3 for front-end and FastAPI for back-end
- **High-performance Back-end**: Asynchronous API service based on FastAPI
- **Responsive Front-end**: Modern user interface built with Vue3
- **Comprehensive API Documentation**: Automatically generated OpenAPI documentation
- **Easy to Extend**: Modular design for easy functionality extension

## Technology Stack

### Back-end

- Python 3.10+
- FastAPI
- Pydantic
- SQLAlchemy
- JWT Authentication

### Front-end

- Vue 3
- TypeScript
- Pinia
- Element Plus

## Quick Start

### Environment Preparation

- Python 3.10+
- Node.js 16+
- MySQL 5.7+

### Environment Configuration

The project uses a `.env` file for environment configuration. You need to properly set up environment variables before launching the project.

1. Find the `.env.example` file in the `Kong_OA_Backend/src` directory
2. Copy this file and rename it to `.env`
3. Fill in the configuration parameters according to your actual environment

```bash
# Application server configuration
APP_PORT=8080            # Application port
APP_HOST=127.0.0.1       # Application host

# Database configuration
DB_HOST=127.0.0.1        # Database host address
DB_USER=root             # Database username
DB_PASSWORD=yourpassword # Database password
DB_PORT=3306             # Database port
DB_DATABASE=kong_oa      # Database name
```

Note: The `.env` file contains sensitive information and has been added to the `.gitignore` file, so it will not be committed to the repository. Please make sure to configure this file correctly during deployment.

### Starting the Front-end

```bash
cd Kong_OA_Front
npm install
npm run dev
```

### Starting the Back-end

```bash
cd Kong_OA_Backend
pip install -r requirements.txt
python main.py
```

## Project Structure

```text
Kong_OA/
├── backend/            # Back-end code
│   ├── app/           # Application core
│   ├── models/        # Data models
│   ├── routers/       # API routes
│   └── main.py        # Application entry
├── frontend/          # Front-end code
│   ├── public/        
│   ├── src/
│   └── package.json
└── README.md          # Project description
```

## TODO

- [x] Role Management
- [x] Permission Management
- [x] User Management

## How to Contribute

We welcome any form of contribution! If you would like to participate in project development, please follow these steps:

1. Fork this project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a Pull Request

## Contributors

Thanks to all developers who have contributed to the project:

## Star Trend

[![Star History Chart](https://api.star-history.com/svg?repos=cyclone-mind/Kong_OA&type=Date)](https://star-history.com/#cyclone-mind/Kong_OA&Date)

## License

This project is open source under the [MIT License](./LICENSE), please refer to the LICENSE file for details.
