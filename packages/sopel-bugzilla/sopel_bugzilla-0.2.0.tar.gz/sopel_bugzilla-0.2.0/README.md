# sopel-bugzilla

Domain-based Bugzilla link handler plugin for Sopel IRC bots.


## Installation

```sh
pip install sopel-bugzilla
```


## Configuration

```ini
[bugzilla]
domains = 
    bugzilla.mozilla.org
    bugzilla.kernel.org
    bugs.winehq.org

# list of Bugzilla issue tracker domains from which to get information
```

Run `sopel-plugins configure bugzilla` to enter the domain list interactively.


## Special thanks

All contributors to [the original `bugzilla` plugin for
Sopel](https://github.com/sopel-irc/sopel/commits/master/sopel/modules/bugzilla.py).
