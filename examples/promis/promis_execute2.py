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

# All the example paths:
path_lists = [
    [(-50,265), (-75,265), (-100,265), (-120,248), (-140,230), (-145,215), (-150,200), (-137,177), (-123,153), (-110,130), (-95,115), (-80,100), (-63,83), (-47,67), (-30,50), (-20,33), (-10,17), (0,0)],
    [(110,-370), (105,-360), (100,-350), (90,-335), (80,-320), (70,-300), (60,-280), (55,-250), (50,-220), (50,-190), (50,-160), (50,-138), (50,-115), (23,-98), (-5,-80), (3,-55), (10,-30), (7,-20), (4,-10), (0,0)],
    [(-350,50), (-325,45), (-300,40), (-260,40), (-220,40), (-200,30), (-180,20), (-150,20), (-120,20), (-90,10), (-60,0), (-40,0), (-20,0), (0,0)],
    [(-350,50), (-330,25), (-310,0), (-295,-20), (-280,-40), (-270,-65), (-260,-90), (-260,-110), (-260,-130), (-245,-105), (-230,-80), (-205,-70), (-180,-60), (-150,-45), (-120,-30), (-90,-30), (-60,-30), (-43,-30), (-25,-30), (-13,-20), (-7,-10), (0,0)],
    [(-230,290), (-215,275), (-200,260), (-185,240), (-170,220), (-150,210), (-130,200), (-115,175), (-100,150), (-90,125), (-80,100), (-60,80), (-40,60), (-30,40), (-20,20), (-13,13), (-7,7), (0,0)],
    [(-350,50), (-325,45), (-300,40), (-275,60), (-250,80), (-225,80), (-200,80), (-185,90), (-170,100), (-145,115), (-120,130), (-105,150), (-90,170), (-65,170), (-40,170), (-20,180), (0,190), (20,170), (40,150), (35,130), (30,110), (10,85), (-10,60), (-10,40), (-10,20), (-7,13), (-3,7), (0,0)],
    [(-90,-278), (-80,-290), (-60,-290), (-20,-290), (-20,-270), (-20,-250), (-10,-235), (0,-220), (15,-220), (30,-210), (38,-195), (45,-180), (43,-160), (40,-140), (30,-120), (20,-100), (10,-90), (0,-80), (-10,-60), (-20,-40), (-13,-27), (-7,-13), (0,0)],
    [(200,40), (190,20), (180,0), (160,-10), (140,-20), (120,-25), (100,-30), (80,-25), (60,-20), (45,-15), (30,-10), (15,-5), (0,0)],
    [(135,210), (135,195), (135,180), (123,160), (110,140), (90,145), (70,150), (50,140), (30,130), (15,115), (0,100), (-8,80), (-15,60), (-23,45), (-30,30), (-20,20), (-10,10), (0,0)],
    [(-50, 265), (-70, 240), (-90, 210), (-110, 180), (-130, 150), (-150, 120), (-120, 90), (-90, 60), (-60, 30), (-30, 15), (0, 0)],
    [(110, -370), (90, -350), (70, -330), (50, -300), (30, -270), (10, -240), (-10, -210), (-30, -180), (-50, -150), (-40, -120), (-30, -90), (-20, -60), (-10, -30), (0, 0)],   
    [(-100, -265), (-80, -240), (-60, -215), (-40, -190), (-20, -165), (0, -140), (20, -115), (10, -90), (0, -65), (-10, -40), (-5, -20), (0, 0)],
    [(200, 40), (180, 30), (160, 20), (140, 10), (120, 0), (100, -10), (80, -5), (60, 0), (40, 5), (20, 10), (10, 5), (0, 0)],
    [(135, 210), (120, 190), (105, 170), (90, 150), (75, 130), (60, 110), (45, 90), (30, 70), (15, 50), (10, 30), (5, 15), (0, 0)],
    [(-50, 265), (-30, 240), (-10, 215), (10, 190), (30, 165), (50, 140), (40, 115), (30, 90), (20, 65), (10, 40), (5, 20), (0, 0)],
    [(110, -370), (100, -340), (90, -310), (80, -280), (70, -250), (60, -220), (80, -190), (100, -160), (90, -130), (80, -100), (70, -70), (60, -40), (30, -20), (0, 0)],
    [(-350, 50), (-320, 70), (-290, 90), (-260, 110), (-230, 130), (-200, 150), (-170, 130), (-140, 110), (-110, 90), (-80, 70), (-50, 50), (-25, 30), (0, 0)],
    [(-230, 290), (-200, 280), (-170, 270), (-140, 260), (-110, 250), (-80, 240), (-50, 220), (-20, 200), (10, 180), (40, 160), (50, 130), (40, 100), (30, 70), (20, 40), (10, 20), (0, 0)],
    [(-100, -265), (-80, -240), (-60, -215), (-40, -190), (-20, -165), (0, -140), (20, -115), (40, -90), (60, -65), (80, -40), (70, -20), (50, -10), (25, -5), (0, 0)],
    [(200, 40), (180, 60), (160, 80), (140, 100), (120, 120), (100, 140), (80, 120), (60, 100), (40, 80), (20, 60), (10, 40), (5, 20), (0, 0)],
    [(135, 210), (110, 200), (85, 190), (60, 180), (35, 170), (10, 160), (-15, 150), (-40, 140), (-20, 120), (0, 100), (20, 80), (40, 60), (30, 40), (20, 20), (10, 10), (0, 0)]
]

def promis_execution(generated_logic:str, bomb_location:tuple, operator_location:tuple=(0.0,0.0), city_attr:Union[Literal["darmstadt","berlin","frankfurt"], tuple] = "darmstadt", load_uam=True):
    """
    args:
        generated_logic: from langda
        bomb_location: 
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
    if city_attr == "darmstadt":
        origin = PolarLocation(latitude=49.878091, longitude=8.654052) # Darmstadt
    elif city_attr == "frankfurt":
        origin = PolarLocation(latitude=50.110924, longitude=8.682127) # Frankfurt
    elif city_attr == "berlin":
        origin = PolarLocation(latitude=52.5186, longitude=13.4081) # Berlin
    elif isinstance(city_attr, tuple):
        origin = PolarLocation(latitude=city_attr[0], longitude=city_attr[1])

    width, height = 1000.0, 1000.0
    number_of_random_maps = 20

    support = CartesianRasterBand(origin, (26, 26), width, height)  # This is the set of points that will be directly computed through sampling (expensive)
    target = CartesianRasterBand(origin, (161, 161), width, height)  # This is the set of points that will be interpolated from the support set (cheap)

    if not load_uam:
        print("Building Uncertainty Annotated Map (UAM)...")
        # Setting up the Uncertainty Annotated Map from OpenStreetMap data
        uam = OsmLoader(origin, (width, height), feature_description).to_cartesian_map()
        uam.features.append(CartesianLocation(operator_location[0], operator_location[1], location_type="operator"))  # We can manually add additional features
        uam.features.append(CartesianLocation(bomb_location[0], bomb_location[1], location_type="bomb"))  # We can manually add additional features
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

    set_path(operator_location[0], operator_location[1], save_dir)


def get_confidence_at_point(landscape, east: float, north: float) -> float:

    # 找到最接近的网格点
    distances = np.sqrt((landscape.data.east - east)**2 + 
                        (landscape.data.north - north)**2)
    closest_idx = distances.idxmin()
    return landscape.data.loc[closest_idx, 'v0']

def set_path(x_pt, y_pt, save_dir):
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
    labels = ["0", "0.5", "1"]
    
    plt.xlabel("Easting / km")
    plt.ylabel("Northing / km")
    plt.xticks(ticks, labels)
    plt.yticks(ticks, labels)
    plt.xlim([-500, 500])
    plt.ylim([-500, 500])
    plt.title("P(mission_landscape)")

    for i, path in enumerate(path_lists):
        confidence_list = []
        valid = True
        for (x,y) in path:
            confidence = np.around(get_confidence_at_point(landscape, x, y),3)
            if confidence < 0.4:
                confidence_list.append(f"Invalid")
                valid = False
            else:
                confidence_list.append(confidence)
        plt.plot(*zip(*path), 
                marker='.',
                markersize=5,
                linewidth=1.5,
                alpha=0.8,
                label=f'Path{i}')
        
        print(f"Path{i}: {valid}",confidence_list)
    
    plt.legend()
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

    plt.savefig(
        f"{save_dir}/mission_landscape.png", 
        dpi=100,
        format='png',
        bbox_inches='tight',
        transparent=False)
    plt.close()
    print(f"Landscape plot saved to mission_landscape.png")
