Visual Studio Code notes
========================

Highlighted shortcuts
---------------------
* <kbd>Ctrl</kbd>+<kbd>P</kbd> - recently used files and project files seh.
  * Enter special symbol <kbd>></kbd>, or <kbd>@</kbd>, or <kbd>#</kbd> for command palette, or refereces, or ... correspondigly.
    * <kbd>@</kbd><kbd>:</kbd> to group references by type
  * Keep hitting <kbd>P</kbd> to quckly navigate.
* 🔥 <kbd>F1</kbd> (or <kbd>Ctrl</kbd>+<kbd>P</kbd>,<kbd>></kbd> or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) - magic command palette - do anything
  * 🍏 <kbd>F1</kbd> "interactive playground" - interactive tutorial on several useful features - try it now!
    * multiple cursors <kbd>Alt</kbd>+🖱️Click
    * multiple selected words <kbd>Alt</kbd>+Dbl🖱️Click
    * selected all search results <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd>
    * code snippets, Emmet
  * <kbd>F1</kbd> "reload window" - as restart but faster.</kbd>
* <kbd>Alt</kbd>+<kbd>Z</kbd>: word wrap enable/disable
* 💣 <kbd>F2</kbd> refactor - rename symbol

Highlighted options
---------------------
* Note: there is the user and the workspace options. Create ```.vscode/settings.json``` in a project folder for the latter.
* Auto-Save
* Trim Trailing Whitespace
* Exclusions  ```{ "files.exclude": {"**/*.map": true} }```
* Breadcrumbs
* Ligatures: install font from https://github.com/tonsky/FiraCode
```json
{
    "editor.fontFamily": "Fira Code, Consolas, 'Courier New', monospace",
    "editor.fontLigatures": true
}
```

Highlighted extensions
---------------------
* Python - python language support from Microsoft, must have (#1 in popular)
* Python Docstring Generator - ```"""``` generator

Extensions to check and see
---------------------
* Bracket Pair Colorizer (probably v2) - color brackets by nesting level
* BetterComment
  * 🔴 !
  * 🔵 ?
  * 🟡 TODO:
* AREPL - quick preview of code result
* ⁇ Icon schemes
* ⁇ Python Test Explorer - probably better pytest integrator, TBD
* ⁇ Project Manager - bookmark your projects nicely
* ⁇ GitLens - additional git-related tooltips/markup
* ⁇ Code Runner - probably better generator of run configuration, TBD
* ⁇ python snippets - TBD

Highlighted GUI and workchain features
---------------------
* Autoformatting, autolinting - TBD
* Reset VSCode? delete ```%userprofile%\AppData\Roaming\Code``` and ```%userprofile%\.vscode```
* Move sidebar to the right? (in context menu) Reason: code stays unmoved
* ```py -0``` - list of installed Python versions
* Remote Work
* Enabling miniconda from VS2019:
```bat
cd "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\Extensions\Microsoft\Python\Miniconda\Miniconda3-x64\Scripts"
call activate
conda init
```
Highlighted Python core features
---------------------

* EXPECT_NEAR ==> assert 2.2 == pytest.approx(2.3, 0.001)
* strongly typed
* resource management
