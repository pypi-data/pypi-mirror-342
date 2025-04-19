import django_environment_settings

__all__ = [
    "VECTORSTORE_INDEX_NAME",
]


VECTORSTORE_INDEX_NAME = django_environment_settings.get(
    "VECTORSTORE_INDEX_NAME",
    "default",
)
