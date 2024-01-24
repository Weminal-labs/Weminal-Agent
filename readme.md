# Repository Usage Guide

This guide will walk you through the steps to use the repository and run it locally.
## 
```
python3 -m venv env 

```

## Prerequisites

Before you begin, make sure you have the following:
- A valid `secret.json` file containing the required API keys.

## Configuration

1. Create a `secret.json` file in the root directory of the repository.

2. Open the `secret.json` file and add the following keys:

    ```json
    {
    "OPENAI_API_KEY": "",
    "SERPAPI_API_KEY": ""
    }   
    ```

    Replace `YOUR_OPEN_API_KEY` and `YOUR_SERAPI_KEY` with your actual API keys.

## Running the Application



Here is the generated msg JSON to swap 5 ORAI to ORAI234124124125:\n\n```json\n{\n  \"swap\": {\n    \"offer_asset\": {\n      \"info\": {\n        \"native_token\": {\n          \"denom\": \"orai\"\n        }\n      },\n      \"amount\": \"5000000\"\n    }\n  }\n}\n\nPlease note that this is just the msg JSON and you will need to use it with the appropriate transaction function to actually perform the swap.