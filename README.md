# IRC RPG Bot

An attempt to write a persistent RPG bot for IRC. Basic account management had been implemented, as well as an attempt to track active player sessions (ie who is logged on or not).

The basics for combat, including fighting other players and random monsters, was previously implemented as a basic plugin for the Sopel IRC bot. It also supported dynamic generation of combat reward items by appending an adjective to a noun, ie "Magic" + "Greatsword". This bot was an attempt to expand on the basic bot's functionality by adding persistence via SQLite, including a persistent item ledger (items you gained could be won by other players, allowing for a persistent log of all item owners to be reviewed). This would also have allowed the bot to run standalone, rather than being run as a plugin to the (otherwise very good) Sopel bot framework.

My motivation for abandonment was primarily time-related, as I have been working on a [full-fledged RPG](https://www.youtube.com/watch?v=v5ZagYqbqGw&list=PLn3RBikH80qIzmF2txcARiN5qYt21hTfG) using Godot for some time, and didn't want to spread my limited time between both. Also, eventually I migrated to Matrix over IRC, and the relative lack of bot frameworks there have caused my bot projects to lose priority. Given more hours in the day, I'd have been quite happy to continue working on this, and release it to the web for posterity.
