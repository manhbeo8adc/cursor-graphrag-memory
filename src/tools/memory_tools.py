"""
Intelligent Memory Tools Implementation - Hỗ trợ mục tiêu tự động hóa
Factory pattern eliminates duplication và enables rapid tool expansion
Supports: Auto-analysis, Smart recommendations, Dependency tracking, Test suggestions
"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod
from .base_mcp_tool import MCPToolBase
from ..services.memory_service import MemoryService
from ..services.nlp_service import NLPService
from ..config.memory_tool_configs import MEMORY_TOOL_CONFIGS, ADVANCED_TOOL_CONFIGS
from ..utils.logger import get_logger


# =================== BASE MEMORY TOOL ===================

class BaseMemoryTool(MCPToolBase, ABC):
    """
    Base class cho memory tools với common logic
    Eliminates duplicate error handling và validation
    Template method pattern for consistent behavior
    """
    
    def __init__(self, service: Any, tool_config: Dict[str, Any]):
        """Initialize base memory tool với service và config"""
        super().__init__()
        self.service = service
        self.config = tool_config
        
        # Set class attributes từ config
        self.name = tool_config["name"]
        self.description = tool_config["description"]
        self.input_schema = tool_config["schema"]
        
        self.logger = get_logger(f"{__name__}.{self.name}")
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        """
        Common execute logic với error handling
        Template method pattern - consistent across all tools
        """
        try:
            # Validate required fields (already done by base class)
            self._validate_tool_specific_inputs(arguments)
            
            # Log execution start
            self.logger.info(f"Executing {self.name} with arguments: {list(arguments.keys())}")
            
            # Execute specific tool logic
            result = await self._execute_tool_logic(arguments)
            
            # Format result consistently
            formatted_result = self._format_result(result, arguments)
            
            self.logger.info(f"Successfully executed {self.name}")
            return formatted_result
            
        except Exception as e:
            error_msg = self._format_error(str(e))
            self.logger.error(f"Error in {self.name}: {str(e)}", exc_info=True)
            return error_msg
    
    def _validate_tool_specific_inputs(self, arguments: Dict[str, Any]) -> None:
        """
        Tool-specific validation - can be overridden
        Template method pattern
        """
        # Default implementation - no additional validation
        pass
    
    @abstractmethod
    async def _execute_tool_logic(self, arguments: Dict[str, Any]) -> Any:
        """
        Tool-specific logic - implemented by subclasses
        Strategy pattern - each tool has different strategy
        """
        pass
    
    def _format_result(self, result: Any, arguments: Dict[str, Any]) -> str:
        """
        Default result formatting - can be overridden
        Template method pattern
        """
        if isinstance(result, str):
            return result
        
        # Default formatting for non-string results
        success_template = self.config.get("success_template", "✅ {operation} hoàn thành thành công")
        operation = self.config.get("operation_name", "Operation")
        return success_template.format(operation=operation, result=result, **arguments)
    
    def _format_error(self, error: str) -> str:
        """
        Common error formatting - consistent across all tools
        """
        operation = self.config.get("operation_name", "thực hiện")
        return f"❌ Lỗi khi {operation}: {error}"


# =================== SERVICE METHOD DELEGATOR ===================

class ServiceMethodTool(BaseMemoryTool):
    """
    Generic tool that delegates to service methods
    Eliminates need for individual tool classes
    Strategy pattern - delegates to different service methods
    """
    
    async def _execute_tool_logic(self, arguments: Dict[str, Any]) -> Any:
        """
        Delegate to configured service method
        Strategy pattern - method determined by configuration
        """
        method_name = self.config["service_method"]
        
        # Get method from service
        if not hasattr(self.service, method_name):
            raise AttributeError(f"Service does not have method: {method_name}")
        
        method = getattr(self.service, method_name)
        
        # Extract method arguments từ config
        method_args = self._extract_method_args(arguments)
        
        # Call service method
        if asyncio.iscoroutinefunction(method):
            return await method(**method_args)
        else:
            return method(**method_args)
    
    def _extract_method_args(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract và map arguments cho service method
        Adapter pattern - adapts tool args to service args
        """
        arg_mapping = self.config.get("arg_mapping", {})
        
        if arg_mapping:
            # Use custom mapping
            return {
                service_arg: arguments[input_arg] 
                for service_arg, input_arg in arg_mapping.items()
                if input_arg in arguments
            }
        else:
            # Direct mapping - tool args = service args
            return arguments


# =================== SPECIAL TOOLS ===================

class NaturalLanguageHandlerTool(BaseMemoryTool):
    """
    Special tool cho NLP - uses different service
    Strategy pattern - different service strategy
    """
    
    def __init__(self, nlp_service: NLPService):
        """Initialize NLP tool với NLP service"""
        config = {
            "name": "natural_language_handler",
            "description": "Xử lý natural language messages từ user và provide intelligent responses",
            "operation_name": "xử lý natural language",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Natural language message từ user"
                    }
                },
                "required": ["message"]
            },
            "required": ["message"]
        }
        super().__init__(nlp_service, config)
    
    async def _execute_tool_logic(self, arguments: Dict[str, Any]) -> Any:
        """
        Delegate to NLP service
        Strategy pattern - NLP-specific processing
        """
        message = arguments["message"]
        return await self.service.process_natural_language(message)
    
    def _validate_tool_specific_inputs(self, arguments: Dict[str, Any]) -> None:
        """
        NLP-specific validation
        """
        message = arguments.get("message", "")
        if not message.strip():
            raise ValueError("Message cannot be empty")
        
        if len(message) > 5000:
            raise ValueError("Message too long (max 5000 characters)")


# =================== MEMORY TOOL FACTORY ===================

class MemoryToolFactory:
    """
    Factory để create memory tools từ configuration
    Eliminates duplicate code và makes adding tools trivial
    Factory pattern - creates tools based on configuration
    """
    
    def __init__(self, memory_service: MemoryService, nlp_service: NLPService):
        """Initialize factory với services"""
        self.memory_service = memory_service
        self.nlp_service = nlp_service
        self.logger = get_logger(__name__)
    
    def create_all_memory_tools(self) -> List[MCPToolBase]:
        """
        Create all memory tools từ configuration
        Factory pattern - mass production of tools
        Adding new tools chỉ cần add config entry
        """
        tools = []
        
        # Create basic memory tools
        basic_tools = self._create_basic_memory_tools()
        tools.extend(basic_tools)
        
        # Create advanced tools
        advanced_tools = self._create_advanced_memory_tools()
        tools.extend(advanced_tools)
        
        # Create special tools
        special_tools = self._create_special_tools()
        tools.extend(special_tools)
        
        self.logger.info(f"Created {len(tools)} memory tools")
        return tools
    
    def _create_basic_memory_tools(self) -> List[MCPToolBase]:
        """
        Create basic memory tools from MEMORY_TOOL_CONFIGS
        """
        tools = []
        
        for tool_name, config in MEMORY_TOOL_CONFIGS.items():
            try:
                tool = ServiceMethodTool(self.memory_service, config)
                tools.append(tool)
                self.logger.info(f"Created basic tool: {tool_name}")
            except Exception as e:
                self.logger.error(f"Failed to create basic tool {tool_name}: {e}")
        
        return tools
    
    def _create_advanced_memory_tools(self) -> List[MCPToolBase]:
        """
        Create advanced memory tools from ADVANCED_TOOL_CONFIGS
        """
        tools = []
        
        for tool_name, config in ADVANCED_TOOL_CONFIGS.items():
            try:
                tool = ServiceMethodTool(self.memory_service, config)
                tools.append(tool)
                self.logger.info(f"Created advanced tool: {tool_name}")
            except Exception as e:
                self.logger.error(f"Failed to create advanced tool {tool_name}: {e}")
        
        return tools
    
    def _create_special_tools(self) -> List[MCPToolBase]:
        """
        Create special tools (NLP, etc.)
        """
        tools = []
        
        try:
            # Natural Language Handler
            nlp_tool = NaturalLanguageHandlerTool(self.nlp_service)
            tools.append(nlp_tool)
            self.logger.info("Created special tool: natural_language_handler")
        except Exception as e:
            self.logger.error(f"Failed to create NLP tool: {e}")
        
        return tools
    
    def create_tool_by_name(self, tool_name: str) -> MCPToolBase:
        """
        Create a specific tool by name
        Factory method pattern
        """
        # Check basic tools
        if tool_name in MEMORY_TOOL_CONFIGS:
            config = MEMORY_TOOL_CONFIGS[tool_name]
            return ServiceMethodTool(self.memory_service, config)
        
        # Check advanced tools
        if tool_name in ADVANCED_TOOL_CONFIGS:
            config = ADVANCED_TOOL_CONFIGS[tool_name]
            return ServiceMethodTool(self.memory_service, config)
        
        # Check special tools
        if tool_name == "natural_language_handler":
            return NaturalLanguageHandlerTool(self.nlp_service)
        
        raise ValueError(f"Unknown tool name: {tool_name}")
    
    def get_available_tool_names(self) -> List[str]:
        """
        Get all available tool names
        """
        names = []
        names.extend(MEMORY_TOOL_CONFIGS.keys())
        names.extend(ADVANCED_TOOL_CONFIGS.keys())
        names.append("natural_language_handler")
        return names
    
    def add_tool_config(self, tool_name: str, config: Dict[str, Any], 
                       is_advanced: bool = False) -> None:
        """
        Add new tool configuration dynamically
        Open/Closed Principle - extend without modification
        """
        if is_advanced:
            ADVANCED_TOOL_CONFIGS[tool_name] = config
        else:
            MEMORY_TOOL_CONFIGS[tool_name] = config
        
        self.logger.info(f"Added new tool configuration: {tool_name}")


# =================== USAGE EXAMPLE ===================

"""
# Adding a new tool is now trivial:

factory = MemoryToolFactory(memory_service, nlp_service)

# Option 1: Add via configuration
factory.add_tool_config("new_analysis_tool", {
    "name": "new_analysis_tool",
    "description": "Perform new type of analysis",
    "service_method": "perform_new_analysis",
    "operation_name": "perform analysis",
    "schema": {
        "type": "object",
        "properties": {
            "input_data": {"type": "string", "description": "Input for analysis"}
        },
        "required": ["input_data"]
    },
    "required": ["input_data"]
})

# Option 2: Create tool directly
new_tool = factory.create_tool_by_name("new_analysis_tool")

# Zero additional code required!
"""

# Import asyncio for coroutine detection
import asyncio
