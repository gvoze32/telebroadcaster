import random
import time
import json
import configparser
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    config = configparser.ConfigParser()

    if config.read("config.data"):
        api_id = config['telegram']['api_id']
        api_hash = config['telegram']['api_hash']
        group_ids = config['telegram']['group_ids'].split(',')
        loop_time = int(config['telegram']['loop_time'])
        message_file = config['telegram']['message_file']
    else:
        api_id = input("API: ")
        api_hash = input("API Hash: ")
        group_ids = input("Group Username: ").split(',')
        loop_time = int(input("Loop (second): "))
        message_file = input("JSON file (e.g., messages.json): ")

        config['telegram'] = {
            'api_id': api_id,
            'api_hash': api_hash,
            'group_ids': ','.join(group_ids),
            'loop_time': str(loop_time),
            'message_file': message_file
        }

        with open('config.data', 'w') as configfile:
            config.write(configfile)

    logger.info(f"Config loaded: api_id={api_id}, group_ids={group_ids}, loop_time={loop_time}, message_file={message_file}")
    return api_id, api_hash, group_ids, loop_time, message_file

def load_messages(file_path):
    with open(file_path, 'r') as file:
        messages = json.load(file)
    logger.info(f"Loaded {len(messages)} messages from {file_path}")
    return messages

async def send_message_to_groups(api_id, api_hash, group_ids, loop_time, messages):
    client = TelegramClient('anon', api_id, api_hash)
    await client.start()

    try:
        entities = []
        for group_id in group_ids:
            try:
                # Menggunakan username grup
                entity = await client.get_entity(group_id)
                entities.append(entity)
                logger.info(f"Successfully got entity for group: {group_id}")
            except Exception as e:
                logger.error(f"Error getting entity for group {group_id}: {e}")

        while True:
            for entity in entities:
                message = random.choice(messages)

                try:
                    await client.send_message(entity, message)
                    logger.info(f"Message sent to group {entity.id}: {message[:30]}...")
                except FloodWaitError as e:
                    logger.warning(f"Rate limit exceeded for group {entity.id}. Sleeping for {e.seconds} seconds.")
                    time.sleep(e.seconds)
                except Exception as e:
                    logger.error(f"Error sending message to group {entity.id}: {e}")
            
            wait_time = loop_time + random.randint(-60, 60)
            logger.info(f"Waiting for {wait_time} seconds before sending the next message to all groups.")
            time.sleep(wait_time)

    finally:
        await client.disconnect()

if __name__ == "__main__":
    api_id, api_hash, group_ids, loop_time, message_file = load_config()
    messages = load_messages(message_file)

    import asyncio
    asyncio.run(send_message_to_groups(api_id, api_hash, group_ids, loop_time, messages))
