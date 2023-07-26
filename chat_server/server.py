import math
import asyncio
from pathlib import Path
from logger import makeLogger
from websockets import exceptions
from utilities import save_file, send_file
from websockets.server import serve, WebSocketServerProtocol

# logger instantiation
logger = makeLogger()


async def handler(websocket: WebSocketServerProtocol):
    """Handler for the server, helping in sending and receiving messages to
    and from the clients respecively.

    Args:
        websocket (WebSocketServerProtocol): WebSocketServerProtocol passed
            by the websockets.server.serve to help the handler in exchange
            of information with the clients by providing it with a high
            level interface to the sockets.
    """
    try:
        async for message in websocket:
            host, port = websocket.remote_address

            if isinstance(message, bytes):
                await save_file(
                    host=host, port=port, logger=logger,
                    message=message, isClient=False)
                
            else:
                # logging the message from client to console
                logger.info(f"{host}:{port} : {message}\n")

                # taking the response from server
                server_response = str()
                while len(server_response) == 0:
                    server_response = input(
                        f"\r\033[K(to {host}:{port})>>> ").strip()

                # Checking if the client wants to close the connection
                if server_response == "end":
                    logger.debug(f"Closing connection with {host}:{port}")
                    await websocket.close()
                    logger.debug("Connection closed!")

                # checking if the user wants to send a file 
                elif server_response.startswith("file://"):
                    path_str = server_response.split(":")[1].strip("/")
                    path = Path(path_str)

                    await send_file(
                        logger=logger, path=path, websocket=websocket)

                # if not, send the user input str to the host 
                else:
                    await websocket.send(server_response.strip())

    except exceptions.WebSocketException as e:
        logger.fatal(e)


async def main():
    """Main coroutine for the server."""
    try:
        host = "localhost"
        port = 5000

        async with serve(handler, host, port, ping_timeout=float(math.inf)):
            logger.debug(f"Started server at {host}:{port}")
            await asyncio.Future()

    except OSError as e:
        logger.fatal(e)


asyncio.run(main())
