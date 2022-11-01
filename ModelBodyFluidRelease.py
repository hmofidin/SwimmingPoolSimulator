import numpy as np


class ModelBodyFluidRelease:
    def __init__(self):
        self.sweat_release_parameters = {
            'a': 0.18,
            'b': 0.0146,
            'beta1': 0.3882,
            'beta2': 11.1848,
            'T0': 29,
            'A0': 0.71,
            'TimeBase': 3600
        }
        print('initiated')

    def calculate_normalized_sweat_release(self, activity_level, water_temperature, time_period_seconds):
        """
        This function estimates sweat release of swimmers based on activity level and water temperature for a period of
        time
        :param activity_level: activity level of swimmers as a %VO2_max, between 0 and 100
        :param water_temperature: water temperature in Celsius
        :param time_period_seconds: time period of swimming
        :return:
        """
        a = self.sweat_release_parameters['a']
        b = self.sweat_release_parameters['b']
        beta1 = self.sweat_release_parameters['beta1']
        beta2 = self.sweat_release_parameters['beta2']
        T0 = self.sweat_release_parameters['T0']
        A0 = self.sweat_release_parameters['A0']
        TimeBase = self.sweat_release_parameters['TimeBase']

        A = activity_level / 100
        T = water_temperature

        return (a + b * np.exp(beta1 * (T - T0) + beta2 * (A / 100 - A0))) * (time_period_seconds / TimeBase)

    def simulate_body_fluid_release(self, datetime_stamps, occupancy_data, swimming_pool_water_temperature_celsius):
        """
        This function estimates the total volume of sweat release for the swimmers based on occupancy data
        :param datetime_stamps: date-time stamps of calculating sweat release
        :param occupancy_data: occupancy data
        :param swimming_pool_water_temperature_celsius: water temperature of swimming pool in celsius
        :return: estimated volume of body fluid release
        """
        total_volume_of_body_fluid_release_date_times = []

        if len(datetime_stamps) < 2:
            return total_volume_of_body_fluid_release_date_times

        time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds

        # Normalize Swear: L / h / m^2
        for dt_stamp in datetime_stamps:
            total_volume_of_body_fluid_release_date_time = 0
            for swimmer in occupancy_data:
                if swimmer['DT-Arrival'] < dt_stamp < swimmer['DT-Leave']:
                    seconds_from_arrival = (dt_stamp - swimmer['DT-Arrival']).seconds
                    percentage_presence_in_cycle = min(1, seconds_from_arrival / time_period_seconds)
                    cycles_from_arrival = int(seconds_from_arrival / time_period_seconds)
                    if len(swimmer['Act-Levels']) > cycles_from_arrival:
                        activity_level = swimmer['Act-Levels'][cycles_from_arrival]

                        normalized_sweat_release = \
                            self.calculate_normalized_sweat_release(activity_level,
                                                                    swimming_pool_water_temperature_celsius,
                                                                    percentage_presence_in_cycle * time_period_seconds)

                        body_surface_area = np.sqrt(swimmer['Weight'] * (swimmer['Height'] / 100.0)) / 6
                        total_volume_of_body_fluid_release_date_time += body_surface_area * normalized_sweat_release

            total_volume_of_body_fluid_release_date_times.append(total_volume_of_body_fluid_release_date_time)

        return total_volume_of_body_fluid_release_date_times

