# Zenbroker Client Example

This project demonstrates how to use the Zenbroker client library to publish messages to channels.

## Installation

```bash
pip install zenbroker
```

## Configuration

You need to configure your Zenbroker client with your application ID:

```python
from zenbroker import ZenbrokerClient

client = ZenbrokerClient(
    application_id="YOUR_APPLICATION_ID",
    base_url="https://broker.oraczen.xyz"
)
```

## Usage

### Publishing a single message

```python
resp = client.publish(
    channel="CHANNEL-ID",
    data={
        "key": "value",
        "message": "hello"
    }
)
```

## Notes

- Replace `YOUR_APPLICATION_ID` with your actual application ID
- Replace `CHANNEL-ID` with your target channel ID when publishing messages
