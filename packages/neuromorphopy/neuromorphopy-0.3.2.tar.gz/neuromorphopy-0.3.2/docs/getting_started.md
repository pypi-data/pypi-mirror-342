# Getting Started

This guide will help you get up and running with `neuromorphopy` quickly. neuromorphopy helps you download and work with neuron morphology data from NeuroMorpho.org.

## Installation

**Using `uv` (Recommended):**

The easiest way to install `neuromorphopy` as a standalone CLI tool is with [`uv`](https://github.com/astral-sh/uv):

```bash
# install the latest release
uv tool install neuromorphopy
# or install the latest development version from GitHub
uv tool install git+https://github.com/kpeez/neuromorphopy.git
```

**Using `pip`:**

Alternatively, you can install `neuromorphopy` into your project environment using `pip`:

```bash
# install the latest release
pip install neuromorphopy
# or install the latest development version directly from GitHub
pip install git+https://github.com/kpeez/neuromorphopy.git
```

## Configuration

## Basic Usage

### 1. Create a Query File

Create a text file named `query.yaml` (or `.json`) with your search criteria:

```yaml
# query.yaml
filters:
  species: ["mouse"]
  brain_region: ["neocortex"]
  cell_type: ["pyramidal"]
sort: # optional
  field: "neuron_id"
  ascending: false
```

To download all neurons, use an empty filter set:

```yaml
# query_all.yaml
filters: {}
```

### 2. Explore Search Fields

Before writing your query, you might want to see what fields and values are available. Use the `fields` command:

```bash
# List all available query fields
neuromorpho fields

# List valid values for a specific field (e.g., species)
neuromorpho fields species
```

### 3. Preview Download (Optional)

Before downloading potentially thousands of files, you can preview what your query will match using the `preview` command:

```bash
neuromorpho preview -q query.yaml
```

This will validate your query file and show you:

- The total number of neurons matching your criteria.
- The target output directory and metadata filename.
- A few sample neuron names that would be downloaded.

This command does *not* download any neuron files or create log files.

### 4. Download Neurons

Once your query is ready, use the `download` command:

```bash
neuromorpho download -q query.yaml -o ./my_neurons
```

This will:

- Validate your query file.
- Create the output directory (`./my_neurons` in this case, defaults to `./neurons`).
- Download all matching neuron SWC files into the `downloads/` subdirectory.
- Save a `metadata.csv` file in the output directory with information about the downloaded neurons.
- Create a log file in the output directory.

## Understanding the Downloaded Data

After downloading, you'll have:

1. A collection of .swc files (one per neuron) containing 3D neuron reconstructions
2. A metadata.csv file containing information about each downloaded neuron

## Common Options for `download`

```bash
# Specify output directory
neuromorpho download query.yaml -o ./my_data

# Change metadata filename
neuromorpho download query.yaml -m neuron_info.csv

# Download fewer neurons concurrently (default 20)
neuromorpho download query.yaml -c 5

# Group downloads by species and brain region
neuromorpho download query.yaml -g species,brain_region

# See more detailed progress output
neuromorpho download query.yaml --verbose

# Suppress non-error output
neuromorpho download query.yaml --quiet

# Disable writing log file
neuromorpho download query.yaml --no-log
```

## Next Steps

- See [detailed CLI usage](cli/basic_usage.md) for more commands
- Learn about [advanced CLI features](cli/advanced_options.md)
- Understand [neuron data formats](user_guide/data_formats.md)
