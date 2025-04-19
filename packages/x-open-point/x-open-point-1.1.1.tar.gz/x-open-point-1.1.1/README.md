# x-open-point
**@readwithai** - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/)

Open an application at a particular location and with a particular size when using X11.

## Motivation
I was experimenting with positioning applications at particular positions in the interests of productivity while writing a blog post. Many applications support a `--geometry` option, however I found that this was far from always the cause and some applications like the popular image viewer [feh](https://feh.finalrewind.org/) did not support different gravities (i.e. you could not use a `-` for positions).

I decided to write a wrapper which externally start an application at a particular location.

## Alternatives and prior work
[wmctrl](http://tripie.sweb.cz/utils/wmctrl/) can move and resize a windows with the `-e` option. I am not aware of any tools that launch an application and then match the window id to the process id like this tool does.

Many applications have a `-geometry` or `--geometry` to provide this functionality but this is determined on an application-by-application basis, may be missing, and the features and inconsistent.

This application was partically inspired by the `kstart` launcher in `KDE` that launches an application while setting a few properties - though not the geometry.

## Installation
You can install x-open-point with [pipx](https://github.com/pypa/pipx):

```
pipx install x-open-point
```

## Usage
The size and location for a window is specified using a syntax similar to [X11 geometries](https://en.wikibooks.org/wiki/Guide_to_X11%2FStarting_Programs).

To open xterm at 100 pixels from the left and 200 pixels from the top you can use:
```
x-open-point +100+200 xterm
```
node the plus sign before `100`. This indicates that this is a distance from the left.

To open a window that is 200 pixels wide and 800 pixels tall you can run:
```
x-open-point 200x800 xterm
```

To open a window at the top-right corner you can use
```
x-open-point -0+0 xterm
```
Similarly you can use `-0-0` for the bottom-right and `+0-0` for the bottom-left.

To place the window at 100 from the left and 200 from the top and have it 300 pixels wide and 400 pixels high you can use:

```
x-open-point 300x400+100+200 xterm
```

In general, if you and expression of the form
```
expression := height "x" width x_gravity X y_gravity Y
height, width, X, Y := integer | percentage
x_gravity, y_gravity := "+" | "-"
```

An `x_gravity` of `+` means that the horizontal is from the left side of the screen to the window, `-` from the right side of the screen. Similarly for `y_gravity`.
`X` is the horizontal distance from a screen edge to the window.
`Y` is the vertical distance.

# Support
If you found this tool useful, you could support it by giving me money ($3 maybe) on [my ko-fi](https://ko-fi.com/c/4e48fdfab2).

You could also my tools [json-wmctrl](https://github.com/talwrii/json-wmctrl) which lists windows with additional information, or [json-xwininfo](https://github.com/talwrii/json-xwininfo). Or read some of my writing on how to take effective notes in [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian).

I've personally found that Obsidian has allowed me for drive-by note taking while coding quite valuable. You could read [something I wrote about this on my blog](https://readwithai.substack.com/p/drive-by-note-taking-in-obsidian).


# About me
I am @readwithai, I make tools related to reading, research and agency sometimes using [Obsidian](https://readwithai.substack.com/p/what-exactly-is-obsidian).

You can follow me on [X](https://x.com/readwithai) on my [blog](https://readwithai.substack.com).

![@readwithai logo](./logo.png)
