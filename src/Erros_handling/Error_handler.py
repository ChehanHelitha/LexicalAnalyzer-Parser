

class ErrorHandler :
    """
     Provides methods to raise exceptions with consistent formatting.
    """
    @staticmethod
    def handle_error(message: str,error_type:type[Exception]=Exception)->None:
        """
        Raises an exception of the specified type with given message.

        Args:
           message (str) : Descriptive error message
           error_type(type[Exception]):Type of exception to raise(default:Exception)
        
        Raises:
           Exception :The specified exception type with formatted message
        """

        raise error_type(message)
    @staticmethod
    def input_error(message: str)-> None:
        """ 
        Raises a ValueError for input-related issues
        """
        raise ValueError(f"Input error: {message}")

    @staticmethod
    def file_error(message :str)-> None:
        """
        Raises on IOError for file-related issues
          """
        raise IOError(f"File error: {message}")
    






