import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables. Create .env file with BOT_TOKEN=your_token")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def split_text(text, max_length=4000):
    parts = []
    while len(text) > max_length:
        split_pos = text.rfind('\n', 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        parts.append(text[:split_pos])
        text = text[split_pos:].lstrip()
    if text:
        parts.append(text)
    return parts

@dp.message(Command("start"))
async def cmd_start(message: Message):
    try:
        if not os.path.exists("dialog.txt"):
            await message.answer("Dialog file not found. Start the AI conversation first!")
            return
        
        with open("dialog.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.strip():
            await message.answer("Dialog file is empty. No conversations yet!")
            return
        
        parts = split_text(content)
        
        await message.answer(f"📜 Sending dialog ({len(content)} characters in {len(parts)} parts)...")
        
        for i, part in enumerate(parts, 1):
            await message.answer(f"Part {i}/{len(parts)}:\n\n{part}")
            await asyncio.sleep(0.5)
        
        await message.answer("✅ All dialog sent!")
        
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

@dp.message(Command("status"))
async def cmd_status(message: Message):
    try:
        if os.path.exists("dialog.txt"):
            size = os.path.getsize("dialog.txt")
            with open("dialog.txt", "r", encoding="utf-8") as f:
                lines = len(f.readlines())
            await message.answer(f"📊 Dialog Status:\n\nFile size: {size} bytes\nLines: {lines}")
        else:
            await message.answer("No dialog file exists yet.")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

@dp.message(Command("clear"))
async def cmd_clear(message: Message):
    try:
        if os.path.exists("dialog.txt"):
            os.remove("dialog.txt")
            await message.answer("🗑️ Dialog file cleared!")
        else:
            await message.answer("No dialog file to clear.")
    except Exception as e:
        await message.answer(f"Error: {str(e)}")

@dp.message()
async def echo(message: Message):
    await message.answer("Commands:\n/start - Get full dialog\n/status - Check dialog status\n/clear - Clear dialog file")

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())