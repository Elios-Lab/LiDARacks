# LiDARacks

A lightweight Python toolkit for injecting physically-grounded anomalies into LiDAR point clouds, intended for robustness evaluation and stress-testing of perception models.

LiDARacks operates directly on spherical-coordinate point clouds and implements four corruption models, each with five configurable severity levels.

## Corruption Models

| Type | Key | Physical phenomenon | Effect on the point cloud |
| --- | --- | --- | --- |
| Background Noise | `Background` | Adverse weather (rain, fog, dust) | Inserts spurious returns at ranges shorter than the true surface |
| Zero-Range Background | `ZRB` | Sensor obstruction (debris, water on the lens) | Inserts points at `rho = 0` on randomly selected azimuths |
| Electromagnetic Interference | `EMI` | Electronic noise coupling into the range channel | Adds a sinusoidal range error across the scan, clipped to the valid range |
| Occlusion | `Occlusion` | Ray diffusion or absorption | Removes all returns along randomly selected azimuths |

Severity is selected with `severity_level` in the range `0`–`4`, mapped per corruption type as follows:

| Type | Severity parameter | `0` | `1` | `2` | `3` | `4` |
| --- | --- | --- | --- | --- | --- | --- |
| `Background` | Points added ≈ `N / value` | 45 | 40 | 35 | 30 | 20 |
| `ZRB` | Zero-range points added | 1 | 2 | 3 | 4 | 5 |
| `EMI` | Range-error amplitude (m) | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 |
| `Occlusion` | Azimuths removed | 2 | 3 | 4 | 5 | 6 |

## Input Format

Point clouds are expected as a `numpy.ndarray` of shape `(N, 3)` in spherical coordinates, with columns ordered `[rho, theta, phi]`:

| Column | Meaning | Range | Resolution |
| --- | --- | --- | --- |
| `rho` | Radial distance (m) | `0` – `5` | continuous |
| `theta` | Azimuth (deg) | `-180` – `180` | `360 / 61` ≈ 5.90° |
| `phi` | Elevation (deg) | `75` – `100` | `5°` |

## Requirements

- Python 3.8+
- NumPy (developed and tested with `1.26.3`)
- Matplotlib (only required to run the visualizations in the notebook)

```bash
pip install numpy matplotlib
```

## Usage

```python
import numpy as np
import LiDARacks

sph_point_clouds = np.load("path/to/sph_point_cloud.npy")   # shape (N, 3)

corrupted = LiDARacks.lidaracks(
    sph_point_clouds,
    severity_level=3,        # 0 to 4
    type_of_noise="EMI",     # 'EMI', 'Occlusion', 'Background', 'ZRB'
)
```

### API

```python
lidaracks(sph_point_clouds, severity_level=0, type_of_noise='EMI') -> np.ndarray
```

**Parameters**

- `sph_point_clouds` (`np.ndarray`): input cloud of shape `(N, 3)` in `[rho, theta, phi]` order.
- `severity_level` (`int`): corruption severity, `0`–`4`.
- `type_of_noise` (`str`): one of `'EMI'`, `'Occlusion'`, `'Background'`, `'ZRB'`.

**Returns**

A new `np.ndarray` of shape `(M, 3)`. The input array is not modified. Note that `M` differs from `N` for the additive (`Background`, `ZRB`) and subtractive (`Occlusion`) corruptions; only `EMI` preserves the point count.

**Raises**

- `TypeError` if `sph_point_clouds` is not a NumPy array.
- `ValueError` if the input shape is not `(N, 3)`, if `severity_level` is outside `0`–`4`, or if `type_of_noise` is unrecognized.

### Reproducibility

The library function does not seed the random number generator. Set a global seed before calling it if deterministic output is required:

```python
np.random.seed(42)
corrupted = LiDARacks.lidaracks(sph_point_clouds, 3, "Background")
```

## Repository Contents

| File | Description |
| --- | --- |
| `LiDARacks.py` | Library module exposing the `lidaracks` function |
| `LiDARacks.ipynb` | Notebook walking through each corruption model with before/after plots |
| `sph_point_cloud.npy` | Sample spherical point cloud (234 points) for testing and demos |
