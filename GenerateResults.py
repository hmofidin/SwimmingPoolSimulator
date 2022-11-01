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
utils.validate_date_time_string(start_date_time)
utils.validate_date_time_string(end_date_time)
dt_start = datetime.datetime.strptime(start_date_time, '%Y/%m/%d %H:%M:%S')
dt_end = datetime.datetime.strptime(end_date_time, '%Y/%m/%d %H:%M:%S')
datetime_stamps_gen = utils.dates_bwn_two_date_times_generator(dt_start, dt_end, time_step_seconds)
datetime_stamps = []
TCM_th = 100
for n, dt in enumerate(datetime_stamps_gen):
    datetime_stamps.append(dt)

with open("run_Chemicals_Lambda1_0.json", "r") as f_chem:
    chemical_parameters = json.load(f_chem)
with open("run_Occupancy_Lambda1_0.json", "r") as f_occ:
    occupancy_data = json.load(f_occ)
bather_loads, dates = utils.get_daily_bather_load(datetime_stamps, occupancy_data)
daily_water_use, daily_evaporation, daily_wastewater_drain = utils.get_daily_water_treatment(datetime_stamps,
                                                                                             chemical_parameters)

daily_TCM, daily_TOC_added, daily_TCM_above_th, max_TCM = utils.get_daily_water_health_quality(datetime_stamps,
                                                                                               chemical_parameters,
                                                                                               TCM_th)

utils.plot_bather_load_and_water_use_twin_chart(dates, bather_loads, daily_water_use)

utils.plot_generated_toc_and_tcm_twin_chart(dates, daily_TOC_added, daily_TCM)

print('number of days with TCM above threshold: {}, maximum TCM:{}'.format(sum(daily_TCM_above_th), max_TCM))
print('Total Water Use: {}'.format(np.sum(np.array(daily_water_use))))
print(bather_loads)

