import datetime
from typing import Any

import utils
import ModelOccupancyParameters
import ModelChemicalParameters
import ModelWaterManagement
import ModelBodyFluidRelease
import ModelWaterEvaporation
import numpy as np
import json
from django.core.serializers.json import DjangoJSONEncoder


def simulate_occupancy_between_two_date_times(start_date_time, end_date_time, time_step_seconds=300):
    """
    This function provides occupancy model between two dates
    :param time_step_seconds: time difference between each consecutive time-sample (default: 300 seconds)
    :param start_date_time: start date-time of occupancy simulation (format: YYYY-MM-DD hh:mm:ss)
    :param end_date_time: end date-time of occupancy simulation (format: YYYY-MM-DD hh:mm:ss)
    :return: returns a json file of occupancy between the specified date-times as an array of objects which each object
    presents one single occupant with its weight, height, age, gender, and activity level data throughout the staying
    time.
    """

    model = ModelOccupancyParameters.ModelOccupancyParameters()

    utils.validate_date_time_string(start_date_time)

    utils.validate_date_time_string(end_date_time)

    dt_start = datetime.datetime.strptime(start_date_time, '%Y/%m/%d %H:%M:%S')

    dt_end = datetime.datetime.strptime(end_date_time, '%Y/%m/%d %H:%M:%S')

    dts = utils.dates_bwn_two_date_times_generator(dt_start, dt_end, time_step_seconds)
    occupancy_data = []
    datetime_stamps = []
    for n, dt in enumerate(dts):
        dt_ = dt
        datetime_stamps.append(dt)
        s = 0
        while True:

            time_to_arrival, gender, age, weight, height, time_of_stay_seconds, als = \
                model.get_a_swimmer_from_model(dt_, time_step_seconds)

            s += time_to_arrival
            if s < time_step_seconds:
                datetime_arrival = dt + datetime.timedelta(seconds=s)
                datetime_leave = dt + datetime.timedelta(seconds=s + time_of_stay_seconds)
                dt_ = datetime_arrival
                occupancy_data.append({'DT-Arrival': datetime_arrival, 'Gender': gender, 'Age': age, 'Weight': weight,
                                       'Height': height, 'DT-Leave': datetime_leave, 'Act-Levels': als})
            else:
                break
    return datetime_stamps, occupancy_data


def generate_set_of_parameters(min_l, min_m, min_h, max_l, max_m, max_h, step_l=4, step_m=10, step_h=10):
    """

    :param min_l:
    :param min_m:
    :param min_h:
    :param max_l:
    :param max_m:
    :param max_h:
    :param step_l:
    :param step_m:
    :param step_h:
    :return:
    """
    set_parameters: list[dict[str, Any]] = []
    for l_ in np.arange(start=min_l, stop=max_l, step=step_l):
        for m_ in np.arange(start=min_m, stop=max_m, step=step_m):
            for h_ in np.arange(start=min_h, stop=max_h, step=step_h):
                if l_ < m_ < h_:
                    set_parameters.append({'gamma_L': l_, 'gamma_M': m_, 'gamma_H': h_})

    return set_parameters


def cost_function(water_ins, bather_load, chemical_parameters, tcm_threshold, lambda_water_quality=1000000,
                  time_step_seconds=360):
    """

    :param water_ins:
    :param chemical_parameters:
    :param tcm_threshold:
    :param lambda_water_quality:
    :return:
    """
    cost_water_use = 0
    cost_water_quality = 0

    liter_2_m3 = 0.001

    for water_in in water_ins:
        cost_water_use += water_in

    # Cost of water use in cubic meters instead of liters
    cost_water_use = liter_2_m3 * cost_water_use

    time_adj = 60 * 60 / time_step_seconds

    for chem_param, bl in zip(chemical_parameters, bather_load):
        tcm = chem_param['TCM']
        if tcm > tcm_threshold:
            cost_water_quality += bl * (tcm-tcm_threshold)/tcm_threshold

    return cost_water_use + lambda_water_quality * (cost_water_quality / time_adj), cost_water_use, cost_water_quality


def main():
    # start_date_time: Start date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    start_date_time = "2022/03/01 00:00:00"
    # end_date_time: End date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    end_date_time = "2022/10/31 23:55:00"
    # time_step_seconds: period of time-stamps in seconds
    time_step_seconds = 360
    # swimming_pool_water_temperature_celsius: operational water temperature of the swimming pool
    swimming_pool_water_temperature_celsius = 28
    natatorium_room_temperature_celsius = 30
    natatorium_room_relative_humidity = 0.5
    # swimming_pool_volume_of_water: volume of water in the swimming pool (liter)
    swimming_pool_volume_of_water = 200 * 1000
    max_swimming_pool_volume_of_water = 250 * 1000
    min_swimming_pool_volume_of_water = 150 * 1000
    swimming_pool_surface_area = 150
    # initial_chemical_parameters: initial chemical parameters of the swimming pool at the start datetime
    initial_chemical_parameters = {"FAC": 1, "TCM": 0, "CC": 0, "pH": 7.8, "ORP": 700, "BF": 0}

    # Simulate occupancy of swimming pool between start and end date-times
    datetime_stamps, occupancy_data = simulate_occupancy_between_two_date_times(start_date_time, end_date_time,
                                                                                time_step_seconds)

    # Simulate body fluid release based on occupancy data and water temperature
    model_bfa_release = ModelBodyFluidRelease.ModelBodyFluidRelease()
    body_fluid_release = model_bfa_release.simulate_body_fluid_release(datetime_stamps, occupancy_data,
                                                                       swimming_pool_water_temperature_celsius)
    # Calculate bather load
    bather_load = utils.get_bather_load_for_datetime_stamps(datetime_stamps, occupancy_data, time_step_seconds)

    model_water_evaporation = ModelWaterEvaporation.ModelWaterEvaporation()
    water_evaporation = model_water_evaporation.process_water_evaporation(datetime_stamps, bather_load,
                                                                          swimming_pool_surface_area,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          natatorium_room_temperature_celsius,
                                                                          natatorium_room_relative_humidity)

    # Plot graph of occupancy and sweat release in a single graph (shared y-axis)
    #utils.plot_bather_load_and_body_fluid_release_in_one_chart(datetime_stamps, bather_load, body_fluid_release)

    # Adding freshwater at the fix rate of 150 liters per hour
    fix_in_water_rate = 500
    # Draining wastewater at the fix rate of 150 liters per hour
    fix_out_water_rate = 500

    model_wm = ModelWaterManagement.ModelWaterManagement(min_swimming_pool_volume_of_water,
                                                         max_swimming_pool_volume_of_water)

    #WaterManagamentMethods = ["Fixed", "Occupancy"]
    model_wm.set_parameters(gamma_l=9, gamma_m=49, gamma_h=100)

    # Generate water management input and output flows of water
    WMM = "Occupancy"
    if WMM == "Fixed":
        wf_in, wf_out = model_wm.generate_fix_rate_water_flow(datetime_stamps,
                                                              fix_in_water_rate,
                                                              fix_out_water_rate,
                                                              water_evaporation,
                                                              swimming_pool_volume_of_water)

    elif WMM == "Occupancy":
        wf_in, wf_out = model_wm.generate_occupancy_based_rate_water_flow(datetime_stamps,
                                                                          occupancy_data,
                                                                          water_evaporation,
                                                                          swimming_pool_volume_of_water)

    # Model chemical parameters and content
    model_chemicals = ModelChemicalParameters.ModelChemicalParameters()
    chemical_parameters = model_chemicals.process_chemical_parameters(initial_chemical_parameters, datetime_stamps,
                                                                      body_fluid_release,
                                                                      swimming_pool_water_temperature_celsius,
                                                                      swimming_pool_volume_of_water,
                                                                      water_evaporation, wf_in, wf_out)

    # Plot graph of occupancy and TCM concentration in a single graph (shared y-axis)
    #utils.plot_bather_load_and_tcm_concentration_in_one_chart(datetime_stamps, bather_load, chemical_parameters)

    # Plot graph of water use, drain, evaporation, and volume in liters
    #utils.plot_water_in_one_chart(datetime_stamps, water_evaporation, wf_in, wf_out, chemical_parameters)

    utils.plot_toc_generated_and_tcm_concentration_in_one_chart(datetime_stamps, chemical_parameters)

    utils.plot_toc_and_tcm_concentration_in_one_chart(datetime_stamps, chemical_parameters)

    with open("run_Chemicals.json", "w") as i:
        json_string = json.dumps(chemical_parameters)
        i.write(json_string)
        i.write(",\n")

    with open("run_Occupancy.json", "w") as i:
        json_string = json.dumps(occupancy_data, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        i.write(json_string)
        i.write(",\n")

    #utils.plot_tcm_concentration(datetime_stamps, chemical_parameters)

    #utils.plot_toc_concentration(datetime_stamps, chemical_parameters)

    print('Total Water Used:{}'.format(sum(wf_in)))
    print('TCM Level:{}'.format(chemical_parameters[-1]["TCM"]))
    print('VoW:{}'.format(chemical_parameters[-1]["VoW"]))
    print('TOC:{}'.format(chemical_parameters[-1]["toc"]))

    print('bather load:{}'.format(len(occupancy_data)))


def train():
    # start_date_time: Start date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    start_date_time = "2022/01/01 00:00:00"
    # end_date_time: End date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    end_date_time = "2022/12/31 23:55:00"
    # time_step_seconds: period of time-stamps in seconds
    time_step_seconds = 360
    # swimming_pool_water_temperature_celsius: operational water temperature of the swimming pool
    swimming_pool_water_temperature_celsius = 30
    natatorium_room_temperature_celsius = 32
    natatorium_room_relative_humidity = 0.5
    # swimming_pool_volume_of_water: volume of water in the swimming pool (liter)
    swimming_pool_volume_of_water = 200 * 1000
    max_swimming_pool_volume_of_water = 250 * 1000
    min_swimming_pool_volume_of_water = 150 * 1000
    swimming_pool_surface_area = 150
    # initial_chemical_parameters: initial chemical parameters of the swimming pool at the start datetime
    initial_chemical_parameters = {"FAC": 1, "TCM": 0.0, "CC": 0, "pH": 7.8, "ORP": 700, "BF": 0}
    # Optimization parameters
    tcm_threshold = 100.0
    lambda_water_quality = 1

    min_l = 2
    max_l = 22

    min_m = 20
    max_m = 82

    min_h = 40
    max_h = 182

    # Generate set of parameters
    set_parameters = generate_set_of_parameters(min_l, min_m, min_h, max_l, max_m, max_h, step_l=2, step_m=2, step_h=2)

    # Simulate occupancy of swimming pool between start and end date-times
    datetime_stamps, occupancy_data = simulate_occupancy_between_two_date_times(start_date_time, end_date_time,
                                                                                time_step_seconds)

    # Simulate body fluid release based on occupancy data and water temperature
    model_bfa_release = ModelBodyFluidRelease.ModelBodyFluidRelease()
    body_fluid_release = model_bfa_release.simulate_body_fluid_release(datetime_stamps, occupancy_data,
                                                                       swimming_pool_water_temperature_celsius)

    # Calculate bather load
    bather_load = utils.get_bather_load_for_datetime_stamps(datetime_stamps, occupancy_data, time_step_seconds)

    # Model water evaporation
    model_water_evaporation = ModelWaterEvaporation.ModelWaterEvaporation()
    water_evaporation = model_water_evaporation.process_water_evaporation(datetime_stamps, bather_load,
                                                                          swimming_pool_surface_area,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          natatorium_room_temperature_celsius,
                                                                          natatorium_room_relative_humidity)

    # Model water management
    model_wm = ModelWaterManagement.ModelWaterManagement(min_swimming_pool_volume_of_water,
                                                         max_swimming_pool_volume_of_water)

    min_cost = 20000
    selected_params = {}
    cost_parameters = []

    for parameters in set_parameters:
        model_wm.set_parameters(gamma_l=parameters['gamma_L'], gamma_m=parameters['gamma_M'],
                                gamma_h=parameters['gamma_H'])

        # Generate water management input and output flows of water
        wf_in, wf_out = model_wm.generate_occupancy_based_rate_water_flow(datetime_stamps,
                                                                          occupancy_data,
                                                                          water_evaporation,
                                                                          swimming_pool_volume_of_water)

        # Model chemical parameters and content
        model_chemicals = ModelChemicalParameters.ModelChemicalParameters()
        chemical_parameters = model_chemicals.process_chemical_parameters(initial_chemical_parameters, datetime_stamps,
                                                                          body_fluid_release,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          swimming_pool_volume_of_water,
                                                                          water_evaporation, wf_in, wf_out)

        # Calculate cost function terms
        cost, cost_water_use, cost_water_quality = cost_function(wf_in, bather_load, chemical_parameters,
                                                                 tcm_threshold, lambda_water_quality, time_step_seconds)

        new_rec = {'cost': cost, 'gamma_l': float(parameters['gamma_L']), 'gamma_m': float(parameters['gamma_M']),
                   'gamma_h': float(parameters['gamma_H']), 'water use': cost_water_use,
                   'health_cost': float(cost_water_quality), 'contribute': min_cost - cost}

        cost_parameters.append(new_rec)

        print(new_rec)

        if min_cost > cost:
            min_cost = cost
            selected_params = parameters

        with open("data_T30C_20220807.json", "a") as i:
            json_string = json.dumps(new_rec)
            i.write(json_string)
            i.write(",\n")

    print('total cost:{}, parameters:{}'.format(min_cost, selected_params))


def train2():
    # start_date_time: Start date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    start_date_time = "2022/01/01 00:00:00"
    # end_date_time: End date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    end_date_time = "2022/12/31 23:55:00"
    # time_step_seconds: period of time-stamps in seconds
    time_step_seconds = 360
    # swimming_pool_water_temperature_celsius: operational water temperature of the swimming pool
    swimming_pool_water_temperature_celsius = 28
    natatorium_room_temperature_celsius = 30
    natatorium_room_relative_humidity = 0.5
    # swimming_pool_volume_of_water: volume of water in the swimming pool (liter)
    swimming_pool_volume_of_water = 200 * 1000
    max_swimming_pool_volume_of_water = 250 * 1000
    min_swimming_pool_volume_of_water = 150 * 1000
    swimming_pool_surface_area = 150
    # initial_chemical_parameters: initial chemical parameters of the swimming pool at the start datetime
    initial_chemical_parameters = {"FAC": 1, "TCM": 0.0, "CC": 0, "pH": 7.8, "ORP": 700, "BF": 0}
    # Optimization parameters
    tcm_threshold = 100.0
    lambda_water_quality = 1

    params = [4, 20, 160]

    # Simulate occupancy of swimming pool between start and end date-times
    print("Occupancy Modeling!")
    datetime_stamps, occupancy_data = simulate_occupancy_between_two_date_times(start_date_time, end_date_time,
                                                                                time_step_seconds)

    # Simulate body fluid release based on occupancy data and water temperature
    print("Body Fluid Release!")
    model_bfa_release = ModelBodyFluidRelease.ModelBodyFluidRelease()
    body_fluid_release = model_bfa_release.simulate_body_fluid_release(datetime_stamps, occupancy_data,
                                                                       swimming_pool_water_temperature_celsius)

    # Calculate bather load
    print("Bather Load!")
    bather_load = utils.get_bather_load_for_datetime_stamps(datetime_stamps, occupancy_data, time_step_seconds)

    # Model water evaporation
    print("Water Evaporation!")
    model_water_evaporation = ModelWaterEvaporation.ModelWaterEvaporation()
    water_evaporation = model_water_evaporation.process_water_evaporation(datetime_stamps, bather_load,
                                                                          swimming_pool_surface_area,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          natatorium_room_temperature_celsius,
                                                                          natatorium_room_relative_humidity)

    # Model water management
    model_wm = ModelWaterManagement.ModelWaterManagement(min_swimming_pool_volume_of_water,
                                                         max_swimming_pool_volume_of_water)

    min_cost = 922.71
    selected_params = {}
    cost_parameters = []
    print("Start Iterations!")
    while True:

        model_wm.set_parameters(gamma_l=params[0], gamma_m=params[1],
                                gamma_h=params[2])

        # Generate water management input and output flows of water
        wf_in, wf_out = model_wm.generate_occupancy_based_rate_water_flow(datetime_stamps,
                                                                          occupancy_data,
                                                                          water_evaporation,
                                                                          swimming_pool_volume_of_water)

        # Model chemical parameters and content
        model_chemicals = ModelChemicalParameters.ModelChemicalParameters()
        chemical_parameters = model_chemicals.process_chemical_parameters(initial_chemical_parameters, datetime_stamps,
                                                                          body_fluid_release,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          swimming_pool_volume_of_water,
                                                                          water_evaporation, wf_in, wf_out)

        # Calculate cost function terms
        cost, cost_water_use, cost_water_quality = cost_function(wf_in, bather_load, chemical_parameters,
                                                                 tcm_threshold, lambda_water_quality, time_step_seconds)

        new_rec = {'cost': cost, 'gamma_l': float(params[0]), 'gamma_m': float(params[1]),
                   'gamma_h': float(params[2]), 'water use': cost_water_use,
                   'health_cost': float(cost_water_quality), 'contribute': min_cost - cost}

        cost_parameters.append(new_rec)

        print(new_rec)

        if min_cost > cost:
            min_cost = cost
            selected_params = params

        with open("data.json", "a") as i:
            json_string = json.dumps(new_rec)
            i.write(json_string)
            i.write(",\n")

        # Prepare for next step
        if cost_water_quality > 0:
            if params[2] < 180:
                params[2] += 2
            else:
                if params[1] < params[2] - 5 and params[1] < 70:
                    params[1] += 2
                else:
                    params[0] += 2
        else:
            if params[1] < params[2] - 5 and params[1] < 70:
                params[1] += 2
                params[2] -= 20
            else:
                params[0] += 2
                params[1] -= 10
                params[2] -= 20

        if params[0] > 16 or params[1] < 10 or params[2] < 10:
            break

        print('Next step: gamma_l={}, gamma_m={}, gamma_h={}'.format(params[0], params[1], params[2]))

    print('total cost:{}, parameters:{}'.format(min_cost, selected_params))


def validation():
    # start_date_time: Start date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    start_date_time = "2022/06/01 00:00:00"
    # end_date_time: End date-time of simulation, format: YYYY/MM/DD HH:mm:ss
    end_date_time = "2022/06/07 23:55:00"
    # time_step_seconds: period of time-stamps in seconds
    time_step_seconds = 360
    time_basis = 60 * 30
    # swimming_pool_water_temperature_celsius: operational water temperature of the swimming pool
    swimming_pool_water_temperature_celsius = 28
    natatorium_room_temperature_celsius = 29
    natatorium_room_relative_humidity = 0.5
    # swimming_pool_volume_of_water: volume of water in the swimming pool (liter)
    swimming_pool_volume_of_water = 200 * 1000
    max_swimming_pool_volume_of_water = 250 * 1000
    min_swimming_pool_volume_of_water = 150 * 1000
    swimming_pool_surface_area = 150
    # initial_chemical_parameters: initial chemical parameters of the swimming pool at the start datetime
    initial_chemical_parameters = {"FAC": 1, "TCM": 0.035, "CC": 0, "pH": 7.8, "ORP": 700.0, "BF": 0.0019}

    gamma_l = 0.8
    gamma_m = 1.0
    gamma_h = 6.6

    # Simulate occupancy of swimming pool between start and end date-times
    datetime_stamps, occupancy_data = simulate_occupancy_between_two_date_times(start_date_time, end_date_time,
                                                                                time_step_seconds)

    # Simulate body fluid release based on occupancy data and water temperature
    model_bfa_release = ModelBodyFluidRelease.ModelBodyFluidRelease()
    body_fluid_release = model_bfa_release.simulate_body_fluid_release(datetime_stamps, occupancy_data,
                                                                       swimming_pool_water_temperature_celsius)

    # Calculate bather load
    bather_load = utils.get_bather_load_for_datetime_stamps(datetime_stamps, occupancy_data, time_step_seconds)

    # Model water evaporation
    model_water_evaporation = ModelWaterEvaporation.ModelWaterEvaporation()
    water_evaporation = model_water_evaporation.process_water_evaporation(datetime_stamps, bather_load,
                                                                          swimming_pool_surface_area,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          natatorium_room_temperature_celsius,
                                                                          natatorium_room_relative_humidity)

    utils.plot_bather_load_and_body_fluid_release_in_one_chart(datetime_stamps, bather_load, body_fluid_release)


    # Model water management
    model_wm = ModelWaterManagement.ModelWaterManagement(min_swimming_pool_volume_of_water,
                                                         max_swimming_pool_volume_of_water)



    model_wm.set_parameters(gamma_l=gamma_l * time_basis / time_step_seconds,
                            gamma_m=gamma_m * time_basis / time_step_seconds,
                            gamma_h=gamma_h * time_basis / time_step_seconds)

    WaterManagamentMethods = ["Fixed", "Occupancy"]
    fix_in_water_rate = fix_out_water_rate = 50
    for WMM in WaterManagamentMethods:
        if WMM == "Fixed":
            wf_in, wf_out = model_wm.generate_fix_rate_water_flow(datetime_stamps,
                                                                  fix_in_water_rate,
                                                                  fix_out_water_rate,
                                                                  water_evaporation,
                                                                  swimming_pool_volume_of_water)

        elif WMM == "Occupancy":
            wf_in, wf_out = model_wm.generate_occupancy_based_rate_water_flow(datetime_stamps,
                                                                              occupancy_data,
                                                                              water_evaporation,
                                                                              swimming_pool_volume_of_water)

        # Model chemical parameters and content
        model_chemicals = ModelChemicalParameters.ModelChemicalParameters()
        chemical_parameters = model_chemicals.process_chemical_parameters(initial_chemical_parameters, datetime_stamps,
                                                                          body_fluid_release,
                                                                          swimming_pool_water_temperature_celsius,
                                                                          swimming_pool_volume_of_water,
                                                                          water_evaporation, wf_in, wf_out)

        # Plot graph of occupancy and TCM concentration in a single graph (shared y-axis)
        utils.plot_bather_load_and_tcm_concentration_in_one_chart_v2(datetime_stamps, wf_in, bather_load,
                                                                     body_fluid_release, chemical_parameters)

        print('Total Water Used:{}'.format(sum(wf_in)))
        print('TCM Level:{}'.format(chemical_parameters[-1]["TCM"]))
        print('VoW:{}'.format(chemical_parameters[-1]["VoW"]))
        print('TOC:{}'.format(chemical_parameters[-1]["toc"]))


if __name__ == "__main__":
    train()
