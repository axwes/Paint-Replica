# Paint Replica 2023

## Attribution
* Designed by Jackson Goerner.
* Programmed by Tan Yin Cheng for FIT 1008.
* Multiple points of valuable feedback and checking provided by Lifi Huang.
* Game Idea originated from [Chicory: A Colorful Tale](https://chicorygame.com/).

## Members

- Tan Yin Cheng 

## Setup

Note: For all of these you may need to replace `python` with `py` or `python3` depending on your operating system and python version.

```bash
python -m pip install virtualenv
python py 
```

Next, activate your virtual environment (Must be done every time you open the terminal)

Windows Bash
```
source venv/Scripts/activate
```

Windows CMD
```
venv/Scripts/activate
```

Windows Powershell
```
venv/Scripts/activate.ps1
```

Mac / Linux bash
```
source venv/bin/activate
```

Then install the requirements!
```
python -m pip install -r requirements.txt
```

## Running the program

To run the interactive version:

```bash
python main.py
```

To run the visual tests:

```bash
python -m visuals.basic
python -m visuals.complex
python -m visuals.styles
```

To run the unit tests:

```bash
python run_tests.py
```
