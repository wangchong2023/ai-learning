.PHONY: test rag graph mcp clean help

# 默认变量
PYTHON = ./env/venv/bin/python3
PYPATH = PYTHONPATH=.

help:
	@echo "可用命令:"
	@echo "  make test    运行自动化系统测试"
	@echo "  make rag     运行现代化 RAG 应用"
	@echo "  make graph   运行带审批流的智能体"
	@echo "  make mcp     启动工具发布服务 (MCP)"
	@echo "  make clean   清理临时文件和缓存"

test:
	$(PYPATH) $(PYTHON) tests/test_system.py

rag:
	$(PYTHON) rag_app/main.py

graph:
	$(PYTHON) -m langgraph_app.main

mcp:
	$(PYTHON) -m tools.mcp_server

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf rag_app/vector_storage/
	@echo "清理完成。"
