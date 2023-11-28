from config import TOKEN, state_dispenser
from vkbottle.bot import Bot
from handlers import labelers
from utilites import db_init

bot = Bot(token=TOKEN, state_dispenser=state_dispenser)

for labeler in labelers:
    bot.labeler.load(labeler)

if __name__ == '__main__':
    db_init.initialize()
    bot.run_forever()
