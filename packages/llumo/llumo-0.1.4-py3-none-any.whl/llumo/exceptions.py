class LlumoAPIError(Exception):
    """Base class for all Llumo SDK-related errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    @staticmethod
    def InvalidApiKey():
        return LlumoAPIError("The provided API key is invalid or unauthorized")

    @staticmethod
    def InvalidApiResponse():
        return LlumoAPIError("Invalid or UnexpectedError response from the API")

    @staticmethod
    def RequestFailed(detail="The request to the API failed"):
        return LlumoAPIError(f"Request to the API failed: {detail}")

    @staticmethod
    def InvalidJsonResponse():
        return LlumoAPIError("The API response is not in valid JSON format")

    @staticmethod
    def UnexpectedError(detail="An UnexpectedError error occurred"):
        return LlumoAPIError(f"UnexpectedError error: {detail}")

    @staticmethod
    def EvalError(detail="Some error occured while processing"):
        return LlumoAPIError(f"error: {detail}")

