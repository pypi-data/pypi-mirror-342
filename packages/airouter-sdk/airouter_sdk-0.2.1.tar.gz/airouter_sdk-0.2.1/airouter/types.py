from enum import Enum


class Model(Enum):
    GPT_4O = 'gpt-4o'
    GPT_4O_MINI = 'gpt-4o-mini'
    GPT_41 = 'gpt-4.1'
    GPT_41_MINI = 'gpt-4.1-mini'
    GPT_41_NANO = 'gpt-4.1-nano'
    MISTRAL_LARGE = 'mistral-large'
    MISTRAL_SMALL = 'mistral-small'
    LLAMA_4_SCOUT = 'llama-4-scout'
    LLAMA_4_MAVERICK = 'llama-4-maverick'
    LLAMA_31_8B = 'llama-3.1-8b'
    LLAMA_31_70B = 'llama-3.1-70b'
    LLAMA_31_405B = 'llama-3.1-405b'
    LLAMA_33_70B = 'llama-3.3-70b'
    LLAMA_33_70B_FAST = 'llama-3.3-70b-fast'
    CLAUDE_3_HAIKU = 'claude-3-haiku'
    CLAUDE_3_OPUS = 'claude-3-opus'
    CLAUDE_35_SONNET = 'claude-3-5-sonnet'
    COMMAND_R_PLUS = 'command-r-plus'
    GEMINI_15_FLASH = 'gemini-1.5-flash'
    GEMINI_15_PRO = 'gemini-1.5-pro'
    GEMINI_2_FLASH = 'gemini-2.0-flash'
    GEMINI_2_FLASH_LITE = 'gemini-2.0-flash-lite'
    QWEN25_72B = 'qwen2.5-72B'
    DEEPSEEK_V3 = 'deepseek-v3'
    PHI_4 = 'phi-4'
    UNKNOWN = 'unknown'

    def __init__(self, value):
        super().__init__()
        self._original_value = None

    @classmethod
    def _get_value_map(cls):
        # Create value map only if needed and cache it
        if not hasattr(cls, '_value_map'):
            cls._value_map = {m.value: m for m in cls.__members__.values()}
        return cls._value_map

    @classmethod
    def from_string(cls, value: str) -> 'Model':
        value_map = cls._get_value_map()
        model = value_map.get(value, cls.UNKNOWN)
        if model == cls.UNKNOWN:
            # Create a new instance for unknown models to store the original value
            model = cls.UNKNOWN
            model._original_value = value
        return model

    def to_string(self):
        if self._original_value is not None:
            return self._original_value
        return self.value


class EmbeddingType(Enum):
    TEXT_EMBEDDING_3_SMALL = 'text-embedding-3-small'
    PARAPHRASE_MULTILINGUAL_MPNET_BASE_V2 = 'paraphrase-multilingual-mpnet-base-v2'
