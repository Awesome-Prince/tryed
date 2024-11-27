import asyncio

# Retry logic for async operations
async def tryer(func, *args, **kwargs):
    retry_count = 3  # Number of retries
    for attempt in range(retry_count):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt < retry_count - 1:
                await asyncio.sleep(2)  # Wait before retrying
                continue
            else:
                raise e  # If all retries fail, raise the error
