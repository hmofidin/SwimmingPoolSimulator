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


def simulate_occupancy_between_two_date_times(start_date_time, end_date_time, time_step_seconds=300,
                                              json_file_path='SwimmingPoolOccupancyParameters.json'):
    """
    This function provides occupancy model between two dates
    :param time_step_seconds: time difference between each consecutive time-sample (default: 300 seconds)
    :param start_date_time: start date-time of occupancy simulation (format: YYYY-MM-DD hh:mm:ss)
    :param end_date_time: end date-time of occupancy simulation (format: YYYY-MM-DD hh:mm:ss)
    :param json_file_path:
    :return: returns a json file of occupancy between the specified date-times as an array of objects which each object
    presents one single occupant with its weight, height, age, gender, and activity level data throughout the staying
    time.
    """

    model = ModelOccupancyParameters.ModelOccupancyParameters(json_file_path=json_file_path)

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


def main():
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
    TCM_th = 100 #ug/L
    # initial_chemical_parameters: initial chemical parameters of the swimming pool at the start datetime
    initial_chemical_parameters = {"FAC": 1, "TCM": 0, "CC": 0, "pH": 7.8, "ORP": 700, "BF": 0}

    # ------------------------------------------------------------------------------------------------------------------
    # Load simulated occupancy of swimming pool between start and end date-times from Json file
    # ------------------------------------------------------------------------------------------------------------------
    load_occupancy_data_from_file = True
    occupancy_data_json_file = 'Data_main/OccupancyData.json'
    body_fluid_release_data_json_file = 'Data_main/BodyFluidReleaseData.json'
    water_evaporation_data_json_file = 'Data_main/WaterEvaporationData.json'
    bather_load_data_json_file = 'Data_main/BatherLoadData.json'

    load_occupancy_data_from_file_failed = True
    while load_occupancy_data_from_file:
        try:
            with open(occupancy_data_json_file, "r") as f_occ:
                occupancy_data_json = json.load(f_occ)
                if 'start_date_time' not in occupancy_data_json or \
                        'end_date_time' not in occupancy_data_json or \
                        'time_step_seconds' not in occupancy_data_json or \
                        'Occupancy' not in occupancy_data_json:
                    break
                if occupancy_data_json['start_date_time'] != start_date_time or \
                        occupancy_data_json['end_date_time'] != end_date_time or \
                        occupancy_data_json['time_step_seconds'] != time_step_seconds:
                    break
                datetime_stamps = utils.generate_timestamps_between_two_date_times(start_date_time, end_date_time,
                                                                                   time_step_seconds)
                occupancy_data = occupancy_data_json['Occupancy']
                for item in occupancy_data:
                    item['DT-Arrival'] = datetime.datetime.strptime(item['DT-Arrival'], '%Y-%m-%dT%H:%M:%S')
                    item['DT-Leave'] = datetime.datetime.strptime(item['DT-Leave'], '%Y-%m-%dT%H:%M:%S')
                print('Occupancy data loaded from file!')
                load_occupancy_data_from_file_failed = False
                break
        except:
            print('Not able to find or load occupancy data json file!')
            break

    load_body_fluid_release_data_from_file_failed = True
    water_evaporation_data_from_file_failed = True
    bather_load_data_from_file_failed = True
    if load_occupancy_data_from_file_failed:
        # Simulate occupancy of swimming pool between start and end date-times
        print("Generating simulated occupancy data between {} and {}".format(start_date_time, end_date_time))
        datetime_stamps, occupancy_data = \
            simulate_occupancy_between_two_date_times(start_date_time, end_date_time, time_step_seconds,
                                                      json_file_path='SwimmingPoolOccupancyParameters.json')
    else:
        try:
            with open(body_fluid_release_data_json_file, "r") as f_bfr:
                body_fluid_release = json.load(f_bfr)
            load_body_fluid_release_data_from_file_failed = False
            print('Body fluid release data loaded from file!')
            with open(water_evaporation_data_json_file, "r") as f_we:
                water_evaporation = json.load(f_we)
            print('water evaporation data loaded from file!')
            water_evaporation_data_from_file_failed = False
            with open(bather_load_data_json_file, "r") as f_bl:
                bather_load = json.load(f_bl)
            print('bather load data loaded from file!')
            bather_load_data_from_file_failed = False
        except:
            print('Not able to find or load body fluid release data json file!')

    # ------------------------------------------------------------------------------------------------------------------
    # Simulate body fluid release based on occupancy data and water temperature
    # ------------------------------------------------------------------------------------------------------------------
    if load_body_fluid_release_data_from_file_failed:
        print("Generating body fluid release data")
        model_bfa_release = ModelBodyFluidRelease.ModelBodyFluidRelease()
        body_fluid_release = model_bfa_release.simulate_body_fluid_release(datetime_stamps, occupancy_data,
                                                                           swimming_pool_water_temperature_celsius)

    # ------------------------------------------------------------------------------------------------------------------
    # Calculate bather load
    # ------------------------------------------------------------------------------------------------------------------
    if bather_load_data_from_file_failed:
        print("Calculating bather load")
        bather_load = utils.get_bather_load_for_datetime_stamps(datetime_stamps, occupancy_data, time_step_seconds)

    # ------------------------------------------------------------------------------------------------------------------
    # Calculate water evaporation based on occupancy
    # ------------------------------------------------------------------------------------------------------------------
    if water_evaporation_data_from_file_failed:
        print("Generating water evaporation data")
        model_water_evaporation = ModelWaterEvaporation.ModelWaterEvaporation()
        water_evaporation = model_water_evaporation.process_water_evaporation(datetime_stamps, bather_load,
                                                                              swimming_pool_surface_area,
                                                                              swimming_pool_water_temperature_celsius,
                                                                              natatorium_room_temperature_celsius,
                                                                              natatorium_room_relative_humidity)

    daily_bather_loads, dates = utils.get_daily_bather_load_2(datetime_stamps, occupancy_data)

    # ------------------------------------------------------------------------------------------------------------------
    # Water management
    # ------------------------------------------------------------------------------------------------------------------
    print("Calculating water management!")
    # Adding freshwater at the fix rate of 150 liters per hour
    fix_in_water_rate = 80
    # Draining wastewater at the fix rate of 150 liters per hour
    fix_out_water_rate = 80

    model_wm = ModelWaterManagement.ModelWaterManagement(min_swimming_pool_volume_of_water,
                                                         max_swimming_pool_volume_of_water)

    model_wm.set_parameters(gamma_l=4, gamma_m=20, gamma_h=158)

    # Generate water management input and output flows of water
    #water_managament_methods = ["Fixed Rate Method", "Proposed Method", "Bather Load Method"]
    water_managament_methods = ["Proposed Method"]
    chemical_parameters = {}
    daily_water_use = {}
    daily_evaporation = {}
    daily_wastewater_drain = {}
    daily_TCM = {}
    daily_TOC_added = {}
    daily_TCM_above_th = {}
    max_TCM = {}
    for WMM in water_managament_methods:
        if WMM == "Fixed Rate Method":
            wf_in, wf_out = model_wm.generate_fix_rate_water_flow(datetime_stamps,
                                                                  fix_in_water_rate,
                                                                  fix_out_water_rate,
                                                                  water_evaporation,
                                                                  swimming_pool_volume_of_water)

        elif WMM == "Proposed Method":
            wf_in, wf_out = model_wm.generate_occupancy_based_rate_water_flow(datetime_stamps,
                                                                              occupancy_data,
                                                                              water_evaporation,
                                                                              swimming_pool_volume_of_water)

        elif WMM == "Bather Load Method":
            wf_in, wf_out = model_wm.generate_water_flow_based_on_bather_load_based(datetime_stamps,
                                                                                    occupancy_data,
                                                                                    water_evaporation,
                                                                                    swimming_pool_volume_of_water,
                                                                                    liters_per_bather=15)

        # ------------------------------------------------------------------------------------------------------------------
        # Model chemical parameters and content
        # ------------------------------------------------------------------------------------------------------------------
        print("Calculating chemical parameters and factors!")
        model_chemicals = ModelChemicalParameters.ModelChemicalParameters()
        chemical_parameters[WMM] = model_chemicals.process_chemical_parameters(initial_chemical_parameters,
                                                                               datetime_stamps,
                                                                               body_fluid_release,
                                                                               swimming_pool_water_temperature_celsius,
                                                                               swimming_pool_volume_of_water,
                                                                               water_evaporation,
                                                                               wf_in,
                                                                               wf_out)

        daily_water_use[WMM], daily_evaporation[WMM], daily_wastewater_drain[WMM] = utils.get_daily_water_treatment(
            datetime_stamps, chemical_parameters[WMM])

        daily_TCM[WMM], daily_TOC_added[WMM], daily_TCM_above_th[WMM], max_TCM[WMM] = \
            utils.get_daily_water_health_quality(datetime_stamps, chemical_parameters[WMM], TCM_th)

        #utils.plot_generated_toc_and_tcm_twin_chart(dates, daily_TOC_added[WMM], daily_TCM[WMM])

        bather_loads2, dates2 = utils.get_daily_bather_load2(datetime_stamps, occupancy_data)

        #utils.plot_bather_load_and_water_use_twin_chart(dates2, bather_loads2, daily_water_use[WMM])

        print('\n Water Management Strategy: {} \n'.format(WMM))
        print('Total Water Used:{}'.format(sum(wf_in)))
        print('# of days with TCM above threshold: {}, maximum TCM:{}'.format(sum(daily_TCM_above_th[WMM]), max_TCM[WMM]))
        print('Total Water Use: {}'.format(np.sum(np.array(daily_water_use[WMM]))))

    # ------------------------------------------------------------------------------------------------------------------
    # Store simulated model
    # ------------------------------------------------------------------------------------------------------------------
    with open("run_Chemicals.json", "w") as i:
        json_string = json.dumps(chemical_parameters)
        i.write(json_string)

    with open(occupancy_data_json_file, "w") as i:
        occupancy_data_to_dump = {'start_date_time': start_date_time,
                                  'end_date_time': end_date_time,
                                  'time_step_seconds': time_step_seconds,
                                  'Occupancy': occupancy_data}
        json_string = json.dumps(occupancy_data_to_dump, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        i.write(json_string)

    with open(body_fluid_release_data_json_file, "w") as i:
        json_string = json.dumps(body_fluid_release, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        i.write(json_string)

    with open(water_evaporation_data_json_file, "w") as i:
        json_string = json.dumps(water_evaporation, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        i.write(json_string)

    with open(bather_load_data_json_file, "w") as i:
        json_string = json.dumps(bather_load, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        i.write(json_string)

    # ------------------------------------------------------------------------------------------------------------------
    # Generate Plots/Charts/Results
    # ------------------------------------------------------------------------------------------------------------------
    # utils.plot_tcm_concentration(datetime_stamps, chemical_parameters)
    # utils.plot_toc_concentration(datetime_stamps, chemical_parameters)

    #utils.plot_generated_toc_and_tcm_twin_chart_multiple(dates, daily_TOC_added, daily_TCM)

    print('total bather load:{}'.format(len(occupancy_data)))


if __name__ == "__main__":
    main()
