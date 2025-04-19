# Contributing to Bhargava Swara

Thank you for your interest in contributing to **Bhargava Swara**, a Python library for analyzing and synthesizing Indian classical music! We welcome contributions from the community to enhance its capabilities and make it a more powerful tool for music enthusiasts, researchers, and developers. This document outlines how you can contribute and suggests potential features and tools to add.

## How to Contribute

1. **Fork the Repository**: Start by forking the Bhargava Swara repository on GitHub.
2. **Clone Your Fork**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/Shouryaanga-Tribe/BhargavaSwaraLibrary.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Implement your feature or fix, ensuring your code follows the existing style and includes appropriate documentation.
5. **Test Your Changes**: Test your code thoroughly to ensure it works as expected.
6. **Commit Your Changes**: Commit your changes with a clear and descriptive message.
   ```bash
   git commit -m "Add feature: your feature description"
   ```
7. **Push to Your Fork**: Push your branch to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Submit a Pull Request**: Open a pull request (PR) against the main repository's `main` branch. Provide a detailed description of your changes in the PR.

## Suggested Features

We encourage contributors to add new features and tools to Bhargava Swara. Below are some ideas categorized into **analysis features** and **synthesis tools**. Feel free to propose your own ideas as well!

### Analysis Features
Enhance the library's music analysis capabilities with features such as:
- **Automatic Raga Recognition**: Develop algorithms to identify ragas automatically from audio input.
 - **Generate Pitch Histograms**: Visualize pitch distributions in a performance.
 - **Applause Detection**: Identify applause in live concert recordings.
- **Singing Mistake Detection**: Compare a student's performance against a teacher's to spot errors (requires two audio inputs).
- **Motif Spotting Task**: Recognize and highlight repeated musical motifs (Repeated pattern recognition).
- **Find Length of Pallavi**: Calculate the duration of the pallavi section in a composition.
- **Raga Verification**: Verify if a performance adheres to a specific raga's rules.
- **Pitch Extraction**: Extract pitch contours from audio for further analysis.
- **Tonic Identification**: Detect the tonic (base pitch) of a performance.
- **Pattern Characterization**: Analyze and describe recurring musical patterns.
- **Pattern Discovery**: Identify new or unexpected patterns in a piece of music.
- **Melodic Similarity**: Compare melodies across different performances or compositions.
- **Nyas Segmentation**: Segment and analyze nyas (resting notes) in a raga performance.
- **Musical Similarity Measures**: Compare two pieces of music for similarity (e.g., raga, rhythm, or melody-based).
- **Rhythm Analysis**: Analyze meter, rhythmic patterns, and structure.
- **Source Separation**: Separate vocals, instruments, or other components from mixed audio.
- **Estimating Tonic Gaps**: Detect gaps (e.g., breaths) between singing to refine tonic estimation.

### Synthesis Tools
The library currently lacks music synthesis capabilities. Contributors can add tools such as:
- **Tanpura Droid Generation**: Generate a tanpura drone sound for accompaniment.
- **Tala Generation**: Create rhythmic cycles (talas) programmatically.
- **Generate Music Based on Raga**: Synthesize music adhering to a specific raga's rules.
- **Music Imitation**: Generate music imitating the style of a given audio input.

## Development Guidelines

- **Dependencies**: Ensure new features use compatible versions of existing dependencies (`google-generativeai`, `librosa`, `matplotlib`, `numpy`) or justify adding new ones.
- **Code Style**: Follow PEP 8 guidelines for Python code.
- **Documentation**: Add docstrings and update the README with any new features or dependencies.
- **Testing**: Include tests for new features where possible.
- **Audio Formats**: Ensure compatibility with WAV and MP3 files, consistent with the current library.

## Getting Help

If you have questions or need assistance, feel free to:
- Open an issue on the GitHub repository.
- Reach out to the maintainers.

## License

By contributing to Bhargava Swara, you agree that your contributions will be licensed under the same license as the project (see the repository's LICENSE file).

Thank you for helping make Bhargava Swara a richer tool for Indian classical music analysis and synthesis!
