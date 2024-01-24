# Repository Usage Guide

This guide will walk you through the steps to use the repository and run it locally.
##  set up
```
python -m venv env 
source env/bin/activate
pip install -r requirements.txt
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


