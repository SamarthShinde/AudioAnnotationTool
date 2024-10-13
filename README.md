# Audio Annotation Tool

An interactive GUI application designed for efficient and user-friendly annotation of audio files. This tool segments audio into smaller clips, assigns labels, and saves annotations in a structured format for further use.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [macOS](#macos)
  - [Windows](#windows)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Annotating Audio Files](#annotating-audio-files)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Additional Notes](#additional-notes)

## Features

- **Load and Display Audio Files**: Load a folder containing audio files (WAV format). The application lists all audio files in the left panel.
- **Audio Segmentation**: Automatically segments audio files into 5-second clips.
- **Playback Controls**: Play, pause, and stop audio segments.
- **Annotation Classes**: Assign one or multiple labels to each audio segment from predefined classes:
  - 1: Male
  - 2: Female
  - 3: Engine_rev
  - 4: No_sound
  - 5: Music
- **Keyboard Shortcuts**:
  - Class Selection: Use number keys (1-5) to toggle class labels.
  - Navigation: Use arrow keys to navigate between segments.
  - Playback Control: Use the spacebar to play or pause audio.
- **Progress Tracking**: Visual progress bar indicating annotation progress.
- **Data Persistence**: Save annotations to a CSV file (`annotations.csv`), including additional metadata:
  - Audio Name
  - File Location
  - Segment Number
  - Segment Time
  - Class IDs
  - Class Names

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- FFmpeg (for audio processing with pydub)
- Git (optional, for cloning the repository)

## Installation

### macOS

1. **Install Python 3.10**  
   Ensure you have Python 3.10 installed. You can download it from the official website or install it via Homebrew:

```bash
   brew install python@3.10
```

2.	Install FFmpeg
FFmpeg is required by pydub for audio processing:

```bash
brew install ffmpeg
```

3.	Clone the Repository

```bash
git clone https://github.com/SamarthShinde/AudioAnnotationTool.git
cd AudioAnnotationTool
```

4.	Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

5.	Install Python Dependencies

```bash
pip install -r requirements.txt
```


Windows

1.	Install Python 3.10
	Download and install Python 3.10 from the official website. Ensure you check the option to add Python to your PATH during installation.
2.	Install FFmpeg
	•	Download FFmpeg from FFmpeg’s official website.
	•	Choose a build from gyan.dev.
	•	Extract the downloaded ZIP file.
	•	Add the bin directory of FFmpeg to your system’s PATH:
	•	Go to Control Panel > System and Security > System > Advanced system settings.
	•	Click Environment Variables.
	•	Under System variables, find and select Path, then click Edit.
	•	Click New and add the path to the bin directory of FFmpeg.
	•	Click OK to close all dialog boxes.
	
3.	Clone the Repository

```bash
git clone https://github.com/SamarthShinde/AudioAnnotationTool.git
cd AudioAnnotationTool
```


4.	Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```


5.	Install Python Dependencies

```bash
pip install -r requirements.txt
```


Usage

Running the Application

	1.	Navigate to the Project Directory

```bash
cd AudioAnnotationTool
```

	2.	Activate Virtual Environment (If Created)
	•	macOS:

```bash
source venv/bin/activate
```

	•	Windows:

```bash
venv\Scripts\activate
```


	3.	Run the Application

```bash
python main.py
```


Annotating Audio Files

	1.	Load Audio Folder
	•	Click the “Load Audio Folder” button.
	•	Browse and select the folder containing your WAV audio files.
	2.	Select an Audio File
	•	The left panel lists all audio files in the selected folder.
	•	Click on an audio file to load it.
	3.	View and Select Segments
	•	Below the audio file list, the segments of the selected audio file are displayed.
	•	Annotated segments are marked with a checkmark (✓).
	•	Click on a segment to select it.
	4.	Playback Controls
	•	Play: Click the “Play” button or press the Spacebar to play the selected segment.
	•	Stop: Click the “Stop” button or press the Spacebar again to stop playback.
	•	Next Segment: Click the “Next” button or press the Right Arrow key.
	•	Previous Segment: Click the “Previous” button or press the Left Arrow key.
	5.	Annotate the Segment
	•	Use the checkboxes to select the appropriate class(es) for the segment.
	•	Classes:
	•	1: Male
	•	2: Female
	•	3: Engine_rev
	•	4: No_sound
	•	5: Music
	•	You can also use the number keys (1-5) to toggle the class selection.
	6.	Annotations List
	•	The right panel displays all annotated segments with their assigned classes.
	7.	Saving Annotations
	•	Annotations are automatically saved to annotations.csv in the project directory.
	•	The CSV file includes:
	•	Audio Name
	•	File Location
	•	Segment Number
	•	Segment Time
	•	Class IDs
	•	Class Names

Keyboard Shortcuts

	•	Class Selection:
	•	Press 1: Toggle Male
	•	Press 2: Toggle Female
	•	Press 3: Toggle Engine_rev
	•	Press 4: Toggle No_sound
	•	Press 5: Toggle Music
	•	Navigation:
	•	Right Arrow: Next segment
	•	Left Arrow: Previous segment
	•	Playback Control:
	•	Spacebar: Play/Pause current segment

Project Structure

	•	main.py: Entry point of the application.
	•	gui.py: Contains the GUI implementation using PyQt5.
	•	annotations.py: Handles loading and saving annotations.
	•	audio_player.py: Manages audio playback.
	•	segmenter.py: Handles audio segmentation.
	•	converter.py: (Optional) Converts audio files to WAV format.
	•	requirements.txt: Lists all Python dependencies.
	•	annotations.csv: Generated file storing annotations.

Dependencies

Listed in requirements.txt:

	•	PyQt5: For the GUI components.
	•	pydub: For audio manipulation and segmentation.
	•	pandas: For handling annotations data.
	•	numpy: Required by pydub and pandas.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

License

This project is licensed under the MIT License.

Contact

For any questions or assistance, feel free to contact me at [samarth.shinde505@gmail.com](mailto:samarth.shinde505@gmail.com)..

Additional Notes

	•	FFmpeg Dependency:
FFmpeg is required by pydub for audio processing. Installation differs between macOS and Windows, as detailed in the installation section.
	•	Python Version:
The application requires Python 3.10 or higher due to the use of recent language features.
	•	Virtual Environment:
Using a virtual environment is recommended to manage dependencies and avoid conflicts with other Python projects.

This markdown is formatted correctly for GitHub, so when you paste it into your `README.md` file, it will display well on your GitHub repository page.