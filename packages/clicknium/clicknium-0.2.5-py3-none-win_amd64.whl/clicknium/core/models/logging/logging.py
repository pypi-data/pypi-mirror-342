from clicknium.core.service.invokerservice import _InvokerService


class Logging:
    def info(self, msg: str = '') -> None:
        """
            Log type info messages
        """
        print(msg)
        _InvokerService.info(msg)
        
    def debug(self, msg: str = '') -> None:
        """
            Log type debug messages
        """
        print(msg)
        _InvokerService.debug(msg)
    
    def warn(self, msg: str = '') -> None:
        """
            Log type warn messages
        """
        print(msg)
        _InvokerService.warn(msg)
        
    def error(self, msg: str = '') -> None:
        """
            Log type error messages
        """
        print(msg)
        _InvokerService.error(msg)
