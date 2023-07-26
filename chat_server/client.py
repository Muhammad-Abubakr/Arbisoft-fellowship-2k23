import math
import asyncio
import os
from pathlib import Path
from logger import makeLogger
from websockets import exceptions
from websockets.client import connect
from utilities import save_file, send_file

# instantiating our custom logger object
logger = makeLogger()


async def client_connection(host: str = "127.0.0.1", port: str = 5000):
    """Opens a persistent client connection with the given "host" at the
    given "port"

    Args:
        host (str, optional): HOST to which to conenct to.
            Defaults to "localhost".
        port (str, optional): PORT to which to connect on
            the host. Defaults to 5000.
    """
    async def receive_message(websocket):
        while True:
            message = await websocket.recv()
            if isinstance(message, bytes):
                await save_file(
                    message, host, port,
                    logger, isClient=True)

            logger.info(f"{host}: {message}\n")
    
    async def async_input(websocket):
        while True:
            file_path = Path(
                    os.path.join(os.getcwd(), "chat_server", "input.txt"))
            if not file_path.is_file():
                open(file=file_path, mode="w+").write(str())
                
            with open(
                file=file_path,
                mode="r+") as input_file:
                for user_input in input_file.readlines():
                    if user_input == "end":  # Checking if the client wants to close the connection
                        logger.debug("Closing connection...")
                        await websocket.close(code=1000)
                        logger.debug("Connection closed!")
                        return
                    elif user_input.startswith("file://"):  # checking if the user wants to send a file
                        path_str = user_input.split(":")[1].strip("/")
                        path = Path(path_str)
                        await send_file(websocket, path=path, logger=logger)
                    else:  # if not, send the user input str to the host
                        logger.info(f"<<<  {user_input}")
                        await websocket.send(user_input.strip())

                input_file.truncate(0)
                input_file.seek(0)
                
            await asyncio.sleep(10)
            
    logger.debug(f"Opening a connection at uri: ws://{host}:{port}")

    try:
        async with connect(
            f"ws://{host}:{port}",
            ping_timeout=float(math.inf),
            open_timeout=float(math.inf),
        ) as websocket:
            logger.debug("connection successful...")

            asyncio.create_task(receive_message(websocket))
            asyncio.create_task(async_input(websocket))

            await asyncio.sleep(1000)

    except (
        exceptions.ConnectionClosedOK,
        exceptions.ConnectionClosedError,
        exceptions.WebSocketException,
    ) as error:
        match error:
            case exceptions.ConnectionClosed:
                logger.debug("Connection closed by Server!. Exit Code: 0")
            case exceptions.ConnectionClosedError:
                logger.debug(
                    f"There was an error while closing the connection {error}"
                )
            case exceptions.WebSocketException:
                logger.debug(f"Websocket Exception: {error}")

        SystemExit(0)
    except OSError as error:
        logger.debug(error)
        SystemExit(0)


asyncio.run(client_connection())
