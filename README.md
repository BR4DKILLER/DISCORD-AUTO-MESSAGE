# Discord Auto Message

Discord Auto Message is a program made for [Discord](https://discord.com) and as the name suggests, is used to send messages to discord channels automatically with a configurable delay & message.

## Installation

Install the latest python version from [python.org](https://python.org) and download the files.

## How to obtain your Discord Token

- Login to the Discord Website & Open the Developer/DevTools Console
- Paste the following code into the console:
```
copy((webpackChunkdiscord_app.push([
    [''], {},
    e => {
        m = [];
        for (let c in e.c) m.push(e.c[c])
    }
]), m).find(m => m?.exports?.default?.getToken !== void 0).exports.default.getToken())
```
- If you need any extra help, look at this youtube tutorial: https://www.youtube.com/watch?v=PQFzqRN_jXY
