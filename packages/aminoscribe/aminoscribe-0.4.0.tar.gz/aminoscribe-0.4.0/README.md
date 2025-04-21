# AminoScribe

AminoScribe is a Python module for generating simulated nanopore squiggle signals from amino acid sequences. It provides tools for sequence-based signal generation, time warping, noise addition, and signal processing such as filtering, normalization, and downsampling.

## Features

- Generate idealized templates for amino acid sequences.
- Add time-domain warping and amplitude noise to simulate realistic signals.
- Apply low-pass Bessel filtering to reduce noise.
- Normalize signals using min-max scaling.
- Downsample signals for efficient processing.
- Fetch protein sequences using UniProt accession numbers.

## Installation

Install AminoScribe using pip:

```bash
pip install aminoscribe
```

## Usage

### Generate a Squiggle Signal

You can generate a simulated squiggle signal from an amino acid sequence or a protein ID:

```python
from aminoscribe.aminoscribe import generate_squiggle

# Generate a squiggle signal from a sequence
signal = generate_squiggle(sequence="MKTLLDLGYTMKTLLLTLVVTMKTLLDLGYTMKTLLLTLVVLLTLVVVTIVCLDLGYTLGYT", 
                           normalize=True, 
                           downsample=True, 
                           downsample_factor=5)

# Generate a squiggle signal from a protein ID
signal = generate_squiggle(protein_id="P12345", 
                           filter_noise=True, 
                           bessel_N=8, 
                           bessel_Wn=0.1)
```

### Generate an Idealized Template

If you only need the idealized template without noise or processing:

```python
sequence = "YYYYYSTSSDGDEEDGDDSTSYYYYYSTSSDGEDDEGDDSTSYYYYYSTSSDGEDEDGDDSTSYYYYYSTSSDGD"
template = generate_squiggle(sequence=sequence, template_only=True)
```

### Fetch Protein Sequence

Retrieve a protein sequence using its UniProt accession number:

```python
from aminoscribe.aminoscribe import get_protein_seq

sequence = get_protein_seq("E2RYF6")
```

## Function Reference

### `generate_squiggle`

Generates a simulated squiggle signal from an amino acid sequence or protein ID.

**Parameters:**
- `sequence` (str, optional): Amino acid sequence.
- `protein_id` (str, optional): Protein ID to fetch the sequence.
- `base_template` (optional): Base template signal.
- `seed` (optional): Random seed for reproducibility.
- `template_only` (bool, optional): Return idealized template only.
- `cterm` (str, optional): Sequence to append to the C-terminal end.
- `nterm` (str, optional): Sequence to prepend to the N-terminal end.
- `filter_noise` (bool, optional): Apply low-pass Bessel filter.
- `bessel_N` (int, optional): Order of the Bessel filter.
- `bessel_Wn` (float, optional): Normalized cutoff frequency.
- `normalize` (bool, optional): Apply min-max normalization.
- `norm_cutoff` (int, optional): Number of elements for normalization.
- `downsample` (bool, optional): Apply linear downsampling.
- `downsample_factor` (float, optional): Downsampling factor.

**Returns:**
- List of float values representing the processed squiggle signal.

### `get_protein_seq`

Fetches a protein sequence using its UniProt accession number.

**Parameters:**
- `protein_id` (str): UniProt accession number.

**Returns:**
- Amino acid sequence as a string.

## License

This project is licensed under Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). See the `LICENSE` file for details.

## Contributing

Source code lives at https://github.com/uwmisl/Amino-Scribe. Please submit a pull request or open an issue for any bugs or feature requests.

## Contributors
## Contributors

- **Melissa Queen** — Lead author and maintainer
- **Daphne Kontogiorgos-Heintz** — Computed and incorporated the amino acid value and variance numbers
