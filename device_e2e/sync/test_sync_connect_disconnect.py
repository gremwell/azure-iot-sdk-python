# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import pytest
import logging
import time
import threading
import parametrize

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


@pytest.mark.describe("Client object")
class TestConnectDisconnect(object):
    @pytest.mark.it("Can disconnect and reconnect")
    @pytest.mark.parametrize(*parametrize.connection_retry_disabled_and_enabled)
    @pytest.mark.parametrize(*parametrize.auto_connect_off_and_on)
    @pytest.mark.quicktest_suite
    def test_connect_disconnect(self, brand_new_client):
        client = brand_new_client

        client.connect()
        assert client.connected

        client.disconnect()
        assert not client.connected

        client.connect()
        assert client.connected

    @pytest.mark.it("calls `on_connection_state_change` when setting the handler (connected case)")
    @pytest.mark.quicktest_suite
    def test_on_connection_state_change_gets_called_with_current_state_connected(
        self, brand_new_client
    ):
        """
        This test verifies that the `on_connection_state_change` handler gets called if
        the client is connected when the handler is set.
        """
        client = brand_new_client

        handler_called = threading.Event()

        nonlocal_py27_hack = {"handler_called": handler_called}

        def handle_on_connection_state_change():
            if client.connected:
                nonlocal_py27_hack["handler_called"].set()

        client.connect()
        assert client.connected
        client.on_connection_state_change = handle_on_connection_state_change
        handler_called.wait()

    @pytest.mark.parametrize(
        "previously_connected",
        [
            pytest.param(True, id="previously connected"),
            pytest.param(
                False,
                id="not previously connected",
                marks=pytest.mark.skip(reason="inconssitent behavior"),
            ),
        ],
    )
    @pytest.mark.it(
        "calls `on_connection_state_change` when setting the handler (disconnected case)"
    )
    @pytest.mark.quicktest_suite
    def test_on_connection_state_change_gets_called_with_current_state_disconnected(
        self, brand_new_client, previously_connected
    ):
        """
        This test verifies that the `on_connection_state_change` handler gets called if
        the client is not connected when the handler is set.

        The "not previously connected" case is marked as skip because this inconsistent
        behavior appears to be a bug.
        """
        client = brand_new_client

        handler_called = threading.Event()

        nonlocal_py27_hack = {"handler_called": handler_called}

        def handle_on_connection_state_change():
            if not client.connected:
                nonlocal_py27_hack["handler_called"].set()

        if previously_connected:
            client.connect()
            client.disconnect()
            assert not client.connected

        client.on_connection_state_change = handle_on_connection_state_change
        handler_called.wait()

    @pytest.mark.it(
        "Can do a manual connect in the `on_connection_state_change` call that is notifying the user about a disconnect."
    )
    @pytest.mark.parametrize(*parametrize.connection_retry_disabled_and_enabled)
    @pytest.mark.parametrize(*parametrize.auto_connect_off_and_on)
    # see "This assert fails because of initial and secondary disconnects" below
    @pytest.mark.skip(reason="two stage disconect causes assertion in test code")
    def test_connect_in_the_middle_of_disconnect(
        self,
        brand_new_client,
        service_helper,
        random_message,
    ):
        """
        Explanation: People will call `connect` inside `on_connection_state_change` handlers.
        We have to make sure that we can handle this without getting stuck in a bad state.
        """
        client = brand_new_client
        assert client

        reconnected_event = threading.Event()

        nonlocal_py27_hack = {"reconnected_event": reconnected_event}

        def handle_on_connection_state_change():
            if client.connected:
                logger.info("handle_on_connection_state_change connected.  nothing to do")
            else:
                logger.info("handle_on_connection_state_change disconnected.  reconnecting.")
                client.connect()
                assert client.connected
                nonlocal_py27_hack["reconnected_event"].set()
                logger.info("reconnect event set")

        client.on_connection_state_change = handle_on_connection_state_change

        # connect
        client.connect()
        assert client.connected

        # disconnet.
        reconnected_event.clear()
        logger.info("Calling client.disconnect.")
        client.disconnect()

        # wait for handle_on_connection_state_change to reconnect
        logger.info("waiting for reconnect_event to be set.")
        reconnected_event.wait()

        logger.info("reconect_event.wait() returned.  client.conencted={}".format(client.connected))
        # This assert fails because of initial and secondary disconnects
        assert client.connected

        # sleep a while and make sure that we're still connected.
        time.sleep(3)
        assert client.connected

        # finally, send a message to makes reu we're _really_ connected
        client.send_message(random_message)
        event = service_helper.wait_for_eventhub_arrival(random_message.message_id)
        assert event

    @pytest.mark.it(
        "Can do a manual disconnect in the `on_connection_state_change` call that is notifying the user about a connect."
    )
    @pytest.mark.parametrize(*parametrize.connection_retry_disabled_and_enabled)
    @pytest.mark.parametrize(*parametrize.auto_connect_off_and_on)
    @pytest.mark.parametrize(
        "first_connect",
        [pytest.param(True, id="First connection"), pytest.param(False, id="Second connection")],
    )
    def test_disconnect_in_the_middle_of_connect(
        self, brand_new_client, service_helper, random_message, first_connect
    ):
        """
        Explanation: This is the inverse of `test_connect_in_the_middle_of_disconnect`.  This is
        less likely to be a user scenario, but it lets us test with unusual-but-specific timing
        on the call to `disconnect`.
        """
        client = brand_new_client
        assert client
        disconnect_on_next_connect_event = False

        disconnected_event = threading.Event()

        nonlocal_py27_hack = {"disconnected_event": disconnected_event}

        def handle_on_connection_state_change():
            if client.connected:
                if disconnect_on_next_connect_event:
                    logger.info("connected.  disconnecitng now")
                    client.disconnect()
                    nonlocal_py27_hack["disconnected_event"].set()
                else:
                    logger.info("connected, but nothing to do")
            else:
                logger.info("disconnected.  nothing to do")

        client.on_connection_state_change = handle_on_connection_state_change

        if not first_connect:
            # connect
            client.connect()
            assert client.connected

            # disconnet.
            client.disconnect()

        assert not client.connected

        # now, connect (maybe for the second time), and disconnect inside the on_connected handler
        disconnect_on_next_connect_event = True
        disconnected_event.clear()
        client.connect()

        # and wait for us to disconnect
        disconnected_event.wait()
        assert not client.connected

        # sleep a while and make sure that we're still disconnected.
        time.sleep(3)
        assert not client.connected

        # finally, connect and make sure we can send a message
        disconnect_on_next_connect_event = False
        client.connect()
        assert client.connected

        client.send_message(random_message)
        event = service_helper.wait_for_eventhub_arrival(random_message.message_id)
        assert event


@pytest.mark.dropped_connection
@pytest.mark.describe("Client object with dropped connection")
@pytest.mark.keep_alive(5)
class TestConnectDisconnectDroppedConnection(object):
    @pytest.mark.it("disconnects when network drops all outgoing packets")
    def test_disconnect_on_drop_outgoing(self, client, dropper):
        """
        This test verifies that the client will disconnect (eventually) if the network starts
        dropping packets
        """

        client.connect()
        assert client.connected
        dropper.drop_outgoing()

        while client.connected:
            time.sleep(1)

    @pytest.mark.it("disconnects when network rejects all outgoing packets")
    def test_disconnect_on_reject_outgoing(self, client, dropper):
        """
        This test verifies that the client will disconnect (eventually) if the network starts
        rejecting packets
        """

        client.connect()
        assert client.connected
        dropper.reject_outgoing()

        while client.connected:
            time.sleep(1)
