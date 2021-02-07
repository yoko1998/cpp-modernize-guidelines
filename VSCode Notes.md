== Visual Studio Code notes ==
* F1 - command palet
* Alt + click = multiple cursors
* Alt + up/down = move current line up/down
* Alt+Shift = block select
* Alt+Z: word wrap
* Auto-Save in options
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
```
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

* Hiding: create a folder in your project folder called .vscode and create the settings.json file in there, (i.e. .vscode/settings.json). All settings within that file will affect your current workspace only.
```
// Workspace settings
{
    // The following will hide the js and map files in the editor
    "files.exclude": {
        "**/*.js": true,
        "**/*.map": true
    }
}
```

* Enabling miniconda from VS2019:
```
cd "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\Extensions\Microsoft\Python\Miniconda\Miniconda3-x64\Scripts"
call activate
conda init
```