Visual Studio Code notes
========================
* <kbd>Ctrl</kbd>+<kbd>P</kbd> - recently used files and project files seh.
  * Enter special symbol <kbd>></kbd>, or <kbd>@</kbd>, or <kbd>#</kbd> for command palette, or refereces, or ... correspondigly.
    * <kbd>@</kbd><kbd>:</kbd> to group references by type
  * Keep hitting <kbd>P</kbd> to quckly navigate.
* <kbd>F1</kbd> 🔥 (or <kbd>Ctrl</kbd>+<kbd>P</kbd>,<kbd>></kbd> or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>) - magic command palette - do anything
  * <kbd>F1</kbd> "interactive playground" 🔥 - interactive tutorial on several useful features - try it now!
    * multiple cursors <kbd>Alt</kbd>+Click
    * code snippets, Emmet
  * <kbd>F1</kbd> "reload window" - as restart but faster.</kbd>
* <kbd>Alt</kbd>+<kbd>Z</kbd>: word wrap enable/disable
* Options:
  * Auto-Save
  * Trim Trailing Whitespace
  * Exclusions  ```{ "files.exclude": {"**/*.map": true} }```
    * create a folder in your project folder called ```.vscode``` and create the settings.json file in there, (i.e. ```.vscode/settings.json```). All settings within that file will affect your current workspace only.
  * Breadcrumbs
* Plugins:
  * AREPL
  * Python Docstring Generator
  * Python Test Explorer
  * BetterComment
    * ! red
    * ? blue
    * TODO: yellow
  * Project Manager ???
  * GitLens?
  * Code Runner
  * Bracket Pair Colorizer (2?)
  * python snippets????
  * Kite ?? requires installation of external bin
  * File Icons schemes
  * https://github.com/tonsky/FiraCode
```json
{
    "editor.fontFamily": "Fira Code, Consolas, 'Courier New', monospace",
    "editor.fontLigatures": true
}
```

* Move panel to right? Reason: code stays unmoved
* Reset VSCode? delete ```%userprofile%\AppData\Roaming\Code``` and ```%userprofile%\.vscode```
* ```py -0``` - list of installed Python versions
* Remote Work
* EXPECT_NEAR ==> assert 2.2 == pytest.approx(2.3, 0.001)
* strongly typed
* Enabling miniconda from VS2019:
```bat
cd "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\Extensions\Microsoft\Python\Miniconda\Miniconda3-x64\Scripts"
call activate
conda init
```