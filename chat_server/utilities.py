import os
from pathlib import Path
from logging import Logger
from websockets.client import WebSocketClientProtocol

async def save_file(
    message: bytes, host: str, 
    port: str, logger: Logger,
    isClient: bool
    ):
    """Converts the data given in bytes to utf-8 string and saves it into
    the appropriate directory, i-e either client's or server's 

    Args:
        message (bytes): data to be stored
        host (str): host sending the data
        port (str): process sending data on host system
        logger (Logger): Logger
        isClient (bool): tells save_file to which directory the data has to
                    be saved to. 
    """
    decoded_data = message.decode("utf-8")
    message = decoded_data.removeprefix("file://")
    [file_name, *other] = message.split(";")
    data = "".join(other)

    storage_folder = str()
    if isClient:
        storage_folder = "client_received"
    else:
        storage_folder = "server_received"

    storage_path = Path(
        os.path.join(
            os.getcwd(), "chat_server", 
            storage_folder, f"{host}:{port}")
    )

    if not storage_path.exists():
        os.makedirs(storage_path)

    with open(storage_path.joinpath(file_name), "w+") as file:
        file.write(data)
        logger.debug(f"{host}:{port} : {file_name} received")

    
async def send_file(
    websocket: WebSocketClientProtocol, path: Path, logger: Logger):
    """Send the file data thorugh the socket as bytes

    Args:
        websocket (WebSocketClientProtocol): helps in sending and
                    receiving information through the websocket
        path (Path): Path descriptor to the file whose data is to 
                    be sent
        logger (Logger): Logger
    """
    if not path.is_file():
        logger.error(f"{path} does not exist")
        return

    with open(path, "r", encoding="utf-8") as file:
        data = "file://" + path.name + ";" + file.read()

        await websocket.send(data.encode(encoding="utf-8"))


