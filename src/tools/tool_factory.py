"""
MCP Tool Factory - SOLID Compliant Factory Pattern
Mục đích: Create và manage all MCP tools với dependency injection
"""

from typing import List, Dict, Any, Optional
from .base_mcp_tool import MCPToolBase, MCPToolRegistry, MCPToolExecutor
from .memory_tools import MemoryToolFactory
from ..services.memory_service import MemoryService
from ..services.nlp_service import NLPService
from ..utils.logger import get_logger


class MCPToolFactory:
    """
    Main factory cho tất cả MCP tools
    SRP: Chỉ lo việc create và configure tools
    DIP: Depends on abstractions (services)
    """
    
    def __init__(self, memory_service: MemoryService, nlp_service: NLPService):
        """Initialize factory với services"""
        self.memory_service = memory_service
        self.nlp_service = nlp_service
        self.logger = get_logger(__name__)
        
        # Create sub-factories
        self.memory_tool_factory = MemoryToolFactory(memory_service, nlp_service)
        
        # Create registry and executor
        self.registry = MCPToolRegistry()
        self.executor = MCPToolExecutor(self.registry)
    
    def create_and_register_all_tools(self) -> MCPToolRegistry:
        """
        Create và register tất cả tools
        Factory pattern - mass production và registration
        """
        try:
            # Create all memory tools
            memory_tools = self.memory_tool_factory.create_all_memory_tools()
            
            # Register all tools
            for tool in memory_tools:
                self.registry.register_tool(tool)
            
            self.logger.info(f"Successfully created and registered {len(memory_tools)} tools")
            return self.registry
            
        except Exception as e:
            self.logger.error(f"Failed to create and register tools: {e}", exc_info=True)
            raise
    
    def get_registry(self) -> MCPToolRegistry:
        """Get tool registry"""
        return self.registry
    
    def get_executor(self) -> MCPToolExecutor:
        """Get tool executor"""
        return self.executor
    
    def create_tool_by_name(self, tool_name: str) -> MCPToolBase:
        """
        Create specific tool by name
        Factory method pattern
        """
        try:
            # Try memory tools first
            return self.memory_tool_factory.create_tool_by_name(tool_name)
        except ValueError:
            # Could add other tool types here in the future
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def add_custom_tool(self, tool: MCPToolBase) -> None:
        """
        Add custom tool to registry
        Open/Closed Principle - extend without modification
        """
        self.registry.register_tool(tool)
        self.logger.info(f"Added custom tool: {tool.name}")
    
    def get_tool_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all tool schemas for MCP server registration
        """
        return self.registry.get_tool_schemas()
    
    def get_available_tools(self) -> Dict[str, str]:
        """
        Get available tools với descriptions
        """
        return self.executor.get_available_tools()
    
    def get_tool_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about registered tools
        """
        all_tools = self.registry.get_all_tools()
        
        # Categorize tools
        memory_tools = []
        nlp_tools = []
        other_tools = []
        
        for name, tool in all_tools.items():
            if "memory" in name or any(keyword in name for keyword in 
                                     ["store", "get", "search", "analyze"]):
                memory_tools.append(name)
            elif "natural_language" in name or "nlp" in name:
                nlp_tools.append(name)
            else:
                other_tools.append(name)
        
        return {
            "total_tools": len(all_tools),
            "memory_tools": len(memory_tools),
            "nlp_tools": len(nlp_tools),
            "other_tools": len(other_tools),
            "tool_categories": {
                "memory": memory_tools,
                "nlp": nlp_tools,
                "other": other_tools
            }
        }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute tool với error handling
        Facade pattern - simple interface to complex subsystem
        """
        return await self.executor.execute_tool(tool_name, arguments)
    
    def validate_tool_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate tool configuration
        Template method pattern
        """
        required_fields = ["name", "description", "schema"]
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Tool config missing required field: {field}")
        
        # Validate schema structure
        schema = config["schema"]
        if "type" not in schema or schema["type"] != "object":
            raise ValueError("Tool schema must be object type")
        
        if "properties" not in schema:
            raise ValueError("Tool schema must have properties")
        
        return True
    
    def get_tool_usage_help(self) -> str:
        """
        Get comprehensive help for all tools
        """
        all_tools = self.registry.get_all_tools()
        stats = self.get_tool_statistics()
        
        help_text = f"🛠️ **MCP Tools Help ({stats['total_tools']} tools available)**\n\n"
        
        # Memory Tools
        if stats['tool_categories']['memory']:
            help_text += "🧠 **Memory Tools:**\n"
            for tool_name in stats['tool_categories']['memory']:
                tool = all_tools[tool_name]
                help_text += f"- `{tool_name}`: {tool.description}\n"
            help_text += "\n"
        
        # NLP Tools
        if stats['tool_categories']['nlp']:
            help_text += "💬 **NLP Tools:**\n"
            for tool_name in stats['tool_categories']['nlp']:
                tool = all_tools[tool_name]
                help_text += f"- `{tool_name}`: {tool.description}\n"
            help_text += "\n"
        
        # Other Tools
        if stats['tool_categories']['other']:
            help_text += "🔧 **Other Tools:**\n"
            for tool_name in stats['tool_categories']['other']:
                tool = all_tools[tool_name]
                help_text += f"- `{tool_name}`: {tool.description}\n"
            help_text += "\n"
        
        help_text += "💡 **Usage:** Use any tool name with appropriate arguments via MCP protocol."
        
        return help_text
