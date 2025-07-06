import os
from numpy import eye
from pathlib import Path
from typing import Literal, Union
import numpy as np
import matplotlib.pyplot as plt

# The imports we will need to run Probabilistic Mission Design
from promis_project import (StaRMap, ProMis, 
                            PolarLocation, CartesianMap, CartesianLocation, CartesianRasterBand, CartesianCollection,
                            OsmLoader
                           )

def promis_execution(generated_logic:str, special_zone_location:tuple, operator_location, city_attr:Union[Literal["darmstadt","berlin","frankfurt"], tuple] = "darmstadt", load_uam=True):
    """
    args:
        generated_logic: from langda
        special_zone_location: 
        operator_location: 
        city_attr: name of the city, one of "darmstadt","berlin","frankfurt"
        load_uam: load already existing uam file
    """
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    save_dir = current_dir / "data"
    save_dir.mkdir(parents=True, exist_ok=True)

    # The features we will load from OpenStreetMap
    # The dictionary key will be stored as the respective features location_type
    # The dictionary value will be used to query the relevant geometry via Overpass
    feature_description = {
        "park": "['leisure' = 'park']",
        "primary": "['highway' = 'primary']",
        "primary_link": "['highway' = 'primary_link']",
        "secondary": "['highway' = 'secondary']",
        "secondary_link": "['highway' = 'secondary_link']",
        "tertiary": "['highway' = 'tertiary']",
        "service": "['highway' = 'service']",
        "crossing": "['footway' = 'crossing']",
        "bay": "['natural' = 'bay']",
        "rail": "['railway' = 'rail']",
    }

    # Covariance matrices for some of the features
    # Used to draw random translations representing uncertainty for the respective features
    covariance = {
        "primary": 15.0 * eye(2),
        "primary_link": 15.0 * eye(2),
        "secondary": 10.0 * eye(2),
        "secondary_link": 10.0 * eye(2),
        "tertiary": 5 * eye(2),
        "service": 2.5 * eye(2),
        "operator": 20 * eye(2),
    }

    # The mission area, points that will be estimated from 25 samples and points that will be interpolated
    # if city_attr == "darmstadt":
    #     origin = PolarLocation(latitude=49.878091, longitude=8.654052) # Darmstadt
    # elif city_attr == "frankfurt":
    #     origin = PolarLocation(latitude=50.110924, longitude=8.682127) # Frankfurt
    # elif city_attr == "berlin":
    #     origin = PolarLocation(latitude=52.5186, longitude=13.4081) # Berlin
    # elif isinstance(city_attr, tuple):
    origin = PolarLocation(latitude=operator_location[0], longitude=operator_location[1])

    width, height = 1000.0, 1000.0
    number_of_random_maps = 20

    support = CartesianRasterBand(origin, (26, 26), width, height)  # This is the set of points that will be directly computed through sampling (expensive)
    target = CartesianRasterBand(origin, (161, 161), width, height)  # This is the set of points that will be interpolated from the support set (cheap)

    if not load_uam:
        print("Building Uncertainty Annotated Map (UAM)...")
        # Setting up the Uncertainty Annotated Map from OpenStreetMap data 49.875, 8.6563899999
        uam = None
        uam = OsmLoader(origin, (width, height), feature_description).to_cartesian_map()
        uam.features.append(CartesianLocation(0, 0, location_type="operator"))  # We can manually add additional features
        uam.features.append(CartesianLocation(special_zone_location[0], special_zone_location[1], location_type="special_zone"))  # We can manually add additional features
        uam.apply_covariance(covariance)  # Assigns the covariance matrices defined earlier
        uam.save(f"{save_dir}/uam_{city_attr}.pkl")  # We can save and load these objects to avoid recomputation

    try:
        print("Initializing StaRMap...")
        # Setting up the probabilistic spatial relations from the map data
        star_map = StaRMap(target, CartesianMap.load(f"{save_dir}/uam_{city_attr}.pkl"))
        star_map.initialize(support, number_of_random_maps, generated_logic)  # This estimates all spatial relations that are relevant to the given logic
        # star_map.add_support_points(support, number_of_random_maps, ["distance"], ["primary"])  # Alternatively, we can estimate for specific relations
        star_map.save(f"{save_dir}/star_map_{city_attr}.pkl")

        print("Running ProMis solver...")
        # Solve the mission area with ProMis
        promis = ProMis(StaRMap.load(f"{save_dir}/star_map_{city_attr}.pkl"))
        landscape = promis.solve(support, generated_logic, n_jobs=4, batch_size=1)
        landscape.save(f"{save_dir}/landscape.pkl")

    except Exception as e:
        print(e)
        return False

    set_path(0, 0, [(0,0)],save_dir)

    return True

def get_confidence_at_point(landscape, east: float, north: float) -> float:

    # 找到最接近的网格点
    distances = np.sqrt((landscape.data.east - east)**2 + 
                        (landscape.data.north - north)**2)
    closest_idx = distances.idxmin()
    return landscape.data.loc[closest_idx, 'v0']

def set_path(x_pt, y_pt, path, save_dir):
    """
    args:
        x_pt, y_pt: will be marked as special mark on the map
        save_dir: save directory
    """
    print("Rendering mission landscape...")
    landscape = CartesianCollection.load(f"{save_dir}/landscape.pkl")

    print(get_confidence_at_point(landscape, x_pt, y_pt))
    image = landscape.scatter(s=0.4, plot_basemap=True, rasterized=True, cmap="coolwarm_r", alpha=1)
    cbar = plt.colorbar(image, ticks=[0.0, 0.5, 1.0], aspect=30, pad=0.02)
    cbar.ax.set_yticklabels(['0.0', '0.5', '1.0'])
    cbar.solids.set(alpha=1)

    ticks = [-500, 0, 500]
    labels = ["-500", "0", "500"]
    
    plt.xlabel("Easting / km")
    plt.ylabel("Northing / km")
    plt.xticks(ticks, labels)
    plt.yticks(ticks, labels)
    plt.xlim([-500, 500])
    plt.ylim([-500, 500])
    plt.title("P(mission_landscape)")
    confidence_list = []
    # for i, path in enumerate(path_lists):
    #     confidence_list = []
    valid = True
    for (x,y) in path:
        confidence = np.around(get_confidence_at_point(landscape, x, y),3)
        if confidence < 0.4:
            confidence_list.append(f"Invalid")
            valid = False
        else:
            confidence_list.append(confidence)
    if valid:
        marker = "."
    else:
        marker = "x"
    plt.plot(*zip(*path), 
            marker=marker,
            markersize=5,
            linewidth=1.5,
            alpha=0.8,
            # label=f'Path{i}'
            )
    
    print(f"Path: {valid}",confidence_list)
    
    plt.title("Path Validity Visualization")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')

    # —— Special mark at x_pt, y_pt —— #
    plt.scatter(
        x_pt, y_pt,
        marker='*',
        s=100,
        c='red',
        edgecolors='black',
        linewidths=1.2,
        zorder=5          # 确保点画在最上层
    )
    if not len(path) > 1:
        plt.savefig(
            f"{save_dir}/mission_landscape.png", 
            dpi=100,
            format='png',
            bbox_inches='tight',
            transparent=False)
        plt.close()
        print(f"Landscape plot saved to mission_landscape.png")
    else:
        plt.savefig(
            f"{save_dir}/validation_path.png", 
            dpi=100,
            format='png',
            bbox_inches='tight',
            transparent=False)
        plt.close()
        print(f"Landscape plot saved to validation_path.png")
    return confidence_list