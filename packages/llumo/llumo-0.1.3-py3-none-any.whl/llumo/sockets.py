import socketio
import threading
import time


class LlumoSocketClient:
    def __init__(self, socket_url):
        self.socket_url = socket_url
        self._received_data = []
        self._last_update_time = None
        self._listening_done = threading.Event()
        self._connection_established = threading.Event()
        self._lock = threading.Lock()
        self._connected = False
        self.server_socket_id = None  # Store the server-assigned socket ID

        # Initialize client
        self.sio = socketio.Client(
            # logger=True,
            # engineio_logger=True,
            reconnection=True,
            reconnection_attempts=5,
            reconnection_delay=1,
        )

        @self.sio.on("connect")
        def on_connect():
            print("Socket connection established")
            self._connected = True
            # Don't set connection_established yet - wait for server confirmation

        # Listen for the connection-established event from the server
        @self.sio.on("connection-established")
        def on_connection_established(data):
            print(
                f"Server acknowledged connection with 'connection-established' event: {data}"
            )
            if isinstance(data, dict) and "socketId" in data:
                self.server_socket_id = data["socketId"]
                print(f"Received server socket ID: {self.server_socket_id}")
            self._connection_established.set()

        @self.sio.on("result-update")
        def on_result_update(data):
            with self._lock:
                print(f"Received result-update event: {data}")
                self._received_data.append(data)
                self._last_update_time = time.time()

        @self.sio.on("disconnect")
        def on_disconnect():
            print("Socket disconnected")
            self._connected = False

        @self.sio.on("connect_error")
        def on_connect_error(error):
            print(f"Socket connection error: {error}")

        @self.sio.on("error")
        def on_error(error):
            print(f"Socket error event: {error}")

    def connect(self, timeout=20):
        self._received_data = []
        self._connection_established.clear()
        self._listening_done.clear()
        self.server_socket_id = None

        try:
            print("Attempting direct WebSocket connection...")
            # Connect with websocket transport
            self.sio.connect(self.socket_url, transports=["websocket"], wait=True)

            print(f"Engine.IO connection established with SID: {self.sio.sid}")
            print(
                "Waiting for server to acknowledge connection with connection-established event..."
            )

            # Wait for the connection-established event
            if not self._connection_established.wait(timeout):
                raise RuntimeError("Timed out waiting for connection-established event")

            self._last_update_time = time.time()
            print(
                f"Connection fully established. Server socket ID: {self.server_socket_id}"
            )

            # Return the server-assigned socket ID if available, otherwise fall back to the client's SID
            return self.server_socket_id or self.sio.sid
        except Exception as e:
            self._connected = False
            raise RuntimeError(f"WebSocket connection failed: {e}")

    def listen_for_results(self, min_wait=5, max_wait=300, inactivity_timeout=30):
        """
        Listen for results with improved timeout handling:
        - min_wait: Minimum time to wait even if no data is received
        - max_wait: Maximum total time to wait for results
        - inactivity_timeout: Time to wait after last data received
        """
        if not self._connected:
            raise RuntimeError("WebSocket is not connected. Call connect() first.")

        start_time = time.time()
        self._last_update_time = time.time()

        def timeout_watcher():
            while not self._listening_done.is_set():
                current_time = time.time()
                time_since_last_update = current_time - self._last_update_time
                total_elapsed = current_time - start_time

                # Always wait for minimum time
                if total_elapsed < min_wait:
                    time.sleep(0.5)
                    continue

                # Stop if maximum time exceeded
                if total_elapsed > max_wait:
                    print(
                        f"⚠️ Maximum wait time of {max_wait}s reached, stopping listener."
                    )
                    self._listening_done.set()
                    break

                # Stop if no activity for inactivity_timeout
                if time_since_last_update > inactivity_timeout:
                    print(
                        f"⚠️ No data received for {inactivity_timeout}s, stopping listener."
                    )
                    self._listening_done.set()
                    break

                # Check every second
                time.sleep(1)

        timeout_thread = threading.Thread(target=timeout_watcher, daemon=True)
        timeout_thread.start()
        print("Started listening for WebSocket events...")
        self._listening_done.wait()
        print(f"Finished listening. Received {len(self._received_data)} data updates.")

    def get_received_data(self):
        with self._lock:
            return self._received_data.copy()

    def disconnect(self):
        try:
            if self._connected:
                self.sio.disconnect()
                self._connected = False
                print("WebSocket client disconnected")
        except Exception as e:
            print(f"Error during WebSocket disconnect: {e}")
