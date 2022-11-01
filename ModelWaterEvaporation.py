import numpy as np


class ModelWaterEvaporation:
    def __init__(self):
        """
        This class models water evaporation in swimming pools based on occupancy data
        :param json_file_path: the path of json file containing parameters of water evaporation
        """
        self.convert_water_kg_to_liter = 1
        self.evaporation_unoccupied = [{"water_temp": 28, "air_temp": 28, "relative_humidity": 0.5, "E0": 0.1360, "delta_roe": 0.0219},
                                       {"water_temp": 28, "air_temp": 29, "relative_humidity": 0.5, "E0": 0.1171, "delta_roe": 0.0168},
                                       {"water_temp": 28, "air_temp": 30, "relative_humidity": 0.5, "E0": 0.0968, "delta_roe": 0.0116},
                                       {"water_temp": 29, "air_temp": 28, "relative_humidity": 0.5, "E0": 0.1651, "delta_roe": 0.0282},
                                       {"water_temp": 29, "air_temp": 29, "relative_humidity": 0.5, "E0": 0.1463, "delta_roe": 0.0231},
                                       {"water_temp": 29, "air_temp": 30, "relative_humidity": 0.5, "E0": 0.1268, "delta_roe": 0.0180},
                                       {"water_temp": 30, "air_temp": 28, "relative_humidity": 0.5, "E0": 0.1959, "delta_roe": 0.0347},
                                       {"water_temp": 30, "air_temp": 29, "relative_humidity": 0.5, "E0": 0.1771, "delta_roe": 0.0295},
                                       {"water_temp": 30, "air_temp": 30, "relative_humidity": 0.5, "E0": 0.1575, "delta_roe": 0.0244}]

    def process_water_evaporation(self, datetime_stamps, bather_load, swimming_pool_surface_area, water_temperature,
                                  room_temperature, room_humidity):

        time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds

        E0 = 0
        delta_roe = 0
        for r in self.evaporation_unoccupied:
            if np.absolute(r["water_temp"] - water_temperature) < 0.5 \
                    and np.absolute(r["air_temp"] - room_temperature) < 0.5 \
                    and np.absolute(r["relative_humidity"] - room_humidity) < 0.1:
                E0 = r["E0"]
                delta_roe = r["delta_roe"]
                break
        evaporations = []
        for dt_stamp, num_bathers in zip(datetime_stamps, bather_load):
            N_star = num_bathers / swimming_pool_surface_area
            evaporation = E0
            if N_star > 0.05:
                evaporation = E0 * (1.9 - 21 * delta_roe + 5.3 * N_star)
            evaporations.append(self.convert_water_kg_to_liter * swimming_pool_surface_area * evaporation *
                                time_period_seconds / 3600)
        return evaporations
