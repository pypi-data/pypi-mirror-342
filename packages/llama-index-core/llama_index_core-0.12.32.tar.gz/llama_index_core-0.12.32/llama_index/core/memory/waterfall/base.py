import asyncio
from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from llama_index.core.base.llms.types import ChatMessage, ContentBlock
from llama_index.core.bridge.pydantic import BaseModel, Field, model_validator
from llama_index.core.memory.chat_memory_buffer import (
    DEFAULT_TOKEN_LIMIT,
    DEFAULT_CHAT_STORE_KEY
)
from llama_index.core.memory.types import BaseChatStoreMemory
from llama_index.core.prompts import BasePromptTemplate, RichPromptTemplate
from llama_index.core.storage.chat_store import BaseChatStore, SimpleChatStore
from llama_index.core.utils import get_tokenizer

DEFAULT_PRESSURE_SIZE = 5
DEFAULT_MEMORY_BLOCKS_TEMPLATE = RichPromptTemplate(
"""
<memory>
{% for (block_name, block_content) in memory_blocks %}
<{{ block_name }}>
{block_content}
</{{ block_name }}>
{% endfor %}
</memory>
"""
)

class InsertMethod(Enum):
    SYSTEM = "system"
    USER = "user"


class BaseMemoryBlock(BaseModel):

    name: str = Field(description="The name/identifier of the memory block.")
    description: Optional[str] = Field(default=None, description="A description of the memory block.")

    @abstractmethod
    async def aget(self, input: Optional[str] = None, **kwargs: Any) -> str:
        """Pull the memory block (async)."""

    @abstractmethod   
    async def aput(self, messages: List[ChatMessage]) -> None:
        """Push to the memory block (async)."""
        

class WaterfallMemory(BaseChatStoreMemory):
    """A waterfall memory module.
    
    Works by orchestrating around
    - a FIFO queue of messages
    - a list of memory blocks
    - various parameters (pressure size, token limit, etc.)

    When the FIFO queue reaches the token limit, the oldest messages within the pressure size are ejected from the FIFO queue.
    The messages are then processed by each memory block.

    When pulling messages from this memory, the memory blocks are processed in order, and the messages are injected into the system message or the latest user message.
    """

    token_limit: int = Field(default=DEFAULT_TOKEN_LIMIT)
    pressure_token_limit: int = Field(default=DEFAULT_PRESSURE_SIZE, description="The token limit of the pressure size. When the token limit is reached, the oldest messages within the pressure size are ejected from the FIFO queue.")
    memory_blocks: List[BaseMemoryBlock] = Field(default_factory=dict)
    memory_blocks_template: RichPromptTemplate = Field(default=DEFAULT_MEMORY_BLOCKS_TEMPLATE)
    insert_method: InsertMethod = Field(
        default=InsertMethod.SYSTEM, 
        description="Whether to inject memory blocks into the system message or into the latest user message."
    )
    tokenizer_fn: Callable[[str], List] = Field(
        default_factory=get_tokenizer,
        exclude=True,
    )

    @classmethod
    def class_name(cls) -> str:
        return "WaterfallMemory"

    @model_validator(mode="before")
    @classmethod
    def validate_memory(cls, values: dict) -> dict:
        # Validate token limit like ChatMemoryBuffer
        token_limit = values.get("token_limit", -1)
        if token_limit < 1:
            raise ValueError("Token limit must be set and greater than 0.")
        
        tokenizer_fn = values.get("tokenizer_fn", None)
        if tokenizer_fn is None:
            values["tokenizer_fn"] = get_tokenizer()

        return values

    @classmethod
    def from_defaults(
        cls,
        chat_history: Optional[List[ChatMessage]] = None,
        chat_store: Optional[BaseChatStore] = None,
        chat_store_key: str = DEFAULT_CHAT_STORE_KEY,
        token_limit: int = DEFAULT_TOKEN_LIMIT,
        memory_blocks: Optional[List[BaseMemoryBlock]] = None,
        tokenizer_fn: Optional[Callable[[str], List]] = None,
    ) -> "WaterfallMemory":
        """Initialize WaterfallMemory."""

        chat_store = chat_store or SimpleChatStore()
        if chat_history is not None:
            chat_store.set_messages(chat_store_key, chat_history)

        return cls(
            token_limit=token_limit,
            tokenizer_fn=tokenizer_fn or get_tokenizer(),
            chat_store=chat_store,
            chat_store_key=chat_store_key,
            memory_blocks=memory_blocks or [],
        )
    
    async def aget(self, input: Optional[str] = None, **kwargs: Any) -> List[ChatMessage]:
        block_contents = await asyncio.gather(*[
            memory_block.aget(input, **kwargs)
            for memory_block in self.memory_blocks
        ])

        block_contents_str = "\n\n".join(block_contents)
        ...
    
    async def aput(self, message: ChatMessage) -> None:
        ...


# Example memory block implementations
class RetrievalMemoryBlock(BaseMemoryBlock):
    """Simple memory block that performs "retrieval" over chat history."""
    
    name: str = "retrieval"
    description: str = "Retrieves relevant information based on user query"
    stored_messages: List[str] = Field(default_factory=list)
    
    async def aget(self, input: Optional[str] = None, **kwargs: Any) -> str:
        """Simulate retrieving relevant information based on input."""
        if not input or not self.stored_messages:
            return "No relevant information found."
            
        # Simple keyword matching to simulate retrieval
        relevant_messages = [
            msg for msg in self.stored_messages 
            if input.lower() in msg.lower()
        ]
        
        if relevant_messages:
            return f"Retrieved context: {' '.join(relevant_messages)}"
        return "No relevant information found for your query."
    
    async def aput(self, messages: List[ChatMessage]) -> None:
        """Store messages for later retrieval."""
        for message in messages:
            if message.content:
                self.stored_messages.append(str(message.content))


class SummaryMemoryBlock(BaseMemoryBlock):
    """Memory block that maintains a running summary of the conversation."""
    
    name: str = "summary"
    description: str = "Provides a summary of the conversation history"
    summary: str = Field(default="No conversation history yet.")
    
    async def aget(self, input: Optional[str] = None, **kwargs: Any) -> str:
        """Return the current summary."""
        return f"Conversation summary: {self.summary}"
    
    async def aput(self, messages: List[ChatMessage]) -> None:
        """Update summary with new messages (simplified for demonstration)."""
        if not messages:
            return
            
        # Simplified summary update - in reality would use an LLM
        new_content = " ".join([str(m.content) for m in messages if m.content])
        if new_content:
            # Simulate summarization by keeping it short
            self.summary = f"{self.summary} + new messages about: {new_content[:50]}..."


class StaticMemoryBlock(BaseMemoryBlock):
    """Memory block that always returns the same content."""
    
    name: str = "static"
    description: str = "Provides static information regardless of input"
    static_content: str = Field(default="This is static information that's always available.")
    
    async def aget(self, input: Optional[str] = None, **kwargs: Any) -> str:
        """Always return the static content."""
        return self.static_content
    
    async def aput(self, messages: List[ChatMessage]) -> None:
        """Static block doesn't need to store anything."""
        pass


async def main():
    """Example usage of WaterfallMemory with different memory blocks."""
    # Create the memory blocks
    retrieval_block = RetrievalMemoryBlock()
    summary_block = SummaryMemoryBlock()
    static_block = StaticMemoryBlock(
        static_content="I am an AI assistant that helps with information retrieval and summarization."
    )

    memory_block_template = RichPromptTemplate(
"""
<memory>
{% for (block_name, block_content) in memory_blocks %}
<{{ block_name }}>
{block_content}
</{{ block_name }}>
{% endfor %}
</memory>
"""
)
    
    # Initialize WaterfallMemory with the blocks
    memory = WaterfallMemory(
        token_limit=30000,
        pressure_token_limit=5000,
        memory_blocks=[retrieval_block, summary_block, static_block],
        memory_blocks_template=memory_block_template,
    )

if __name__ == "__main__":
    asyncio.run(main())