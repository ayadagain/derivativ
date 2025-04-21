# Derivativ - AI-Powered Math Education

Derivativ is a project that leverages AI to generate interactive video tutorials, exercises, and educational content for mathematics. Using Manim (Mathematical Animation Engine) and AI voice synthesis, it creates engaging and dynamic math learning materials.

## Current Implementation

The project currently uses Manim to generate precise mathematical visualizations and animations, with voice-over integration for enhanced learning experience.

## Future Development

The next phase of development will focus on:
- Integration with Wolfram for advanced mathematical computations
- Development of a Model Context Protocol (MCP) server for reusability
- Generation based on topic and level

## Features

- AI-generated mathematical animations
- Voice-over narration for tutorials
- Interactive examples and exercises
- Support for various mathematical concepts and visualizations

## Prerequisites

- Python 3.7 or higher
- FFmpeg
- LaTeX (for mathematical expressions)
- SoX (for audio processing)

## Installation

1. Install Manim:
```bash
pip install manim
```

2. Install voice-over dependencies:
```bash
pip install --upgrade "manim-voiceover[azure,gtts]"
```

## Project Structure

- `manim_examples/`: Contains example animations and tutorials
  - `diagram_animation.py`: Demonstrates binomial to Poisson convergence
  - `equation_animation.py`: Shows equation transformations
  - `solution_animation.py`: Example of problem-solving animations
  - `gtts-example.py`: Text-to-speech integration example

## Usage

To run an example animation:

```bash
manim -pql manim_examples/diagram_animation.py BinomialToPoissonConvergence
```

Replace `diagram_animation.py` with any other example file and `BinomialToPoissonConvergence` with the appropriate scene class name.

## Examples

1. **Binomial to Poisson Convergence**
   - Visualizes the convergence of binomial distribution to Poisson distribution
   - Demonstrates probability mass functions
   - Includes dynamic parameter changes

2. **Equation Animations**
   - Shows step-by-step equation transformations
   - Highlights mathematical operations
   - Includes voice-over explanations

3. **Solution Animations**
   - Presents problem-solving processes
   - Combines visual and audio explanations
   - Interactive step-by-step demonstrations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 