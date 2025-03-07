# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import asyncio
import pytest
import logging
import json
from utils import get_random_dict

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

pytestmark = pytest.mark.asyncio

# TODO: add tests for various application properties
# TODO: is there a way to call send_c2d so it arrives as an object rather than a JSON string?


@pytest.mark.describe("Client C2d")
class TestSendMessage(object):
    @pytest.mark.it("Can receive C2D")
    @pytest.mark.quicktest_suite
    async def test_send_message(self, client, service_helper, event_loop):
        message = json.dumps(get_random_dict())

        received_message = None
        received = asyncio.Event()

        async def handle_on_message_received(message):
            nonlocal received_message, received
            logger.info("received {}".format(message))
            received_message = message
            event_loop.call_soon_threadsafe(received.set)

        client.on_message_received = handle_on_message_received

        await service_helper.send_c2d(message, {})

        await asyncio.wait_for(received.wait(), 60)
        assert received.is_set()

        assert received_message.data.decode("utf-8") == message
