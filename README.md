# How to Start This Project

Follow these steps to set up the project:

## 1. Create Accounts

Create free accounts on the following platforms:

- **Groq:** <https://console.groq.com>
- **Qdrant Cloud:** <https://cloud.qdrant.com>

## 2. Create a Conda Environment

Create and activate a Conda environment to keep the project's dependencies isolated.

```bash
conda create -n <env_name> python=3.11
conda activate <env_name>
```

## 3. Install Required Packages

Install the required Python packages:

```bash
pip install groq python-dotenv
```

`groq` is the official Groq Python SDK, and `python-dotenv` is used to load environment variables from a `.env` file.
