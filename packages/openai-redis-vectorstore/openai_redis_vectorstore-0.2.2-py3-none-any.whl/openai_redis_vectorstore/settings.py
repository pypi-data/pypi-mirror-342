import python_environment_settings

__all__ = [
    "OPENAI_REDIS_VECTORSTORE_REDIS_STACK_URL",
]

OPENAI_REDIS_VECTORSTORE_REDIS_STACK_URL = python_environment_settings.get(
    "OPENAI_REDIS_VECTORSTORE_REDIS_STACK_URL",
    "redis://localhost:6379/0",
    aliases=[
        "REDIS_STACK_URL",
        "REDIS_URL",
        "REDIS",
    ],
)
