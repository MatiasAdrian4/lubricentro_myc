# Django's StreamingHttpResponse only supports synchronous generators.
# The `async_to_sync_gen` adapter converts an async generator function into a synchronous generator,
# enabling Django to stream responses incrementally while preserving the non-blocking nature of the underlying logic.
# If you want to avoid this adapter, consider using ASGI-native frameworks like FastAPI or Starlette,
# which natively support asynchronous streaming. For Django, this approach is a pragmatic workaround.


def async_to_sync_gen(async_gen_func):
    """
    Converts an asynchronous generator function into a synchronous generator.
    Args:
        async_gen_func: A callable that returns an asynchronous generator.
    Yields:
        Synchronously yields items produced by the asynchronous generator.
    """
    # TODO: search the best way for handling this
    pass
