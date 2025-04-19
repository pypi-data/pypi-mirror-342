# textual-pyfiglet-fonts

This contains the full extended fonts collection for Textual-PyFiglet.

The original PyFiglet contains all fonts in the package. For Textual-PyFiglet they were split into their own package, since the fonts data is much larger than the size of the program data. Textual aims to be efficient due to being a TUI framework. (There's still 15 or so default fonts that come with the base package.)

This is intended to be installed like this:  

```sh
pip install textual-pyfiglet[fonts]
```

But you could also just download the package directly:

```sh
pip install textual-pyfiglet-fonts
```

There is no code in this package which can be executed.
