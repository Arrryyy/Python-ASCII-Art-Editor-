# Python-ASCII-Art-Editor-
# ASCII Art Converter

This repository contains a Python program, `ascii_art.py`, which is a graphical user interface (GUI) for an ASCII art editor. The program allows you to convert an image to ASCII text using the ASCII art technique.

## Installation

To run the ASCII Art Converter, please follow these steps:

1. Clone the repository to your local machine or download the ZIP file and extract it.

```bash
git clone https://github.com/your-username/ascii-art-converter.git
```

2. Make sure you have Python installed on your system.

3. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Open a terminal or command prompt and navigate to the repository's directory.

2. Run the `ascii_art.py` file using the following command:

```bash
python ascii_art.py
```

3. The GUI window will open, providing various options for image conversion.

4. Select an image by either entering the path in the designated entry or using the file selection dialogue accessible via the button.

5. Specify the character image width, height, and font size using the respective entries.

6. Choose the grayscale conversion method by clicking on the appropriate button.

7. Enter a character set for the conversion in the designated entry.

8. Customize any other desired settings.

9. Click on the "Generate" button to start the conversion process.

10. The generated ASCII text will be displayed in the main element of the GUI. If the text doesn't fit within the window, scroll bars will appear.

11. To save the generated text as a .txt file, click on the "Save Text" button, and a file selection dialogue will open. Choose the desired location and save the file.

## Task Details

- All rules from the slide set `00_exercise_performance_general.pdf` apply.

- The main file is called `ascii_art.py`.

- Deadline is 2023-06-05 (Monday), 23.59 o'clock.

- There are 10 points to achieve:

  - 1 point for sticking to the general rules.
  
  - 2 points for a GUI layout that contains all the required elements and options.
  
  - 2 points for all options being read correctly from the GUI for the conversion and proper default values.
  
  - 3 points for a working conversion of an image to ASCII.
  
  - 2 points for having the conversion done with a thread, which is meaningfully joined to the main thread at some point.

## Additional Information

- ASCII art: [https://en.wikipedia.org/wiki/ASCII_art](https://en.wikipedia.org/wiki/ASCII_art)

- The program converts an image to ASCII text by performing the following steps:

  - The input image is converted to grayscale.
  
  - A set of characters is provided as input.
  
  - These characters are rendered as little images, with customizable width, height, and font size.
  
  - For each possible position in the input image, the distance between the original image crop and all the character images is computed.
  
  - The character with the lowest distance is selected for the final ASCII text.

- The GUI parameters and main elements of the GUI include:

  - Image path entry and file selection dialogue button.
  
  - Character image width, height, and font size entries with proper labels.
  
  - Grayscale conversion method selection button.
  
  - Character set entry for conversion.
  
  - Generate button to initiate the conversion with the current options.
  
  - Save Text button to save the generated text as a .txt file using a file selection dialogue.
  
  - The generated ASCII text is displayed as the main element of the GUI, with scroll
