# LiDARacks
Python toolkit to generate physically-grounded LiDAR anomalies for robust sensor testing: Background noise (simulating adverse weather conditions), Zero-Range Background (modeling sensor obstruction), Electromagnetic Interference (representing electronic noise), and Occlusion (ray diffusion/absorption).

## Usage/Examples
The toolkit requires numpy to work, and in our implementation the version is '1.26.3'.

```python
# Example of LiDARacks
import numpy as np
import LiDARacks
sph_path = "PATH\\TO\\sph_point_cloud.npy" # The spherical point clouds
sph_point_clouds = np.load(sph_path)
severity_level = 3 # From 0 to 4
type_of_noise = 'EMI' # EMI, Occlusion, Background, ZRB
new_sph_point_clouds = LiDARacks.lidaracks(sph_point_clouds,severity_level,type_of_noise)
```

## Files
-sph_point_cloud.npy : Example of spherical point clouds

-LiDARacks.ipynb : The Notebook to generate the different noises/attacks

-LiDARacks.py : The Python script containing the function for LiDARacks

