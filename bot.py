import asyncio, re, sys, aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import BufferedInputFile

bot = "8084448228:AAFV6Rhko8rMD4QZ4pATNMtq296H4F8kDus"

if bot == "":
    print("ضع التوكن في المتغير bot بالسطر 7")
    sys.exit(1)

bot_client = Bot(token=bot)
dp = Dispatcher()

def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.reply("أرسل رابط الموقع")

@dp.message()
async def process_url(message: types.Message):
    if not message.text:
        return

    url = message.text
    if not is_valid_url(url):
        await message.reply("الرابط لازم يبلش بـhttp او https")
        return

    wait_msg = await message.reply("باخذلك سكرين اصبر")

    api_url = f"https://image.thum.io/get/width/1280/nocompress/{url}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_file = BufferedInputFile(image_data, filename="screenshot.png")
                    await message.answer_photo(photo=image_file, caption=f"هاد السكرين الي رسلتلي الرابط هاد تبعه : {url}")
                else:
                    await message.reply(f"ما قدرت آخذ لقطة شاشة : {response.status}")
    except Exception:
        await message.reply("صار خطأ")
    finally:
        await bot_client.delete_message(chat_id=wait_msg.chat.id, message_id=wait_msg.message_id)

async def main():
    await dp.start_polling(bot_client)

if __name__ == '__main__':
    asyncio.run(main())