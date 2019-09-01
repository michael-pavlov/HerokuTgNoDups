# HerokuTelegramNoDups
In heroku on free accounts dyno receiving two duplicate messages after wake up.
This code fix it. Also it could be used for prevent multiple duplicate message in short time initiated by user.

# Usage
import herokutelegramnodups

in init section:
duplicate_controll = herokutelegramnodups.HerokuTgNoDups()
duplicate_controll.run()

in message processing function:
if duplicate_controll.in_cache(message.chat.id, message.text):
  <duplicate way>
else:
  <normal way>
