# AWS Access Key ID Utility
A Python module for extracting the AWS Account ID and resource type from an AWS Access Key ID. This tool simplifies the process of decoding AWS Access Key IDs to identify account and resource information programmatically.

###  AWS Resource Type Prefixes

This table lists various prefixes and their associated AWS resource types. For more details, refer to the [AWS IAM User Guide - Unique Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids).

| Prefix | Resource Type |
|--------|---------------|
| ABIA   | AWS STS service bearer token |
| ACCA   | Context-specific credential |
| AGPA   | User group |
| AIDA   | IAM user |
| AIPA   | Amazon EC2 instance profile |
| AKIA   | Access key |
| ANPA   | Managed policy |
| ANVA   | Version in a managed policy |
| APKA   | Public key |
| AROA   | Role |
| ASCA   | Certificate |
| ASIA   | Temporary (AWS STS) access key IDs use this prefix, but are unique only in combination with the secret access key and the session token. |

## Features
* Extracts the AWS Account ID from an AWS Access Key ID.
* Identifies the resource type (e.g., IAM user, role, access key).
* Lightweight and easy to integrate into your projects.

## Installation
Install the package via pip:

``` pip install aws_access_key_id ```

## Usage
Here’s an example of how to use the module in your Python code:

### Extracting AWS Account ID and Resource Type
```
from aws_access_key_id import get_aws_account_id, get_resource_type

# Example AWS Access Key ID
aws_access_key_id = "AKIAEXAMPLE123456"

# Extract account ID
account_id = get_aws_account_id(aws_access_key_id)
print(f"AWS Account ID: {account_id}")

# Identify resource type
resource_type = get_resource_type(aws_access_key_id[:4])
print(f"Resource Type: {resource_type}")
```
## Functions
``` get_aws_account_id(aws_access_key_id: str) -> str ```
* Input: A valid AWS Access Key ID (e.g., "AKIAEXAMPLE123456").
* Output: The corresponding 12-digit AWS Account ID.

``` get_resource_type(prefix: str) -> str ```
* Input: The 4-character prefix of the AWS Access Key ID.
* Output: The resource type (e.g., IAM user, Role, Access Key).

## Testing
The package includes a test suite to ensure all functionalities work as expected. To run the tests:

1. Clone the repository:

```
git clone https://github.com/yourusername/aws-access-key-id.git
cd aws-access-key-id
```

2. Install testing dependencies:

```
pip install pytest
```

3. Run the tests:
```
pytest tests/
```

## Contributing
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch:
```
git checkout -b feature-name
```
3. Commit your changes:
```
git commit -m "Add feature or fix description"
```
4. Push the branch to your fork:
```
git push origin feature-name
```
5 .Open a pull request.

## Development Guidelines
* **Code Style:** Follow PEP 8 guidelines.
* **Testing:** Add test cases for new features in the tests/ directory.
* **Documentation:** Update the README.md file for any major changes.

### Project Structure
The repository is organized as follows:

```
aws_access_key_id/
│
├── aws_access_key_id/        # Module folder
│   ├── __init__.py           # Contains your module code
│
├── tests/                    # Test cases folder
│   ├── test_aws_access_key_id.py  # Unit tests for the module
│
├── LICENSE                   # Project license file (e.g., MIT License)
├── README.md                 # Detailed description and usage documentation
├── setup.py                  # Configuration for building and packaging
├── pyproject.toml            # Build system configuration (PEP 517/518)
├── setup.cfg                 # Optional: Additional build configurations
```
### Explanation
```aws_access_key_id/:``` The core module containing all the functionality.

```tests/:``` Contains test cases to ensure the module works as expected.

```LICENSE:``` The license file for the project (e.g., MIT License).

```README.md:``` Documentation about the project, including installation and usage.

```setup.py:``` Configures the module for distribution and packaging.

```pyproject.toml:``` Specifies the build system and dependencies.

```setup.cfg:``` Optional configurations for packaging tools.

## License
This project is licensed under the MIT License.

## Feedback
If you have any suggestions, issues, or feature requests, feel free to open an issue on the GitHub repository.
