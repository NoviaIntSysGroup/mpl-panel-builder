# Example Structure

Each example in this directory demonstrates how to create publication-quality figures using the `mpl-panel-builder` package. The examples are organized in self-contained directories, where each directory contains a subset of four key files:

## File Structure

```
examples/
├── example_name/
│   ├── create_panels.py    # Script to generate individual panels
│   ├── create_figure.py    # Script to run panel creation + LaTeX
│   ├── config.yaml         # YAML file with the panel configuration
│   └── figure.tex          # TikZ/LaTeX file for panel assembly
├── tikz_settings.tex       # Shared TikZ settings for all examples
├── helpers.py              # Utility functions for example scripts
└── README.md               # This file
```

## File Purposes

1. `create_panels.py`: 
   - Contains the Python code to generate individual panels using `mpl-panel-builder`
   - Defines/loads panel configurations, layouts, and content
   - Saves panels as PDF files in `outputs/example_name/panels/`

1. `create_figure.py`:
   - Orchestrates the complete figure creation process
   - Runs the panel creation script
   - Compiles the LaTeX file to create the final figure
   - Saves the final figure in `outputs/example_name/figure.pdf`

1. `config.yaml`:
   - Contains panel configuration parameters
   - Defines a shared configuration for all panels
   - Highlights how the PanelBuilder config can be a subset of a larger project config file.

1. `figure.tex`:
   - Contains the TikZ/LaTeX code to assemble the panels
   - Defines the final figure layout
   - Includes panel PDFs and arranges them according to the desired layout
   - Uses shared TikZ settings from `tikz_settings.tex`

## Output Structure

```
outputs/
├── example_name/
│   ├── panels/            # Individual panel PDFs
│   │   ├── panel1.pdf
│   │   └── panel2.pdf
│   └── figure.pdf         # Final assembled figure
└── .gitkeep
```

## Usage

To use an example:
1. Navigate to the example directory.
1. Run `create_panels.py` to generate the figure panels.
1. Run `create_figure.py` to generate the complete figure.

Each example demonstrates different aspects of the package's capabilities, from basic panel creation to complex multi-panel figures. 
