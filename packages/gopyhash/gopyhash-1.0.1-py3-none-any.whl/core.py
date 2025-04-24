import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_hash_from_text(text: str) -> str:
    """
    Generate a hash from the given text using bcrypt.
    
    Args:
        text (str): The text to hash
        
    Returns:
        str: The hashed text
        
    Raises:
        ValueError: If hashing fails
    """
    try:
        text_bytes = text.encode('utf-8')
        hashed = bcrypt.hashpw(text_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to generate hash: {str(e)}")
        raise ValueError(f"Failed to generate hash: {str(e)}")

def compare_hash_and_text(hash_from_db: str, text: str) -> bool:
    """
    Compare a hash with plain text to verify if they match.
    
    Args:
        hash_from_db (str): The stored hash from database
        text (str): The plain text to compare
        
    Returns:
        bool: True if match successful, False otherwise
        
    Raises:
        ValueError: If comparison operation fails
    """
    try:
        hash_bytes = hash_from_db.encode('utf-8')
        text_bytes = text.encode('utf-8')
        return bcrypt.checkpw(text_bytes, hash_bytes)
    except Exception as e:
        logger.error(f"Failed to compare hash: {str(e)}")
        raise ValueError(f"Failed to compare hash: {str(e)}")