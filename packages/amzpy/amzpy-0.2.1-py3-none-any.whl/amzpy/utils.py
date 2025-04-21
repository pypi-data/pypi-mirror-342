from typing import Tuple, Optional
import re

def parse_amazon_url(url: str) -> Optional[Tuple[str, str]]:
    """
    Parse Amazon product URL to extract base URL and product ID
    
    Args:
        url (str): Full Amazon product URL
        
    Returns:
        Tuple[str, str]: (base_url, product_id) if valid
        None: If URL is invalid
        
    Examples:
        >>> parse_amazon_url("https://www.amazon.com/dp/B0D4J2QDVY")
        ("https://www.amazon.com/", "B0D4J2QDVY")
        >>> parse_amazon_url("https://www.amazon.in/product-name/dp/B0D4J2QDVY/ref=...")
        ("https://www.amazon.in/", "B0D4J2QDVY")
    """
    # Clean up the URL
    url = url.strip()
    
    # Match Amazon domain and product ID
    pattern = r'https?://(?:www\.)?amazon\.([a-z.]+)(?:/[^/]+)*?/(?:dp|gp/product)/([A-Z0-9]{10})'
    match = re.search(pattern, url)
    
    if not match:
        return None
        
    # Extract domain and construct base URL
    domain = match.group(1)
    base_url = f"https://www.amazon.{domain}/"
    
    # Extract product ID
    product_id = match.group(2)
    
    return base_url, product_id 

def format_canonical_url(url: str, asin: str, country_code: str = None) -> str:
    """
    Format a canonical Amazon product URL in the form amazon.{country}/dp/{asin}
    
    Args:
        url (str): Original Amazon URL
        asin (str): ASIN of the product
        country_code (str, optional): Country code (e.g., "com", "in")
        
    Returns:
        str: Canonical URL
    """
    if not asin:
        return url  # Return original if no ASIN available
        
    # If country_code is not provided, try to extract it from the original URL
    if not country_code:
        try:
            parsed_url = urlparse(url)
            domain_parts = parsed_url.netloc.split('.')
            # Extract country code from domain (e.g., www.amazon.com -> com)
            if len(domain_parts) >= 3 and 'amazon' in domain_parts:
                amazon_index = domain_parts.index('amazon')
                if amazon_index + 1 < len(domain_parts):
                    country_code = domain_parts[amazon_index + 1]
        except Exception:
            country_code = "com"  # Default to .com if extraction fails
    
    # Default to .com if still no country code
    if not country_code:
        country_code = "com"
        
    # Create canonical URL
    return f"https://www.amazon.{country_code}/dp/{asin}"

# Function to extract brand name from text
def extract_brand_name(text):
    match = re.search(r'visit the (.+?) store', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None