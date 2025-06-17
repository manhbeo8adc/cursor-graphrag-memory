# Cursor GraphRAG Memory System - MCP Server

> **🎯 Mục tiêu chính**: Khi yêu cầu thêm tính năng mới, feedback sửa tính năng cũ hoặc report bug thì Cursor sẽ **tự động cập nhật những phần liên quan** (cả code lẫn tài liệu) và **chạy các unittest** để đảm bảo code cũ không bị ảnh hưởng và tài liệu luôn up-to-date

## 🌟 Key Features

### 📊 Intelligent Capabilities
- 🔍 **Intelligent Impact Analysis**: Tự động phân tích tác động của thay đổi
- 🧪 **Smart Test Recommendations**: Gợi ý tests cần chạy dựa trên code changes
- 📝 **Auto Documentation Updates**: Cập nhật docs khi code thay đổi
- 🐛 **Bug Tracking & Root Cause Analysis**: Theo dõi bugs và phân tích nguyên nhân
- 🔗 **Dependency Tracking**: Hiểu mối quan hệ giữa features, bugs, tests
- ⚡ **Performance Monitoring**: Track performance impact của changes
- 🛡️ **Quality Assurance**: Đảm bảo code cũ không bị ảnh hưởng
- 🤖 **Natural Language Processing**: Chat với AI để get insights

### 🏗️ Architecture Highlights
- **11 Core Entities**: ProjectRequirement, Feature, Bug, CodeChange, Test, TestResult, UserFeedback, DocumentEntity, CodeFileEntity, TestCoverage, EntityRelationship
- **17 Relationship Types**: Comprehensive tracking cho docs + code + features + bugs
- **Factory Pattern**: Zero code duplication, trivial adding new tools
- **SOLID Principles**: Clean, maintainable, extensible architecture
- **Gemini-2.5-Flash**: Cost-effective AI integration

## 🚀 Quick Start (GitHub Codespaces)

### 1. Open in Codespaces
```bash
# Tự động setup environment với .devcontainer
# Open repository in GitHub Codespaces
```

### 2. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys:
# GEMINI_API_KEY=your_gemini_api_key_here
# DATABASE_URL=postgresql://... (Railway will provide)
# REDIS_URL=redis://... (Railway will provide)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run MCP Server
```bash
python src/main.py
```

### 5. Connect from Cursor IDE
Add to your Cursor IDE MCP settings:
```json
{
  "mcpServers": {
    "cursor-graphrag-memory": {
      "command": "python",
      "args": ["path/to/src/main.py"],
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

## 🛠️ Available Tools

### 📝 Core Memory Tools
- `store_project_requirement`: Lưu project requirement với automatic analysis
- `store_feature_dependency`: Lưu dependency giữa features với impact analysis
- `store_bug_report`: Lưu bug report với automatic categorization
- `store_code_change`: Lưu code change với comprehensive impact analysis
- `store_user_feedback`: Lưu user feedback với automatic categorization

### 🔍 Query & Analysis Tools
- `get_tests_to_run`: Lấy danh sách tests cần chạy dựa trên modified features
- `get_related_features`: Tìm các features liên quan đến feature đã cho
- `search_memory`: Tìm kiếm trong memory system bằng natural language
- `get_bug_impact_analysis`: Phân tích comprehensive impact của bug

### 🎯 Advanced Analysis Tools
- `get_change_impact_analysis`: Phân tích impact của code changes và recommend testing strategy
- `get_regression_risk`: Assess regression risk và recommend mitigation strategies
- `get_documents_to_update`: Lấy danh sách documents cần update dựa trên code/feature changes
- `get_comprehensive_test_plan`: Tạo comprehensive test plan dựa trên code/feature/doc changes

### 🤖 AI Tools
- `natural_language_handler`: Chat với AI assistant để get insights và recommendations

## 📊 Data Model Overview

### Core Entities (11)
```python
# Project Management
ProjectRequirement, Feature, Bug, CodeChange, Test, TestResult, UserFeedback

# Documentation & Code Tracking (NEW)
DocumentEntity, CodeFileEntity, TestCoverage, EntityRelationship
```

### Relationship Types (17)
```python
# Original relationships
depends_on, conflicts_with, enhances, blocks, related_to, implements, tests, fixes, caused_by

# Enhanced relationships for docs/code tracking
documents, described_by, covers, covered_by, imports, imported_by, references, referenced_by
```

## 🎯 Usage Examples

### Example 1: Adding New Feature
```python
# 1. Store requirement
result = await call_tool("store_project_requirement", {
    "requirement": "Add user authentication with OAuth2",
    "project_name": "MyApp",
    "priority": "high"
})

# 2. Store feature dependencies
result = await call_tool("store_feature_dependency", {
    "feature_a": "user_auth",
    "feature_b": "user_profile",
    "relationship_type": "depends_on",
    "risk_level": "medium"
})

# 3. Get comprehensive test plan
result = await call_tool("get_comprehensive_test_plan", {
    "code_changes": ["src/auth/oauth.py", "src/auth/middleware.py"],
    "feature_changes": ["user_auth"],
    "risk_level": "high"
})
```

### Example 2: Bug Reporting & Impact Analysis
```python
# 1. Store bug report
result = await call_tool("store_bug_report", {
    "title": "Login fails with special characters in password",
    "description": "Users cannot login when password contains @#$ characters",
    "severity": "major",
    "affected_features": ["user_auth", "password_validation"]
})

# 2. Get comprehensive impact analysis
result = await call_tool("get_bug_impact_analysis", {
    "bug_id": "bug_12345678"
})

# 3. Get documents that need updating
result = await call_tool("get_documents_to_update", {
    "feature_changes": ["user_auth"],
    "code_changes": ["src/auth/validation.py"]
})
```

### Example 3: Natural Language Interaction
```python
# Chat with AI assistant
result = await call_tool("natural_language_handler", {
    "message": "I just fixed a bug in the payment system. What tests should I run and what docs need updating?"
})

# AI will analyze and provide specific recommendations
```

## 🏗️ Architecture Details

### SOLID Principles Implementation
- **SRP**: Each class has single responsibility
- **OCP**: Adding tools only requires inheriting MCPToolBase + factory addition
- **LSP**: Consistent tool interfaces
- **ISP**: Small, focused interfaces
- **DIP**: Dependency injection throughout

### Factory Pattern Benefits
- **Zero Duplication**: BaseMemoryTool eliminates 90% code duplication
- **Trivial Adding**: New tools only need configuration entry
- **Consistent Behavior**: Template method pattern ensures consistency
- **Easy Testing**: Mock services for development

### Key Components
- `MCPToolBase`: Abstract base class with class attributes
- `MCPToolRegistry`: Tool registration and management
- `MCPToolExecutor`: Safe tool execution with error handling
- `MCPToolFactory`: Dependency injection and tool creation
- `GraphitiMCPServer`: Pure MCP protocol handling
- `MCPServerBootstrap`: Orchestration and dependency management

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_memory_service.py -v
```

## 🚀 Deployment

### Railway Deployment
1. Connect GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on push to main

### Docker Deployment
```bash
# Build image
docker build -t cursor-graphrag-memory .

# Run container
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e DATABASE_URL=your_db_url \
  -e REDIS_URL=your_redis_url \
  cursor-graphrag-memory
```

## 🤝 Contributing

### Adding New Tools
1. Add configuration to `src/config/memory_tool_configs.py`
2. Implement service method in `MemoryService` if needed
3. That's it! Factory pattern handles the rest.

### Adding New Entities
1. Add dataclass to `src/models/memory_models.py`
2. Add relationships if needed
3. Update service methods to handle new entity

## 📋 TODO
- [ ] Integrate with actual Graphiti database
- [ ] Add real-time notifications
- [ ] Implement caching with Redis
- [ ] Add metrics and monitoring
- [ ] Expand test coverage
- [ ] Add API documentation

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: This README + inline code comments
- **Architecture**: See `GraphRAG-Setup-Guide.md` for detailed setup

---

**Happy coding với Intelligent Cursor + GraphRAG! 🎉**
