# neo-automaton-basic-toolkit
Optimized implementation of Infix to postfix, Regex to ATS, ATS to NFA, NFA to DFA and DFA to DFA minimized.

Use the next command to run the server:

```bash
flask --app server run
```

Modify the [compose.yalm](./compose.yaml) for hot reloading (use only for dev env):
```
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