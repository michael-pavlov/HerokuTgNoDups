Heroku Telegram Duplicate Messages - v1_0
========
In heroku on free accounts dyno receiving two duplicate messages after wake up.
This code fix it. Also it could be used for prevent multiple duplicate message in short time initiated by user.

Import
-------------

.. code-block:: python

  import herokutelegramnodups

Init
-------------

.. code-block:: python

  duplicate_controll = herokutelegramnodups.HerokuTgNoDups(lifetime_seconds = 2)
  duplicate_controll.run()

Message processing
-------------

.. code-block:: python

  if duplicate_controll.in_cache(message.chat.id, message.text):
    <duplicate way>
  else:
    <normal way>
    

