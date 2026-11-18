<meta name="author" content="Liran Funaro"/>
<meta name="copyright" content="Copyright (c) 2023-2026, Liran Funaro."/>
<meta name="version" content="0.6.11"/>

<a id="auto-module"></a>

# Auto Module

Example module

### *class* Point(x: [int](https://docs.python.org/3/library/functions.html#int), y: [str](https://docs.python.org/3/library/stdtypes.html#str))

A Point

* **Attributes:**
  **x: int**
  : The x value

  **y: str**
  : The y value

#### x *: [int](https://docs.python.org/3/library/functions.html#int)*

X value

#### y *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Y value

### deprecated_function()

Some old function.

> [!WARNING]
> Deprecated since version 3.1: Use `other()` instead.

### span([start, ]stop[, step])

Return the numbers from start (default 0) up to stop, by step (default 1).

### defaults(a, b=None, \*args, c=1, \*\*kwargs)

Optional parameters in a real signature: rendered with their defaults, with no brackets.

### clock([hour[, minute[, second]]])

Format a time of day as `HH:MM:SS`; missing parts are zero.

### func1(param1: [int](https://docs.python.org/3/library/functions.html#int)) → [int](https://docs.python.org/3/library/functions.html#int)

This is a function with a single parameter. Thanks to github.com/remiconnesson.

* **Parameters:**
  **param1** – This is a single parameter.

### get_option(options, name)

Get an option by name.

* **Parameters:**
  - **options** (*Optional\[Mapping\[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* [*int*](https://docs.python.org/3/library/functions.html#int)*\]\]*) – The options, if any.
  - **name** (*None* *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The option name.

### get_query(name, params=None)

Get a query, with a Google-style docstring.

* **Parameters:**
  - **name** (*Optional\[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*\]*) – Optional name parameter.
  - **params** (*Optional\[Mapping\[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *Any\]\]*) – Optional query params.

### func2(param1: [int](https://docs.python.org/3/library/functions.html#int), param2: [int](https://docs.python.org/3/library/functions.html#int)) → [str](https://docs.python.org/3/library/stdtypes.html#str)

This is a function with two parameters.

* **Parameters:**
  - **param1** – This is the first parameter.
  - **param2** – This is the second parameter.

### func3(param1: [int](https://docs.python.org/3/library/functions.html#int), param2: [int](https://docs.python.org/3/library/functions.html#int))

This is a function with two parameters.

* **Parameters:**
  - **param1** – Alice <sup>[1](#r9b3957318714-1)</sup>.
  - **param2** – Bon <sup>[2](#r9b3957318714-2)</sup>.

### References

* <a id='r9b3957318714-1'>**[1]**</a> Alice is commonly used to describe the first actor.
* <a id='r9b3957318714-2'>**[2]**</a> Bob is commonly used to describe the second actor.

### downside_risk(returns, min_acceptable_return=0.0)

Compute the downside risk of a series of returns.

* **Parameters:**
  **returns** : *ndarray of shape (n_observations,)*
  : The observed returns, at least one.

  **min_acceptable_return** : *float, optional*
  : Returns below this value count as downside.
* **Returns:**
  **risk** : *float*
  : The downside risk.
