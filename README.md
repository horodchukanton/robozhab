*master* - 
[![Python package](https://github.com/horodchukanton/robozhab/actions/workflows/default.yaml/badge.svg?branch=master)](https://github.com/horodchukanton/robozhab/actions/workflows/default.yaml)

## Robozhab

This is a python telethon based client that will go and schedule your daily messages.

### Usage

#### Installation

1. [Register the developer application for your Telegram Account](https://docs.telethon.dev/en/latest/basic/signing-in.html)
2. Copy the settings file ``cp .env.sample .env``
3. Paste the **api_id** and **api_hash** to .env (or set them as environment variables)
4. Ask @tgtoadbot "Мои жабы" to get the **chat_id**
5. Run python ``python src/main.py``
6. You will need to log in with your phone number, and password
7. Then Robozhab will schedule messages for the next 3 (or configured) days.

#### Docker
 
    docker run -it --env-file zhaba.env -v $(pwd)/anon.session:/app/anon.session -v $(pwd)/.offset:/app/.offset horodchukanton/robozhab
