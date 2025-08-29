from typing import Optional
import re


class UserValidators:
    @staticmethod
    def validate_email(email: Optional[str]) -> Optional[str]:
        if email is None:
            return email
        return email.lower().strip()
    
    @staticmethod
    def validate_name(name: Optional[str]) -> Optional[str]:
        if name is None:
            return name
            
        name = name.strip()
        if not name:
            raise ValueError('Name cannot be empty')
        return name.title()
    
    @staticmethod
    def validate_username(username: Optional[str]) -> Optional[str]:
        if username is None:
            return username
            
        username = username.strip().lower()
        if not username:
            return None
            
        if len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return username
    
    @staticmethod
    def validate_password(password: Optional[str], require_special_char: bool = True) -> Optional[str]:
        if password is None:
            return password
            
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Check for at least one lowercase letter
        if not any(c.islower() for c in password):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for at least one digit
        if not any(c.isdigit() for c in password):
            raise ValueError('Password must contain at least one digit')
        
        # Check for special character (only if required)
        if require_special_char:
            special_chars = '!@#$%^&*()-_=+[]{}|;:,.<>?/'
            if not any(c in special_chars for c in password):
                raise ValueError('Password must contain at least one special character')
        
        return password
    
    @staticmethod
    def validate_phone_number(phone: Optional[str]) -> Optional[str]:
        if phone is None:
            return phone
            
        # Remove all spaces and hyphens for validation
        clean_phone = re.sub(r'[\s\-]', '', phone)
        
        # Check if it matches the pattern
        if not re.match(r"^\+?[1-9]\d{0,15}$", clean_phone):
            raise ValueError('Invalid phone number format')
            
        return phone
    
    @staticmethod
    def validate_url(url: Optional[str], max_length: int = 500) -> Optional[str]:
        if url is None:
            return url
            
        url = url.strip()
        if not url:
            return None
            
        if len(url) > max_length:
            raise ValueError(f'URL must be less than {max_length} characters')
            
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
        if not url_pattern.match(url):
            raise ValueError('Invalid URL format')
            
        return url