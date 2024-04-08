# photoshop-timer
Simple timer to track how much time is spent on each image and how many steps were taken to edit it.

## Features

- Tracks the time spent on each image in Adobe Photoshop.
- Displays the elapsed time and history states for each document.
- Updates the display every second.
- Uses ASCII art to display the elapsed time for the currently active document.
- Keeps record of all edited images.

![photoshop-timer-demoASCII](https://github.com/xRyul/photoshop-timer/assets/47340038/df241982-3900-41f0-b9b4-09b067e57376)

![photoshop-timer-ASCIIdemo](https://github.com/xRyul/photoshop-timer/assets/47340038/35716628-5e36-486a-a429-bc0e9b8d2544)



# Requirements
- macOS (we use AppleScript to detect which document is open in Photoshop)
- Adobe Photoshop
- `pyfiglet` Python library
- `curses` Python library


## Usage

1. Open Photoshop
2. Run either directly from VScode or any other terminal "python3 main.py"
3. The elapsed time and history states for each document will be displayed in the terminal.