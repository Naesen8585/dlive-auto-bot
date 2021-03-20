# The DLive Auto Bot Project

Have you ever wondered if, as a streamer, you could artificially increase your user participation,
and, if you were a stream watcher, you could automatically increase your participation and lock in your
rewards with DLive? This is your solution!


**This project is still in beta**

## Prerequesites:
To start with, you'll need a DLive account.
You'll need to install Goole Chrome on your machine.
You'll need Python3.7 or greater.
You'll need to make sure pip is functional (or pip3 with python3).

## Installation and Operation:
First, download this repository (Either from Code >> download zip or cloning)
If you downloaded the zip, extract it, in a terminal / command line, navigate to the extracted folder and then

 `pip3 install -r REQUIREMENTS.txt`
and then
`python3 dlivemilker.py`
It will intelligently detect your chrome installation path, meaning all you need to do is follow the prompts in your shell. It will open up a Chrome browser window to the show, which you can watch while the bot works in the background.

### What it does:
This bot takes advantage of DLive's participation system, while attempting to appear as organic as possible, given the show audience and participants. It waits a random interval past the set delay mode, and then posts a sticker, or, reads the most recent and relevant chat posts, and generates a text response based on NLP models (currently modeled off Reddit) to create """realistic""" entries.  This increases your participation score, which increases your potential share of the pot when the chest is opened. Eventually I'd also like to find a way to bypass the captcha hook and run it purely in headless mode, meaning you could let it run on its own, but that's down the line.

### What currently works:
This bot can automatically detect if the show is running or not, and will only start posting stickers and operating in general when the show is live. This prevents you from looking like an obnoxious robo spammer which will inevitably get silenced by the moderation team.
This Bot can also automatically detect if the chest has been opened, and, if so, will automatically collect your rewards. 
### What doesn't quite work yet
Because of the nature of training an NLP system and distributing it to many users with unknown systems, you're probably going to
run in to issues with the text generation, and it's not fully "custom" yet based on the chat dataset. That's a work in progress, though.


## Something Isn't working:
Either file a bug report on this repo or ping me on Discord. Or both! I'd be happy to look in to it, though this tool is a hobby project for me, and progress will be based on free time.

## I don't trust you
That's fine! I included the source code, which you are more than welcome to audit. If you have any questions feel free to ask!
