"""
Memory Tool Configurations - Centralized Configuration
Mục đích: Configuration-driven tool creation với zero duplication
"""

from typing import Dict, Any


# =================== CORE MEMORY TOOL CONFIGURATIONS ===================

MEMORY_TOOL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "store_project_requirement": {
        "name": "store_project_requirement",
        "description": "Lưu project requirement vào memory system với automatic analysis",
        "service_method": "store_project_requirement",
        "operation_name": "lưu project requirement",
        "schema": {
            "type": "object",
            "properties": {
                "requirement": {
                    "type": "string",
                    "description": "Chi tiết requirement cần lưu"
                },
                "project_name": {
                    "type": "string",
                    "description": "Tên project"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Mức độ ưu tiên",
                    "default": "medium"
                }
            },
            "required": ["requirement", "project_name"]
        },
        "required": ["requirement", "project_name"]
    },
    
    "store_feature_dependency": {
        "name": "store_feature_dependency",
        "description": "Lưu dependency giữa các features với impact analysis",
        "service_method": "store_feature_dependency",
        "operation_name": "lưu feature dependency",
        "schema": {
            "type": "object",
            "properties": {
                "feature_a": {
                    "type": "string",
                    "description": "Feature thứ nhất"
                },
                "feature_b": {
                    "type": "string",
                    "description": "Feature thứ hai"
                },
                "relationship_type": {
                    "type": "string",
                    "enum": ["depends_on", "conflicts_with", "enhances", "blocks", "related_to"],
                    "description": "Loại relationship"
                },
                "risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Mức độ rủi ro",
                    "default": "medium"
                }
            },
            "required": ["feature_a", "feature_b", "relationship_type"]
        },
        "required": ["feature_a", "feature_b", "relationship_type"]
    },
    
    "get_tests_to_run": {
        "name": "get_tests_to_run",
        "description": "Lấy danh sách tests cần chạy dựa trên modified features",
        "service_method": "get_tests_to_run",
        "operation_name": "lấy test recommendations",
        "schema": {
            "type": "object",
            "properties": {
                "modified_features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách features đã sửa đổi"
                }
            },
            "required": ["modified_features"]
        },
        "required": ["modified_features"]
    },
    
    "get_related_features": {
        "name": "get_related_features",
        "description": "Tìm các features liên quan đến feature đã cho",
        "service_method": "get_related_features",
        "operation_name": "tìm related features",
        "schema": {
            "type": "object",
            "properties": {
                "feature": {
                    "type": "string",
                    "description": "Tên feature cần tìm related"
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth cho graph traversal",
                    "default": 2,
                    "minimum": 1,
                    "maximum": 5
                }
            },
            "required": ["feature"]
        },
        "required": ["feature"]
    },
    
    "search_memory": {
        "name": "search_memory",
        "description": "Tìm kiếm trong memory system bằng natural language",
        "service_method": "search_memory",
        "operation_name": "tìm kiếm memory",
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Từ khóa tìm kiếm"
                },
                "limit": {
                    "type": "integer",
                    "description": "Số kết quả tối đa",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50
                }
            },
            "required": ["query"]
        },
        "required": ["query"]
    },
    
    "store_bug_report": {
        "name": "store_bug_report",
        "description": "Lưu bug report với automatic categorization",
        "service_method": "store_bug_report",
        "operation_name": "lưu bug report",
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Tiêu đề bug"},
                "description": {"type": "string", "description": "Mô tả chi tiết bug"},
                "severity": {
                    "type": "string",
                    "enum": ["trivial", "minor", "major", "critical", "blocker"],
                    "description": "Mức độ nghiêm trọng"
                },
                "affected_features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Các features bị ảnh hưởng"
                }
            },
            "required": ["title", "description", "severity"]
        },
        "required": ["title", "description", "severity"]
    },
    
    "store_code_change": {
        "name": "store_code_change",
        "description": "Lưu code change với impact analysis",
        "service_method": "store_code_change",
        "operation_name": "lưu code change",
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Tiêu đề thay đổi"},
                "change_type": {
                    "type": "string",
                    "enum": ["new_feature", "enhancement", "bug_fix", "refactor", "performance", "security"],
                    "description": "Loại thay đổi"
                },
                "file_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách files đã thay đổi"
                },
                "lines_added": {"type": "integer", "description": "Số dòng thêm"},
                "lines_removed": {"type": "integer", "description": "Số dòng xóa"}
            },
            "required": ["title", "change_type", "file_paths"]
        },
        "required": ["title", "change_type", "file_paths"]
    },
    
    "store_user_feedback": {
        "name": "store_user_feedback",
        "description": "Lưu user feedback với automatic categorization",
        "service_method": "store_user_feedback",
        "operation_name": "lưu user feedback",
        "schema": {
            "type": "object",
            "properties": {
                "feedback_type": {
                    "type": "string",
                    "enum": ["bug_report", "feature_request", "improvement", "question", "compliment"],
                    "description": "Loại feedback"
                },
                "title": {"type": "string", "description": "Tiêu đề feedback"},
                "description": {"type": "string", "description": "Nội dung feedback chi tiết"},
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Mức độ ưu tiên"
                }
            },
            "required": ["feedback_type", "title", "description"]
        },
        "required": ["feedback_type", "title", "description"]
    },
    
    "get_bug_impact_analysis": {
        "name": "get_bug_impact_analysis",
        "description": "Phân tích comprehensive impact của bug",
        "service_method": "get_bug_impact_analysis",
        "operation_name": "analyze bug impact",
        "schema": {
            "type": "object",
            "properties": {
                "bug_id": {"type": "string", "description": "Bug ID cần phân tích"}
            },
            "required": ["bug_id"]
        },
        "required": ["bug_id"]
    }
}


# =================== ADVANCED TOOL CONFIGURATIONS ===================

ADVANCED_TOOL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "get_change_impact_analysis": {
        "name": "get_change_impact_analysis",
        "description": "Phân tích impact của code changes và recommend testing strategy",
        "service_method": "analyze_change_impact",
        "operation_name": "analyze change impact",
        "schema": {
            "type": "object",
            "properties": {
                "file_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách file paths đã thay đổi"
                },
                "change_type": {
                    "type": "string",
                    "enum": ["new_feature", "enhancement", "bug_fix", "refactor", "performance", "security"],
                    "description": "Loại thay đổi"
                }
            },
            "required": ["file_paths"]
        },
        "required": ["file_paths"]
    },
    
    "get_regression_risk": {
        "name": "get_regression_risk",
        "description": "Assess regression risk và recommend mitigation strategies",
        "service_method": "assess_regression_risk",
        "operation_name": "assess regression risk",
        "schema": {
            "type": "object",
            "properties": {
                "changed_features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách feature IDs đã thay đổi"
                },
                "change_scope": {
                    "type": "string",
                    "enum": ["small", "medium", "large"],
                    "description": "Phạm vi thay đổi"
                }
            },
            "required": ["changed_features"]
        },
        "required": ["changed_features"]
    },
    
    "get_documents_to_update": {
        "name": "get_documents_to_update",
        "description": "Lấy danh sách documents cần update dựa trên code/feature changes",
        "service_method": "get_documents_to_update",
        "operation_name": "get documents to update",
        "schema": {
            "type": "object",
            "properties": {
                "feature_changes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách features đã thay đổi"
                },
                "code_changes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách code files đã thay đổi"
                }
            },
            "required": ["feature_changes", "code_changes"]
        },
        "required": ["feature_changes", "code_changes"]
    },
    
    "get_comprehensive_test_plan": {
        "name": "get_comprehensive_test_plan",
        "description": "Tạo comprehensive test plan dựa trên code/feature/doc changes",
        "service_method": "get_comprehensive_test_plan",
        "operation_name": "create comprehensive test plan",
        "schema": {
            "type": "object",
            "properties": {
                "code_changes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách code files đã thay đổi"
                },
                "feature_changes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Danh sách features đã thay đổi"
                },
                "risk_level": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Mức độ rủi ro của thay đổi"
                }
            },
            "required": ["code_changes", "feature_changes"]
        },
        "required": ["code_changes", "feature_changes"]
    }
}


# =================== HELPER FUNCTIONS ===================

def get_all_tool_configs() -> Dict[str, Dict[str, Any]]:
    """Get all tool configurations"""
    return {**MEMORY_TOOL_CONFIGS, **ADVANCED_TOOL_CONFIGS}


def get_tool_config(tool_name: str) -> Dict[str, Any]:
    """Get specific tool configuration"""
    all_configs = get_all_tool_configs()
    if tool_name not in all_configs:
        raise ValueError(f"Tool '{tool_name}' not found in configurations")
    return all_configs[tool_name]


def get_tool_names() -> list[str]:
    """Get all available tool names"""
    return list(get_all_tool_configs().keys())
