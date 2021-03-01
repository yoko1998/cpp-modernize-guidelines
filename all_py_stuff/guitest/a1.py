import os
import sys
import PySimpleGUI as sg

sg.theme("GreenTan")
from PySimpleGUI import (
    Checkbox,
    Button,
    ButtonMenu,
    Canvas,
    Column,
    Combo,
    Frame,
    Graph,
    Image,
    Input,
    Listbox,
    Menu,
    Multiline,
    OptionMenu,
    Output,
    Pane,
    ProgressBar,
    Radio,
    Slider,
    Spin,
    StatusBar,
    Tab,
    TabGroup,
    Table,
    Text,
    Tree,
    TreeData,
    VerticalSeparator,
    Window,
    Sizer,
)

M = sg.MLine
B = sg.B

# This layout uses the user defined "M" element as well as the PySimpleGUI Button shortcut, B.
layout = [[M(size=(30, 3))], [B("OK")]]

window = sg.Window("Shortcuts", layout)
event, values = window.read()
sg.popup_scrolled(event, values)
window.close()

col2 = Column(
    [
        [
            Frame(
                "Accounts:",
                [
                    [
                        Column(
                            [
                                [
                                    Listbox(
                                        ["Account " + str(i) for i in range(1, 16)],
                                        key="-ACCT-LIST-",
                                        size=(15, 20),
                                        select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
                                    ),
                                ]
                            ],
                            size=(150, 400),
                        )
                    ]
                ],
            )
        ]
    ],
    pad=(0, 0),
)

col1 = Column(
    [
        # Categories frame
        [
            Frame(
                "Categories:",
                [
                    [
                        Radio(
                            "Websites",
                            "radio1",
                            default=True,
                            key="-WEBSITES-",
                            size=(10, 1),
                        ),
                        Radio("Software", "radio1", key="-SOFTWARE-", size=(10, 1)),
                    ]
                ],
            )
        ],
        # Information frame
        [
            Frame(
                "Information:",
                [
                    [
                        Text(),
                        Column(
                            [
                                [Text("Account:")],
                                [Input(key="-ACCOUNT-IN-", size=(19, 1))],
                                [Text("User Id:")],
                                [
                                    Input(key="-USERID-IN-", size=(19, 1)),
                                    Button("Copy", key="-USERID-"),
                                ],
                                [Text("Password:")],
                                [
                                    Input(key="-PW-IN-", size=(19, 1)),
                                    Button("Copy", key="-PASS-"),
                                ],
                                [Text("Location:")],
                                [
                                    Input(key="-LOC-IN-", size=(19, 1)),
                                    Button("Copy", key="-LOC"),
                                ],
                                [Text("Notes:")],
                                [Multiline(key="-NOTES-", size=(25, 5))],
                            ],
                            size=(235, 350),
                            pad=(0, 0),
                        ),
                    ]
                ],
            )
        ],
    ],
    pad=(0, 0),
)

col3 = Column(
    [
        [
            Frame(
                "Actions:",
                [
                    [
                        Column(
                            [
                                [
                                    Button("Save"),
                                    Button("Clear"),
                                    Button("Delete"),
                                ]
                            ],
                            size=(450, 45),
                            pad=(0, 0),
                        )
                    ]
                ],
            )
        ]
    ],
    pad=(0, 0),
)

layout = [[col1, col2], [col3]]

window = Window("Passwords", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break

window.close()

# # All the stuff inside your window.
# layout = [
#     [sg.Text(f"{sys.version}")],
#     [sg.Text(f"{sys.executable}")],
#     [sg.Text("Enter something"), sg.InputText()],
#     [sg.Output(size=(80, 20))],
#     [sg.Button("Ok"), sg.Button("Cancel")],
# ]

# # Create the Window
# window = sg.Window("Window Title", layout, return_keyboard_events=True)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if (
#         event == sg.WIN_CLOSED or event == "Cancel" or event == "Escape:27"
#     ):  # if user closes window or clicks cancel
#         break
#     print("You entered ", values[0], " event:", str(event), " value:", str(values))
#     window.Refresh()

# window.close()