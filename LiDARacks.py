import numpy as np

def lidaracks(sph_point_clouds, severity_level=0, type_of_noise='EMI'):

    if type_of_noise not in ['EMI', 'Occlusion', 'Background', 'ZRB']:
        raise ValueError("type_of_noise must be either 'EMI' or 'Occlusion' or 'Background' or 'ZRB'")
    
    if severity_level < 0 or severity_level > 4:
        raise ValueError("severity_level must be between 0 and 4")
    
    if not isinstance(sph_point_clouds, np.ndarray):
        raise TypeError("sph_point_clouds must be a numpy array")
    
    if sph_point_clouds.ndim != 2 or sph_point_clouds.shape[1] != 3:
        raise ValueError("sph_point_clouds must be a 2D numpy array with shape (N, 3)")
    
    if type_of_noise == 'EMI':
        severity = [0.5, 1, 1.5, 2, 2.5][severity_level]

        num_points = sph_point_clouds.shape[0]

        freq = 615e6
        cycles = 12
        samples_per_cycle = 5.1
        sample_rate = samples_per_cycle * freq
        duration = cycles / freq
        t = np.linspace(0, duration, num_points, endpoint=False)
        phase_shift = np.random.uniform(0, 2 * np.pi)
        sine_wave = severity * np.sin(2 * np.pi * freq * t + phase_shift)

        sph_point_cloud_interfered = sph_point_clouds.copy()
        sph_point_cloud_interfered[:, 0] += sine_wave

        sph_point_cloud_interfered[:, 0] = np.clip(sph_point_cloud_interfered[:, 0], 0, 5)

        return sph_point_cloud_interfered
    
    elif type_of_noise == 'Occlusion':
        severity = [2,3,4,5,6][severity_level]

        planar_degree = 360/61 
        theta = np.arange(-180, 180, planar_degree)  

        theta = np.array([t for t in theta if t in sph_point_clouds[:, 1]])
        theta = np.unique(theta)  
        theta = np.random.choice(theta, severity, replace=False)

        sph_point_cloud_occluded = sph_point_clouds.copy()
        sph_point_cloud_occluded = np.array([point for point in sph_point_cloud_occluded if point[1] not in theta])
        return sph_point_cloud_occluded
    
    elif type_of_noise == 'Background':
        severity = [45,40,35,30,20][severity_level]

        planar_degree = 360/61

        rhos = np.random.uniform(0.5,4.5,round(sph_point_clouds.shape[0]//severity))
        theta = np.random.choice(np.arange(-180,180,planar_degree),round(sph_point_clouds.shape[0]//severity))
        phi = np.random.choice(np.arange(75,101,5),round(sph_point_clouds.shape[0]//severity))

        for i, (rho_new, theta_new, phi_new) in enumerate(zip(rhos, theta, phi)):
            matching_indices = np.where(sph_point_clouds[:, 1] == theta_new)[0]
            if len(matching_indices) > 0:
                for idx in matching_indices:
                    if rho_new >= sph_point_clouds[idx, 0]:
                        rhos[i] = np.random.uniform(0, sph_point_clouds[idx, 0])
                        break
                    
        sph_point_cloud_background = sph_point_clouds.copy()
        sph_point_cloud_background = np.append(sph_point_cloud_background, np.column_stack((rhos, theta, phi)),axis=0)
        return sph_point_cloud_background
    
    elif type_of_noise == 'ZRB':
        severity = [1,2,3,4,5][severity_level]

        planar_degree = 360/61 
        rhos = np.zeros(severity)  
        theta = np.random.choice(np.arange(-180, 180, planar_degree), severity, replace=False)
        phi = np.random.choice(np.arange(75, 101, 5), severity, replace=False)

        sph_point_cloud_corrupted = sph_point_clouds.copy()
        sph_point_cloud_corrupted = np.append(sph_point_cloud_corrupted, np.column_stack((rhos, theta, phi)), axis=0)
        return sph_point_cloud_corrupted