@echo off
REM 修复aerich路径问题的批处理文件
REM 使用当前目录下的虚拟环境Python解释器来运行aerich
.\.venv\Scripts\python.exe .\.venv\Scripts\aerich.exe %* 