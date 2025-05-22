from numpy import eye
import sys
from config import paths
sys.path.append(paths.get_abscase_path("promis_project"))

# from config import paths
# The imports we will need to run Probabilistic Mission Design
from promis_project import StaRMap, ProMis
from promis_project import PolarLocation, CartesianMap, CartesianLocation, CartesianRasterBand, CartesianCollection
from promis_project import OsmLoader
import matplotlib.pyplot as plt


def promis_execution(generated_logic:str):
    # The features we will load from OpenStreetMap
    # The dictionary key will be stored as the respective features location_type
    # The dictionary value will be used to query the relevant geometry via Overpass
    feature_description = {
        "park": "['leisure' = 'park']",
        "primary": "['highway' = 'primary']",
        "secondary": "['highway' = 'secondary']",
        "tertiary": "['highway' = 'tertiary']",
        "service": "['highway' = 'service']",
        "crossing": "['footway' = 'crossing']",
        "bay": "['natural' = 'bay']",
        "rail": "['railway' = 'rail']",
    }

    # Covariance matrices for some of the features
    # Used to draw random translations representing uncertainty for the respective features
    covariance = {
        "primary": 15 * eye(2),
        "secondary": 10 * eye(2),
        "tertiary": 5 * eye(2),
        "service": 2.5 * eye(2),
        "operator": 20 * eye(2),
    }

    city_attr = "berlin"

    # The mission area, points that will be estimated from 25 samples and points that will be interpolated
    # origin = PolarLocation(latitude=49.878091, longitude=8.654052) # Darmstadt
    # origin = PolarLocation(latitude=50.110924, longitude=8.682127) # Frankfurt
    origin = PolarLocation(latitude=52.5186, longitude=13.4081) # Berlin
    # origin = PolarLocation(latitude=36.8167, longitude=118.3000) # LinZi

    width, height = 1000.0, 1000.0
    number_of_random_maps = 25
    support = CartesianRasterBand(origin, (50, 50), width, height)  # This is the set of points that will be directly computed through sampling (expensive)
    target = CartesianRasterBand(origin, (250, 250), width, height)  # This is the set of points that will be interpolated from the support set (cheap)
    # alternative = CartesianCollection(origin, [CartesianLocation(42, 42)])  # Alternatively, arbitrary points can be set for either set

    print("Building Uncertainty Annotated Map (UAM)...")
    #============================# dynamic features #============================#
    # Setting up the Uncertainty Annotated Map from OpenStreetMap data
    uam = OsmLoader(origin, (width, height), feature_description).to_cartesian_map()
    uam.features.append(CartesianLocation(0.0, 0.0, location_type="operator"))  # We can manually add additional features
    uam.features.append(CartesianLocation(100.0, 100.0, location_type="bomb"))  # We can manually add additional features
    uam.apply_covariance(covariance)  # Assigns the covariance matrices defined earlier
    uam.save(paths.get_abscase_path(f"history/uam_{city_attr}.pkl"))  # We can save and load these objects to avoid recomputation
    print(f"UAM saved to uam_{city_attr}.pkl")

    city_attr = "berlin"
    print("Initializing StaRMap...")
    # Setting up the probabilistic spatial relations from the map data
    star_map = StaRMap(target, CartesianMap.load(paths.get_abscase_path(f"history/uam_{city_attr}.pkl")))
    star_map.initialize(support, number_of_random_maps, generated_logic)  # This estimates all spatial relations that are relevant to the given logic
    # star_map.add_support_points(support, number_of_random_maps, ["distance"], ["primary"])  # Alternatively, we can estimate for specific relations
    star_map.save(paths.get_abscase_path(f"history/star_map_{city_attr}.pkl"))

    print("Running ProMis solver...")
    # Solve the mission area with ProMis
    promis = ProMis(StaRMap.load(paths.get_abscase_path(f"history/star_map_{city_attr}.pkl")))
    landscape = promis.solve(support, generated_logic, n_jobs=4, batch_size=1)
    landscape.save(paths.get_abscase_path(f"history/landscape.pkl"))
    print(f"Mission landscape saved to landscape.pkl")

    print("Rendering mission landscape...")
    # ProMis' Collectiopn classes have a scatter method that can be used to render spatial relations or probabilistic mission landscapes
    landscape = CartesianCollection.load(paths.get_abscase_path(f"history/landscape.pkl"))
    image = landscape.scatter(s=0.4, plot_basemap=True, rasterized=True, cmap="coolwarm_r", alpha=0.25)
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
    # plt.show()

    plt.savefig(
        paths.get_abscase_path("history/mission_landscape.png"), 
        dpi=100, 
        format='png',
        bbox_inches='tight',
        transparent=False)
    print(f"✅ Landscape plot saved to history/mission_landscape.png")

    # # We can also retrieve and visualize StaR Map spatial relations in the same way
    # star_map = StaRMap.load(paths.get_abscase_path("history/star_map.pkl"))
    # fig, axes = plt.subplots(1, 4, sharey=True, figsize=(18, 9))

    # axes[0].title.set_text('P(over(X, park))')
    # image = star_map.get("over", "park").parameters.scatter(ax=axes[0], s=0.4, plot_basemap=True, rasterized=True, cmap="coolwarm_r", alpha=0.25)

    # axes[1].title.set_text('$\mu$ of distance(X, primary)')
    # distance_primary = star_map.get("distance", "primary")
    # image = distance_primary.parameters.scatter(ax=axes[1], s=0.4, plot_basemap=True, rasterized=True, cmap="coolwarm_r", alpha=0.25)

    # axes[2].title.set_text('$\sigma$ of distance(X, primary)')
    # image = distance_primary.parameters.scatter(value_index=1, ax=axes[2], s=0.4, plot_basemap=True, rasterized=True, cmap="coolwarm_r", alpha=0.25)

    # axes[3].title.set_text('P(distance(X, primary) > 25m')
    # image = (distance_primary > 25).scatter(ax=axes[3], s=0.4, plot_basemap=True, rasterized=True, cmap="coolwarm_r", alpha=0.25)

    # axes[0].set_ylabel("Northing / km")
    # axes[0].set_yticks(ticks, labels)
    # axes[0].set_ylim([-500, 500])
    # for ax in axes:
    #     ax.set_xlabel("Easting / km")
    #     ax.set_xticks(ticks, labels)
    #     ax.set_xlim([-500, 500])

    # plt.show()
