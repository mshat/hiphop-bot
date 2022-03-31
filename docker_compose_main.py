from hiphop_bot.db.init.artist_init import init_artist_db_table
from hiphop_bot.dialog_bot.controller.telegram_interface.telegram import run_bot

init_artist_db_table()
run_bot()