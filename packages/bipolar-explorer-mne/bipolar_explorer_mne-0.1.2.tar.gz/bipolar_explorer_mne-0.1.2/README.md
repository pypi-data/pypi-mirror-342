# BipolarExplorerMNE

A simple Python package built on top of [MNE-Python](https://mne.tools) to visualize **bipolar montages** of non-EEG signals (e.g., ECG, EMG, EOG) from `.EDF` or `.EEG` files, even when channel names are inconsistent or messy.

---

## 🚀 Motivation

Working with physiological recordings from hospital systems often means dealing with inconsistently named or misconfigured channels. While EEG data typically follows the 10-20 naming convention, **ECG and other physiological signals often don't** — you'll find channel names like:

- `ECG-`, `ECG+`
- `E`, `Ecg`
- `-0`, `Ecg`
- ...and other unpredictable combinations.

On top of that, **electrode placement can sometimes be reversed**, making interpretation more difficult.

This package helps **quickly visualize possible bipolar combinations** between selected channels, so you can identify useful signals and confirm polarity before moving on to analysis.

---

## 📦 Features

- Load `.EDF` or `.EEG` files using MNE
- Visualize bipolar signals from non-EEG channels
- Interactive (plotly) plots to scroll and inspect signals
- Designed for **manual exploration and verification**

---

## 🔧 Installation

You can install the package via pip (if uploaded to PyPI) or directly from GitHub:

```bash
pip install bipolar-explorer-mne
```

or

```bash
pip install git+https://github.com/anascacais/BipolarExplorerMNE.git
```

---

## Usage

```python
from bipolar_explorer_mne.bipolar_explorer import BipolarExplorer

# Load the data
explorer = BipolarExplorer(filepath='test_file.edf')

# Optional: list all available channels
explorer.list_channels()

# Open the UI
bipolar_config, id = explorer.explore(extra_ui_info=['id'])
```

---

## Notes

- This tool is primarily meant for **channel exploration**, not as an automated pipeline.
- You should still verify the actual electrode placements and channel meaning based on metadata or clinical notes when available.
- It assumes you have `MNE` **installed and working** in your environment.
