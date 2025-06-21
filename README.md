# ClaudeBot

This bot is designed to run shiny checks in the game Pokémon. The point of this project was not to create a bot that will shiny hunt for me — it was to create an assistant that will help keep a Twitch chat company while the streamer is away.

ClaudeBot is powered by an easy-to-run local LLM called LLaMA. It makes calls to the LLM while the gameplay loop of the shiny hunt is running.

ClaudeBot is prompted to keep a Pokémon theme and only respond to user messages in the chat, while not repeating old messages. This ensures a small viewer stream is not spammed by just one message and Claude responding to itself.

In order to run the program, you need to have **Pytesseract** installed. This library allows the program to screen capture the chat box and read messages from the display. It also requires **LLaMA** to be installed and running on your machine, as the LLM is accessed locally and not over the internet.

---

### Issues Encountered

Some issues that I ran into while creating ClaudeBot:

- ClaudeBot would often roleplay having viewers.  
- It would read one message and then go off on an imaginary conversation about how interesting the person was — and it would fake their responses as well.  
- It would also try and use emojis in its responses, which would in turn crash the terminal’s ability to type out its response.

I had to create rules and catches to prevent ClaudeBot from talking to itself and from typing things it is not allowed to.

---

### Reflection

I feel this project **has been a success**. This is something that I wanted to accomplish a year ago, but I did not have the courage to learn and understand what it took to create this kind of bot.

Through this course, I have been able to learn how to push myself into uncomfortable areas and create things I did not know were possible.
