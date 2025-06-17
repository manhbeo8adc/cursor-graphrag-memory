"""
Base MCP Tool Classes - Abstract Foundation
Mục đích: SOLID principles foundation cho all MCP tools
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..utils.logger import get_logger


class MCPToolBase(ABC):
    """
    Abstract base class cho tất cả MCP tools
    SRP: Chỉ define interface, không implement logic
    OCP: Open for extension, closed for modification
    LSP: Subclasses phải implement consistent interface
    """
    
    # Class attributes - sẽ được set bởi subclasses
    name: str = ""
    description: str = ""
    input_schema: Dict[str, Any] = {}
    
    def __init__(self):
        """Initialize base tool"""
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    async def execute(self, arguments: Dict[str, Any]) -> str:
        """
        Execute tool logic - phải được implement bởi subclasses
        LSP: Tất cả subclasses phải return string
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get tool schema for MCP registration
        Template method pattern
        """
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": self.input_schema.get("properties", {}),
                "required": self.input_schema.get("required", [])
            }
        }
    
    def validate_arguments(self, arguments: Dict[str, Any]) -> bool:
        """
        Validate tool arguments against schema
        Template method pattern - common validation logic
        """
        required_fields = self.input_schema.get("required", [])
        
        for field in required_fields:
            if field not in arguments:
                raise ValueError(f"Missing required field: {field}")
        
        return True
    
    def __str__(self) -> str:
        """String representation for debugging"""
        return f"{self.__class__.__name__}(name='{self.name}')"


class MCPToolRegistry:
    """
    Registry cho MCP tools - Singleton pattern
    SRP: Chỉ lo việc manage tool registry
    """
    
    def __init__(self):
        """Initialize empty registry"""
        self._tools: Dict[str, MCPToolBase] = {}
        self.logger = get_logger(__name__)
    
    def register_tool(self, tool: MCPToolBase) -> None:
        """
        Register a tool in the registry
        OCP: Easy to add new tools without modifying existing code
        """
        if not isinstance(tool, MCPToolBase):
            raise TypeError(f"Tool must inherit from MCPToolBase, got {type(tool)}")
        
        if not tool.name:
            raise ValueError(f"Tool {tool.__class__.__name__} must have a name")
        
        self._tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> MCPToolBase:
        """
        Get tool by name
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry")
        return self._tools[name]
    
    def get_all_tools(self) -> Dict[str, MCPToolBase]:
        """
        Get all registered tools
        """
        return self._tools.copy()
    
    def get_tool_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Get schemas for all registered tools
        """
        return {name: tool.get_schema() for name, tool in self._tools.items()}
    
    def list_tool_names(self) -> list[str]:
        """
        Get list of all tool names
        """
        return list(self._tools.keys())


class MCPToolExecutor:
    """
    Executor cho MCP tools với error handling
    SRP: Chỉ lo việc execute tools safely
    """
    
    def __init__(self, registry: MCPToolRegistry):
        """Initialize executor với registry"""
        self.registry = registry
        self.logger = get_logger(__name__)
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute tool với comprehensive error handling
        Template method pattern với error handling
        """
        try:
            # Get tool from registry
            tool = self.registry.get_tool(tool_name)
            
            # Validate arguments
            tool.validate_arguments(arguments)
            
            # Execute tool
            self.logger.info(f"Executing tool: {tool_name} with args: {list(arguments.keys())}")
            result = await tool.execute(arguments)
            
            # Ensure result is string
            if not isinstance(result, str):
                result = str(result)
            
            self.logger.info(f"Tool {tool_name} executed successfully")
            return result
            
        except KeyError as e:
            error_msg = f"❌ Tool '{tool_name}' not found: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
            
        except ValueError as e:
            error_msg = f"❌ Invalid arguments for tool '{tool_name}': {str(e)}"
            self.logger.error(error_msg)
            return error_msg
            
        except Exception as e:
            error_msg = f"❌ Error executing tool '{tool_name}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg
    
    def get_available_tools(self) -> Dict[str, str]:
        """
        Get available tools với descriptions
        """
        return {
            name: tool.description 
            for name, tool in self.registry.get_all_tools().items()
        }
