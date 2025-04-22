from typing import Optional, Any, Dict, Union

class Message:
    """
    Represents a message in the messaging system.
    
    A Message encapsulates data being sent between components, including
    the payload and optional reply subject for request-reply patterns.
    
    Attributes:
        reply: The reply subject for request-reply messaging patterns
        payload: The message payload data
        headers: Optional headers associated with the message
    """
    
    reply: Optional[str]
    payload: Union[bytes, str]
    headers: Dict[str, str]

    def __init__(self, 
                 payload: Union[bytes, str], 
                 reply: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None):
        """
        Initialize a new Message.
        
        Args:
            payload: The message payload data
            reply: Optional reply subject for request-reply patterns
            headers: Optional headers associated with the message
        """
        self.payload = payload
        self.reply = reply
        self.headers = headers or {}
        
    def get_data_as_string(self) -> str:
        """
        Get the message data as a string.
        
        Returns:
            The message data as a string, decoded if necessary
        """
        if isinstance(self.payload, bytes):
            return self.payload.decode('utf-8')
        return self.payload
        
    def get_data_as_bytes(self) -> bytes:
        """
        Get the message data as bytes.
        
        Returns:
            The message data as bytes, encoded if necessary
        """
        if isinstance(self.payload, str):
            return self.payload.encode('utf-8')
        return self.payload
    
    def add_header(self, key: str, value: str) -> None:
        """
        Add a header to the message.
        
        Args:
            key: The header key
            value: The header value
        """
        self.headers[key] = value
        
    def get_header(self, key: str, default: Any = None) -> Any:
        """
        Get a header value.
        
        Args:
            key: The header key
            default: Default value to return if the key is not found
            
        Returns:
            The header value or the default value
        """
        return self.headers.get(key, default)
    
    def __str__(self) -> str:
        """
        Get a string representation of the message.
        
        Returns:
            A string representation of the message
        """
        payload_preview = str(self.payload)
        if len(payload_preview) > 50:
            payload_preview = payload_preview[:47] + "..."
        
        return f"Message(reply={self.reply}, payload={payload_preview}, headers={self.headers})"
