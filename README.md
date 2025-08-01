<img src="src/fixed_currency_data/data/icon.svg" width="128" height="128">

# Fixer.io Currency Exchange Rate Integration

A Kognitos book integration for accessing real-time currency exchange rates via the Fixer.io API. Supports 170+ world currencies with conversion, rate lookup, and currency information.

## Features

- **Real-time Exchange Rates**: Get current exchange rates for all supported currencies
- **Currency Conversion**: Convert amounts between any supported currencies  
- **Specific Rate Lookup**: Get rates for specific currencies only
- **Currency Information**: List all supported currencies with full names
- **Free Tier Compatible**: Works with free Fixer.io accounts

## Requirements

- Fixer.io API key (free account available at https://fixer.io/signup/free)
- Kognitos platform access

## Available Procedures

### 1. Test Connection
```
say hello
```
Test if the book is loaded and responding.

### 2. Get All Exchange Rates
```
get rates with "your_api_key"
```
Get current exchange rates for all supported currencies (shows first 10).

### 3. Get Specific Currency Rates
```
get specific rates with
    the currencies is "USD,GBP,JPY,CAD"
    the api key is "your_api_key"
```
Get rates for specific currencies only.

### 4. Convert Currency
```
convert currency with
    the amount is "100"
    the source currency is "USD"
    the target currency is "EUR"
    the api key is "your_api_key"
```
Convert an amount from one currency to another using current rates.

### 5. Check Supported Currencies
```
check supported currencies with "your_api_key"
```
Get a list of all supported currencies with their full names.

## Free Tier Limitations

The free Fixer.io plan includes:
- 100 API requests per month
- EUR base currency only
- Current rates only (no historical data)
- HTTPS support via Kognitos

## Prerequisites
Before you begin, ensure you have the following installed on your system:

### Python 3.11
The project is developed with Python 3.11. You can use [pyenv](https://github.com/pyenv/pyenv), [homebrew](https://formulae.brew.sh/formula/python@3.11), [apt](https://linuxcapable.com/how-to-install-python-3-11-on-ubuntu-linux/), or [manual installation](https://www.python.org/downloads/).
 
### Poetry
Poetry is used for dependency management and packaging in this project. You can find the installation guide [here](https://python-poetry.org/docs/).

### Configure Poetry
Once poetry is installed, [configure poetry](https://python-poetry.org/docs/configuration/#virtualenvsin-project) to create the virtual environment inside the project's root directory, by running this:

```Text CLI
poetry config virtualenvs.in-project true
```

## Setting Up the Project

### Clone the Repository
Ensure you have the necessary permissions to access the repository and clone it to your local machine:

```shell
git clone <book repository>
cd <book project>
```

### Install Dependencies
Use Poetry to install all required dependencies in an isolated environment.

```shell
poetry env use 3.11
poetry install
```

### Activate the virtual environment

There are many ways of doing this, depending on your poetry version.

- Running `poetry shell`

or

- Manually activating the venv:
  ```
  # Mac or Linux
  $(poetry env activate)

  # Windows PowerShell
  Invoke-Expression (poetry env activate)
  ```

## Running Tests
This book uses Pytest as its test runner. You can execute it using the following command:

```shell
poetry run tests
```

## Formatting Code
This book uses black and isort as its source formatter. You can execute it using the following command:

```shell
poetry run format
```

## Linting Code
This book uses pylint as its source linter. You can execute it using the following command:

```shell
poetry run lint
```

## Generate usage documentation
This script automatically generates a comprehensive USAGE.md file from the docstrings:

```shell
poetry run doc
```

## Running locally for testing (using docker and ngrok)
You can run the image locally, and use ngrok to make your image routable from the playground:

- You need to install [docker](https://www.docker.com) if you haven't already.
- You need to install and configure [ngrok](https://ngrok.com/) (you need an account, and you have to set up an API KEY. The free tier is enough).

After that, you need to configure ngrok api key as an environment variable:

```shell
export NGROK_AUTHTOKEN=<YOUR_API_KEY>
```

Finally, run the poetry script to host the book locally:

```shell
poetry run host
```

When you run this, you are going to see some logs. One of which contains the ngrok address: `listening on https://<SOME_UUID>.ngrok-free.app`. You need to copy this url and paste it on your kognitos playground using the learn command like this:

```
learn "https://5aad-186-127-136-101.ngrok-free.app"
```

## Building Docker image
In order to deploy the book, a docker image must be build that wraps the book with the BDK runtime:

```shell
docker build -t fixed_currency_data:<VERSION> .
```

## Deploying the Docker image
Once the image is built and tested, you can deploy it anywhere plublicly routable (remember to bind the correct port in the Dockerfile to the port your infrastructure exposes). After that you can learn from that endpoint in the Kognitos playground like this:

```
learn "<HOST_URI_HERE>"
```

## Error Handling

The book includes comprehensive error handling for:
- Invalid API keys
- Rate limiting
- Network issues
- Invalid currency codes
- Malformed requests

All errors are returned as descriptive messages to help troubleshoot issues.