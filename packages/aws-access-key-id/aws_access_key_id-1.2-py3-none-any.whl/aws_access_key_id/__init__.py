import json
import base64

__version__ = "1.2"

def get_resource_type(prefix):
    """Return the resource type based on the prefix."""
    prefix_to_type = {
        "ABIA": "AWS STS service bearer token",
        "ACCA": "Context-specific credential",
        "AGPA": "Group",
        "AIDA": "IAM user",
        "AIPA": "Amazon EC2 instance profile",
        "AKIA": "Access key",
        "ANPA": "Managed policy",
        "ANVA": "Version in a managed policy",
        "APKA": "Public key",
        "AROA": "Role",
        "ASCA": "Certificate",
        "ASIA": "Temporary (AWS STS) keys",
    }
    return prefix_to_type.get(prefix, "Unknown resource type")


def forgiving_base32_decode(input_str):
    """Forgiving Base32 decoder that skips invalid characters."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    input_str = input_str.upper()
    buffer = 0
    bits_left = 0
    output = bytearray()

    for char in input_str:
        if char not in alphabet:
            continue
        buffer = (buffer << 5) | alphabet.index(char)
        bits_left += 5
        if bits_left >= 8:
            bits_left -= 8
            output.append((buffer >> bits_left) & 0xFF)
            buffer &= (1 << bits_left) - 1

    return bytes(output)


def aws_account_from_aws_key_id(aws_key_id):
    """Decode AWS Key ID to get the associated AWS account ID."""
    if len(aws_key_id) <= 4:
        return "Invalid Key ID"

    trimmed_key_id = aws_key_id[4:]
    padding = "=" * ((8 - len(trimmed_key_id) % 8) % 8)
    padded_key = trimmed_key_id + padding

    try:
        decoded = base64.b32decode(padded_key, casefold=True)
    except Exception:
        # Fallback to forgiving decode
        try:
            decoded = forgiving_base32_decode(trimmed_key_id)
        except Exception:
            return "Failed to decode with both strict and forgiving methods."

    try:
        y = decoded[:6]
        z = int.from_bytes(y, byteorder="big")
        mask = 0x7FFFFFFFFF80
        e = (z & mask) >> 7
        return str(e).zfill(12)
    except Exception:
        return "Failed to extract AWS account ID after decoding."


def aws_access_key_id(aws_access_key_id):
    """Extract AWS account ID and resource type from an AWS access key ID."""
    try:
        if not aws_access_key_id or len(aws_access_key_id) < 4:
            raise ValueError("Invalid AWS Access Key ID provided.")

        prefix = aws_access_key_id[:4]
        resource_type = get_resource_type(prefix)
        account_id = aws_account_from_aws_key_id(aws_access_key_id)

        if account_id.startswith("Failed"):
            return {
                "statusCode": 422,
                "body": json.dumps({"error": account_id}),
                "headers": {"Content-Type": "application/json"},
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"account_id": account_id, "type": resource_type}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }
    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal error occurred."}),
            "headers": {"Content-Type": "application/json"},
        }


def get_aws_account_id(aws_access_key_id):
    """Return only the AWS account ID from an AWS access key ID."""
    try:
        if not aws_access_key_id or len(aws_access_key_id) < 4:
            raise ValueError("Invalid AWS Access Key ID provided.")

        account_id = aws_account_from_aws_key_id(aws_access_key_id)
        if account_id.startswith("Failed"):
            raise ValueError(account_id)
        return account_id

    except Exception as e:
        raise ValueError(f"Error extracting AWS account ID: {str(e)}")
