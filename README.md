### Robozhab

This is python telethon based client that will go and schedule your daily messages.


#### Installation

1. [Register the developer application for your Telegram Account](https://docs.telethon.dev/en/latest/basic/signing-in.html)
2. Copy the settings file ``cp .env.sample .env``
3. Paste the **api_id** and **api_hash** to .env (or set them as environment variables)
4. If you don't know the **chat_id**, you can create an Invite Link for the chat and use **invite_hash** to get it. But it's better to ask @tgtoadbot with "Мои жабы" command.
6. Run python ``python src/main.py``
7. You will need to log in with your phone number, and password (session data is stored in 'anon.session')
8. Then Robozhab will schedule messages for the next 3 days.

