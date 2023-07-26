from abc import ABC
import asyncio
import sys

class LoadingAnimation(ABC):
    """Provides a loading animation for console application

    ### Parent:
        ABC (class): Abstract Base Class to prevent instantion of a class, and
            forcing any method implementation to the child class by using
            @abstractmethod decorator.
    
    ### Methods:
        @staticmethod
        cleanup() -> None
            Performs the cleanup after the loading indicator has stopped
        
        @staticmethod
        async def animate(
            post_message: str= str(""), pre_message: str='waiting...'
        ) -> None
            Provides a loading animation
        
    """
    @staticmethod
    def cleanup() -> None:
        """Performs the cleanup after the loading indicator has stopped
        
        Cleaning up the characters on the console line being used by 
        animate while also cleaning up any characters in the buffer.
        """
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()
    
    @staticmethod
    async def animate(
        post_message: str= str(""),
        pre_message: str='waiting...'
    ) -> None:
        """provides a loading animation

        Args:
            post_message (str): message to show after the laoding indicator.
                        Defaults to None.
            pre_message (str, optional): message to show before the loading
                        indicator. Defaults to 'waiting...'.
        """
        while True:
            for ele in ['-', '\\', '|', '/']:
                sys.stdout.write(f"\r{pre_message}{ele}{post_message}")
                sys.stdout.flush()
                await asyncio.sleep(0.1)
