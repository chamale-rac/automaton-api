# 🚀 automaton-server AKA Proyecto 1

Optimized implementation of Infix to postfix, Regex to ATS, ATS to NFA, NFA to DFA and DFA to DFA minimized.

## 📑 Index

- [💻 Standalone terminal program version.](#standalone-terminal-program-version)
- [🌐 How to run the server?](#how-to-run-the-server)
- [🤔 Why I code this?](#why-i-code-this)
- [🧐 Who I am?](#who-i-am)

## Standalone terminal program version

⚠️ This version is intended to work on the terminal,  perfect for easy checking the accomplishment of project requirements.

Use the next command to run it:

```bash
python app.py
```

## How to run the server?

This server works directly with the web application, go to the referenced repository for more information [automaton (repository)](https://github.com/chamale-rac/automaton).

Use the next command to run the server on your local machine:

```bash
flask --app server run
```

If using docker, you can modify the [compose.yalm](./compose.yaml) for hot reloading (reminder: use only for dev env):

```bash
services:
  web:
    build: .
    ports:
      - "8000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_DEBUG: "true"
```

## Why I code this?

Es el **Proyecto No. 1** de **Teoría de la Computación** **Sección 20** del **Segundo ciclo 2023**. Valía puntos, fuí coaccionado 😭.

## Who I am?

[Samuel A. Chamalé](https://github.com/chamale-rac) - Human

Guatemala, 2023
