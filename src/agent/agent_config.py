from typing import Dict, Optional
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    """Configuration for Customer Service Agent"""
    
    model_name: str = Field(
        default="gpt-4o-mini",
        description="Name of the LLM model to use"
    )

    api_key: str = Field(
        default="",
        description="API key for the LLM model"
    )

    api_base: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM model"
    )
    
    temperature: float = Field(
        default=0.7,
        description="Temperature parameter for LLM responses",
        ge=0.0,
        le=1.0
    )
    
    max_tokens: Optional[int] = Field(
        default=None,
        description="Maximum number of tokens for LLM responses"
    )
    
    verbose: bool = Field(
        default=False,
        description="Whether to print verbose output"
    )
    
    cache: bool = Field(
        default=True,
        description="Whether to cache LLM responses"
    )
    
    knowledge_base_config: Optional[Dict] = Field(
        default=None,
        description="Configuration for knowledge base integration"
    )
    
    @classmethod
    def default_config(cls) -> "AgentConfig":
        """Create default agent configuration"""
        return cls(
            model_name="gpt-4o-mini",
            temperature=0.7,
            verbose=False,
            cache=True
        )
