import builtins

# JavaScript-style
class console:
    @staticmethod
    def log(*args, **kwargs): print(*args, **kwargs)

# Java-style
class System:
    class out:
        @staticmethod
        def println(*args, **kwargs): print(*args, **kwargs)

# C#-style
class Console:
    @staticmethod
    def WriteLine(*args, **kwargs): print(*args, **kwargs)

# Other styles
def echo(*args, **kwargs): print(*args, **kwargs)
def sh_echo(*args, **kwargs): print(*args, **kwargs)
def println(*args, **kwargs): print(*args, **kwargs)
def puts(*args, **kwargs): print(*args, **kwargs)
def println_rust(*args, **kwargs): print(*args, **kwargs)
def fmt_Println(*args, **kwargs): print(*args, **kwargs)

# Expose globally
builtins.console = console
builtins.System = System
builtins.Console = Console
builtins.echo = echo
builtins.sh_echo = sh_echo
builtins.println = println
builtins.puts = puts
builtins.println_rust = println_rust
builtins.fmt = type("fmt", (), {"Println": staticmethod(fmt_Println)})
