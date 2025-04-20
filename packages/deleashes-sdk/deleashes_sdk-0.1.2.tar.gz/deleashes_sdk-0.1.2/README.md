# Deleashes SDK for Python

A Python client for the Deleashes feature flag service.

## Installation

```bash
pip install deleashes-sdk
```

Or from source:

```bash
git clone https://github.com/explrms/DeleashesSDK-python.git
cd deleashes-sdk-python
pip install -e .
```

## Quick Start

```python
from deleashes import Deleashes
from deleashes.logging import get_logger
import logging

# Configure logging (optional)
logger = get_logger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)  # Set to DEBUG for verbose logging

# Initialize the client
client = Deleashes(
    api_key="YOUR_PROJECT_API_KEY",
    base_url="https://your-deleashes-url.com",  # Required: URL of your Deleashes instance
    environment="development"  # Or "staging", "production"
)

# Check if a feature flag is enabled
if client.is_enabled("new-feature"):
    # Feature flag is enabled
    print("Feature is enabled!")

# Get the value of a feature flag
feature_value = client.get_value("feature-with-config", default_value="default")
print(f"Feature value: {feature_value}")

# With user context
user_context = {
    "user_id": "user-123",
    "context": {
        "country": "US",
        "plan": "premium"
    }
}

if client.is_enabled("premium-feature", context=user_context):
    print("Premium feature is enabled for this user!")
```

## Configuration

### Environments

Valid environments:
- `development`
- `staging`
- `production`

### Logging

The SDK uses Python's built-in logging system. You can configure the logger to suit your needs:

```python
from deleashes.logging import get_logger
import logging

logger = get_logger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set the log level
logger.setLevel(logging.INFO)  # Or DEBUG, WARNING, ERROR, etc.
```

## Error Handling

The SDK is designed to fail gracefully. If a flag cannot be evaluated (e.g., network issues, invalid flag key):
- `is_enabled()` returns `False`
- `get_value()` returns the provided default value

These failures are logged at the appropriate level (warning or error).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
