import datetime
import numpy as np

class ModelWaterManagement:

    def __init__(self, min_volume_of_water, max_volume_of_water):
        """

        """
        self.max_volume_of_water = max_volume_of_water
        self.min_volume_of_water = min_volume_of_water
        self.gamma_L = 5
        self.gamma_M = 10
        self.gamma_H = 20
        self.time_base_seconds = 60 * 30

    def set_parameters(self, gamma_l, gamma_m, gamma_h):
        """

        :param gamma_l:
        :param gamma_m:
        :param gamma_h:
        :return:
        """

        self.gamma_L = gamma_l
        self.gamma_M = gamma_m
        self.gamma_H = gamma_h

    def generate_fix_rate_water_flow(self, datetime_stamps, fix_in_water_rate, fix_out_water_rate,
                                     water_evaporation, swimming_pool_volume_of_water):
        """

        :param datetime_stamps:

        :param fix_in_water_rate:
        :param fix_out_water_rate:
        :param swimming_pool_volume_of_water:
        :param water_evaporation:
        :return:
        """

        time_step_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
        VoW = swimming_pool_volume_of_water

        water_in = []
        water_out = []

        for dts, E in zip(datetime_stamps, water_evaporation):
            out_water = fix_out_water_rate * time_step_seconds / self.time_base_seconds - E
            in_water = fix_in_water_rate * time_step_seconds / self.time_base_seconds
            VoW += in_water - out_water - E
            if VoW > self.max_volume_of_water:
                out_water += VoW - self.max_volume_of_water
            elif VoW < self.min_volume_of_water:
                in_water += self.min_volume_of_water - VoW
            water_in.append(in_water)
            water_out.append(out_water)

        return water_in, water_out

    def generate_occupancy_based_rate_water_flow(self, datetime_stamps, occupancy_data, water_evaporation,
                                                 swimming_pool_volume_of_water):
        """

        :param datetime_stamps:
        :param occupancy_data:
        :param water_evaporation:
        :param swimming_pool_volume_of_water:
        :return:
        """

        time_step_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
        VoW = swimming_pool_volume_of_water

        alpha_L = self.gamma_L * time_step_seconds / self.time_base_seconds
        alpha_M = self.gamma_M * time_step_seconds / self.time_base_seconds
        alpha_H = self.gamma_H * time_step_seconds / self.time_base_seconds

        water_in = [0]
        water_out = [0]

        water_to_add = np.zeros((len(datetime_stamps)))

        for oc_d in occupancy_data:
            dt_st_ind = int(((oc_d['DT-Arrival'] - datetime_stamps[0]).total_seconds()) / time_step_seconds)
            dt_ed_ind = int(((oc_d['DT-Leave'] - datetime_stamps[0]).total_seconds()) / time_step_seconds)
            for m, n in enumerate(np.arange(start=dt_st_ind, stop=dt_ed_ind, step=1)):
                if len(oc_d['Act-Levels']) <= m:
                    break
                activity_level = oc_d['Act-Levels'][m] / 100
                if activity_level < 0.4:
                    water_to_add[n] += alpha_L
                elif activity_level < 0.7:
                    water_to_add[n] += alpha_M
                else:
                    water_to_add[n] += alpha_H

        for dts, E, in_water in zip(datetime_stamps, water_evaporation, water_to_add):
            '''in_water = 0
            for oc_d in occupancy_data:
                if oc_d['DT-Arrival'] < dts + datetime.timedelta(seconds=time_step_seconds) and oc_d['DT-Leave'] > dts:
                    seconds_from_arrival = (dts - oc_d['DT-Arrival']).seconds
                    percentage_presence_in_cycle = min(1, seconds_from_arrival / time_step_seconds)
                    cycles_from_arrival = int(seconds_from_arrival / time_step_seconds)
                    if len(oc_d['Act-Levels']) > cycles_from_arrival:
                        activity_level = oc_d['Act-Levels'][cycles_from_arrival] / 100
                        if activity_level < 0.45:
                            in_water += alpha_L
                        elif activity_level < 0.7:
                            in_water += alpha_M
                        else:
                            in_water += alpha_H'''

            out_water = in_water - E

            if VoW > self.max_volume_of_water:
                out_water += VoW - self.max_volume_of_water
            elif VoW < self.min_volume_of_water:
                in_water += self.min_volume_of_water - VoW

            VoW += in_water - out_water - E

            water_in.append(in_water)
            water_out.append(out_water)

        return water_in, water_out

    def generate_water_flow_based_on_bather_load_based(self, datetime_stamps, occupancy_data, water_evaporation,
                                                       swimming_pool_volume_of_water, daily_frequency=3,
                                                       liters_per_bather=15):
        """
        :param datetime_stamps:
        :param occupancy_data:
        :param water_evaporation:
        :param swimming_pool_volume_of_water:
        :param daily_frequency:
        :param liters_per_bather:
        :return:
        """
        time_step_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
        dates = []
        for dt in datetime_stamps:
            date_ = dt.date()
            if date_ not in dates:
                dates.append(date_)

        hrs = np.linspace(11, 23, num=daily_frequency)
        water_injection_date_times = []
        for d in dates:
            for h in hrs:
                dt = datetime.datetime(d.year, d.month, d.day, int(h), 0, 0)
                water_injection_date_times.append({'dt': dt, 'Applied': False})

        occupancy_of_injection_periods = np.zeros((len(water_injection_date_times)))

        for oc_d in occupancy_data:
            ind_hr = 0
            for n, hr in enumerate(hrs):
                if oc_d['DT-Leave'].hour < hr:
                    ind_hr = n
                    break
            diff_days = (oc_d['DT-Leave'].date() - datetime_stamps[1].date()).days
            ind = diff_days * len(hrs) + ind_hr
            occupancy_of_injection_periods[ind] += 1
            #if oc_d['DT-Leave'] < dts + datetime.timedelta(seconds=time_step_seconds) and oc_d['DT-Leave'] > dts:
            #    cumulative_volume_of_water += liters_per_bather

        max_water_rate_to_inject_liter_per_second = 1

        VoW = swimming_pool_volume_of_water

        water_in = [0]
        water_out = [0]

        cumulative_volume_of_water_to_add = 0
        cumulative_volume_of_water = 0
        for dts, E in zip(datetime_stamps, water_evaporation):
            for item, occ in zip(water_injection_date_times, occupancy_of_injection_periods):
                if not item['Applied']:
                    if item['dt'] < dts:
                        cumulative_volume_of_water_to_add = occ * liters_per_bather
                        item['Applied'] = True
                    else:
                        break

            out_water = 0
            in_water = 0

            if cumulative_volume_of_water_to_add > 0:
                delta = time_step_seconds * max_water_rate_to_inject_liter_per_second
                cumulative_volume_of_water_to_add_new = max(0, cumulative_volume_of_water_to_add - delta)
                in_water = cumulative_volume_of_water_to_add - cumulative_volume_of_water_to_add_new
                cumulative_volume_of_water_to_add = cumulative_volume_of_water_to_add_new

            out_water = in_water

            if VoW > self.max_volume_of_water:
                out_water += VoW - self.max_volume_of_water
            elif VoW < self.min_volume_of_water:
                in_water += self.min_volume_of_water - VoW

            VoW += in_water - out_water - E

            water_in.append(in_water)
            water_out.append(out_water)

        return water_in, water_out

