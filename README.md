# ailive

## 1. Introduction
This project creates semi-living entities based on recent generative AI models (e.g chatGPT).
It allows creating entities (bots) that can interact with the outside world (e.g chat with people, post on social media, etc).
Such fully automated entities can be used for a variety of purposes, including:
- Fully automated websites (e.g blog, news, etc)
  - 
- Social:
  - Fully automated social media accounts (e.g bot runs on new account)
  - Increase the engagement of social media accounts (proving that the account is active). It can be fully automated or semi-automated in which is the account manager need to approve the actions before they are executed.

The project is composed of 4 main components:
- readers: collection of readers that read data from the outside world (e.g chat, social media, etc). Readers are implemented as plugins. For example:
  - news: reads news from a news website
  - wordpress: reads posts from a wordpress website
- engine: defines the AI model used to generate responses
  - prompt: defines the personality of the entity
  - model: defines the model to be user (e.g GPT-3, GPT-3.5, etc)
- writers: collection of SDK that automate the execution of tasks. Writers are implemented as plugins. For example:
  - chat: sends messages to a chat
  - wordpress: posts on a wordpress website
  - social: posts on social media (e.g twitter, facebook, etc)
- runner: orchestrates the execution of the readers, engine and writers. This is done by running the engine (chatGPT) in a loop, allowing it to interact with the outside world
 

## 2. Installation
### 2.1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2.2. Install ailive
```bash
pip install -e .
```

### 2.3. Environment setup
#### 2.3.1 GPT Setting
Set the MOCK_GPT environment variable to True if you want to use a mock GPT instance for testing purposes. Otherwise, leave it unset or set it to False.
If using real GPT, you will need to set the GPT_EMAIL and GPT_PASSWORD environment variables to the email address and password associated with your GPT account.
```bash
export MOCK_GPT=True
export GPT_EMAIL=your-email@example.com
export GPT_PASSWORD=your-password
```
#### 2.3.2. Wordpress Setting
Set your website details under: ailive/.secrets.yaml
```yaml
plugins:
  wordpress1:
    url: https://your-website.com
    username: your-username
    password: your-password
```


## 3. Usage
### 3.1. Run the server
```bash
python ailive/live_ai_bot.py
```

## 4. Testing
### 4.1. Run the tests
```bash
pytest tests
```
