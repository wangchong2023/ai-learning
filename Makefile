.PHONY: test rag graph mcp multi clean help

# 默认变量
PYTHON = ./env/bin/python3
PYPATH = PYTHONPATH=source:source/apps:.

help:
	@echo "可用命令:"
	@echo "  make test    运行自动化系统测试"
	@echo "  make rag     运行现代化 RAG 应用"
	@echo "  make graph   运行带审批流的智能体"
	@echo "  make multi   启动多智能体协作实验室"
	@echo "  make plan    运行高级深度规划实验室 (Plan & Execute)"
	@echo "  make mcp     启动工具发布服务 (MCP)"
	@echo "  make clean   清理临时文件和缓存"

test:
	$(PYPATH) $(PYTHON) tests/test_system.py

rag:
	$(PYPATH) $(PYTHON) source/apps/rag_app/main.py

graph:
	$(PYPATH) $(PYTHON) -m apps.langgraph_app.main

multi:
	$(PYPATH) $(PYTHON) source/apps/multi_agent_app/main.py

plan:
	$(PYPATH) $(PYTHON) source/apps/planner_app/main.py

mcp:
	$(PYPATH) $(PYTHON) -m tools.mcp_server

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf rag_app/vector_storage/
	@echo "清理完成。"
