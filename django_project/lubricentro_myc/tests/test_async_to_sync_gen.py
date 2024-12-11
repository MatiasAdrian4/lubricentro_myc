from asyncio import sleep

import pytest

from lubricentro_myc.chatbot.utils import async_to_sync_gen


class TestAsyncToSyncGen:
    async def async_generator_example(self):
        for word in ["hello", "how", "are", "you"]:
            await sleep(0.1)  # simulates asynchronous operation
            yield word

    def test_consumption(self):
        sync_gen = async_to_sync_gen(self.async_generator_example)
        result = list(sync_gen)  # consume the generator
        assert result == ["hello", "how", "are", "you"]

    def test_partial_consumption(self):
        sync_gen = async_to_sync_gen(self.async_generator_example)
        first_item = next(sync_gen)  # consume only the first item
        assert first_item == "hello"
        remaining_items = list(sync_gen)  # consume the rest
        assert remaining_items == ["how", "are", "you"]

    def test_reuse_generator(self):
        sync_gen = async_to_sync_gen(self.async_generator_example)
        list(sync_gen)  # consume the generator
        with pytest.raises(StopIteration):
            next(sync_gen)
