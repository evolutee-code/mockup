"""
simple_2fa_generator.py - Generate OTP codes from a 2FA secret using pyotp

This script focuses on properly handling 2FA secrets in various formats
and generating valid TOTP codes using the pyotp library.
"""

import pyotp
import time
import re
import sys
import base64


def format_2fa_secret(secret):
    """
    Format a 2FA secret key for use with pyotp.
    Handles various formats including spaces, dashes, and different casings.

    Args:
        secret: The 2FA secret key

    Returns:
        Properly formatted secret for pyotp
    """
    # Remove all whitespace, dashes, and special characters
    clean_secret = re.sub(r'[\s\-_=]', '', secret)

    # Convert to uppercase (base32 is case-insensitive but traditionally uppercase)
    clean_secret = clean_secret.upper()

    # Check if it's a valid base32 string
    if not re.match(r'^[A-Z2-7]+$', clean_secret):
        raise ValueError("Invalid 2FA secret: contains characters not in base32 alphabet (A-Z, 2-7)")

    # Add padding if needed
    padding_needed = len(clean_secret) % 8
    if padding_needed > 0:
        clean_secret += '=' * (8 - padding_needed)

    return clean_secret


def validate_secret(secret):
    """
    Validate that a secret can be used with pyotp

    Args:
        secret: The formatted secret key

    Returns:
        True if valid, False otherwise
    """
    try:
        # Try to decode the secret
        base64.b32decode(secret)
        return True
    except Exception:
        return False


def generate_totp(secret):
    """
    Generate a TOTP code from a 2FA secret

    Args:
        secret: The 2FA secret key

    Returns:
        Current TOTP code and time remaining
    """
    try:
        # Format the secret
        formatted_secret = format_2fa_secret(secret)

        # Validate secret
        if not validate_secret(formatted_secret):
            raise ValueError("Invalid 2FA secret: could not decode as base32")

        # Create TOTP object
        totp = pyotp.TOTP(formatted_secret)

        # Generate current code
        code = totp.now()

        # Calculate time remaining
        remaining = 30 - (int(time.time()) % 30)
        formatted_code = f"{code[:3]} {code[3:]}" if len(code) == 6 else code

        return {
            'code': formatted_code,
            'remaining': remaining,
            'formatted_secret': formatted_secret
        }
    except Exception as e:
        print(f"Error: {e}")
        return None




# def display_totp_info(totp_info):
    # """
    # Display formatted TOTP information
    #
    # Args:
    #     totp_info: Dictionary with TOTP information
    # """
    # if not totp_info:
    #     return
    #
    # code = totp_info['code']
    # remaining = totp_info['remaining']
    #
    # # Format code for display (add space in middle like Google Authenticator)
    # formatted_code = f"{code[:3]} {code[3:]}" if len(code) == 6 else code
    #
    # # Create progress bar
    # bar_length = 30
    # filled_length = int(bar_length * remaining / 30)
    # bar = '█' * filled_length + '░' * (bar_length - filled_length)
    #
    # print("\n== 2FA ONE-TIME PASSWORD ==")
    # print(f"Code: {formatted_code}")
    # print(f"Valid for: {remaining} seconds")
    # print(f"[{bar}]")
    #
    # # If time is short, add a warning
    # if remaining <= 5:
    #     print("⚠️  CODE EXPIRING SOON ⚠️")
#
#
    # secret = "j67g 7kvt ai7z fcex 4c3h ku5e hdpk imez"

# def main():
#     # Get the secret from command line argument or use default example
#     if len(sys.argv) > 1:
#         secret = sys.argv[1]
#     else:
#         # Default to using the string "2FA Secret" as the seed
#         secret = "j67g 7kvt ai7z fcex 4c3h ku5e hdpk imez"
#         print("No secret provided, using the string '2FA Secret' as the seed.")
#
#     # Generate and display TOTP

        # totp_info = generate_totp(secret)
#
#     if totp_info:
#         display_totp_info(totp_info)
#
#         # Show the formatted secret
#         print(f"\nFormatted secret: {totp_info['formatted_secret']}")
#
#         # Generate URI for QR code
#         totp = pyotp.TOTP(totp_info['formatted_secret'])
#         uri = totp.provisioning_uri(name="Example", issuer_name="Test")
#         print(f"Auth URI: {uri}")
#     else:
#         print("\nFailed to generate TOTP code. Please check your secret key.")
#         print("The secret key should contain only characters A-Z and 2-7 (after removing spaces/dashes).")
#
#
# if __name__ == "__main__":
#     main()