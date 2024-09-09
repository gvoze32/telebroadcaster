# Telebroadcaster

A Telegram bot that sends messages to specified groups at regular intervals.

## Description

This bot reads messages from a JSON file and sends them to specified Telegram groups at random intervals. It handles rate limiting and logs its activities.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gvoze32/telebroadcaster.git
   cd telebroadcaster
   ```

2. Install the required dependencies:
   ```bash
   pip install telethon
   ```

## Configuration

1. Edit the `config.data` file with the following content:

   ```ini
   [telegram]
   api_id = your_api_id
   api_hash = your_api_hash
   group_ids = group1,group2,group3
   loop_time = loop_time_in_seconds
   message_file = messages.json_path
   ```

2. Alternatively, the bot will prompt you to enter these details when you run it for the first time.

## Usage

1. Prepare a JSON file with the messages you want to send. Example `messages.json`:

   ```json
   ["Hello, group!", "This is a test message.", "How are you doing today?"]
   ```

2. Run the bot:
   ```bash
   python bot.py
   ```

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is licensed under the MIT License.
