# Agility Teams Manager

## /app/controllers/account - Account controllers

Controls login, logout and signup.

### Routes

#### `login.py`

- `/account/login`

#### `logout.py`

- `/account/logout`

#### `reset.py`

- `/account/reset`
- `/account/reset/<uuid:id_reset>`

#### `signup.py`

- `/account/signup`
- `/account/signup/<uuid:id_confirm>`

### Functions

#### `auth.py`

- `check_auth()`
  
### Docs

See [official documentation](https://agilityteamsmanager.github.io/PROGESCO-Teams/developpement/app.html#account) for more infos.
