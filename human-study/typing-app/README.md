# Typing Study Collector

A minimal client-side collector for the controlled human typing study.

## Run locally

From the repository root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/human-study/typing-app/
```

The app:
- records only keystrokes inside the research prompt box;
- tracks typing duration, edit count and backspace/delete count;
- stores data only in browser memory during the session;
- exports a de-identified CSV locally.

It does **not** transmit study responses to a server.

Before real participant recruitment, replace the minimal consent checkbox with institution-approved participant information/consent language.
