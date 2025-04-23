# Dartmouth Auth

A lightweight package facilitating authentication for Dartmouth services.

## Getting started

1. Install the package:

```
pip install dartmouth-auth
```

2. Obtain a Dartmouth API key from [developer.dartmouth.edu](https://developer.dartmouth.edu/)
3. Store the API key as an environment variable called `DARTMOUTH_API_KEY`:
```
export DARTMOUTH_API_KEY=<your_key_here>
```

## Using the library

Obtain a [JSON Web Token (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token):

```{python}
import dartmouth_auth


my_jwt = dartmouth_auth.get_jwt()
```

You can then use `my_jwt` for any authenticated Dartmouth services that require a JWT.

Inspect `get_jwt()`'s docstring for more detailed usage information.



