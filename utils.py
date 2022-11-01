import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib import rc, rcParams


def generate_timestamps_between_two_date_times(start_date_time, end_date_time, time_step_seconds=300):
    """

    :param start_date_time:
    :param end_date_time:
    :param time_step_seconds:
    :return:
    """
    validate_date_time_string(start_date_time)

    validate_date_time_string(end_date_time)

    dt_start = datetime.datetime.strptime(start_date_time, '%Y/%m/%d %H:%M:%S')

    dt_end = datetime.datetime.strptime(end_date_time, '%Y/%m/%d %H:%M:%S')

    dts = dates_bwn_two_date_times_generator(dt_start, dt_end, time_step_seconds)

    datetime_stamps = []
    for n, dt in enumerate(dts):
        datetime_stamps.append(dt)

    return datetime_stamps


def validate_date_time_string(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y/%m/%d %H:%M:%S')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY/MM/DD hh:mm:ss")


def dates_bwn_two_date_times_generator(start_date_time, end_date_time, time_step_seconds):
    for n in range(int((end_date_time - start_date_time).total_seconds() / time_step_seconds)):
        yield start_date_time + datetime.timedelta(seconds=time_step_seconds*n)


def get_bather_load_for_datetime_stamps(datetime_stamps, occupancy_data, time_step_seconds):
    occupancy_array = np.zeros((len(datetime_stamps),))
    for oc_d in occupancy_data:
        for n, dts in enumerate(datetime_stamps):
            if oc_d['DT-Arrival'] < dts + datetime.timedelta(seconds=time_step_seconds) and oc_d['DT-Leave'] > dts:
                occupancy_array[n] += 1
    return list(occupancy_array)


def get_daily_bather_load(datetime_stamps, occupancy_data):
    dates = []
    for dt in datetime_stamps:
        date_ = dt.date()
        if date_ not in dates:
            dates.append(date_)

    occupancy_array = np.zeros((len(dates),))
    for oc_d in occupancy_data:
        date__ = datetime.datetime.strptime(oc_d['DT-Arrival'], '%Y-%m-%dT%H:%M:%S').date()
        ind = dates.index(date__)
        occupancy_array[ind] += 1
    return list(occupancy_array), list(dates)


def get_daily_bather_load2(datetime_stamps, occupancy_data):
    dates = []
    for dt in datetime_stamps:
        date_ = dt.date()
        if date_ not in dates:
            dates.append(date_)

    occupancy_array = np.zeros((len(dates),))
    for oc_d in occupancy_data:
        date__ = oc_d['DT-Arrival'].date()
        ind = dates.index(date__)
        occupancy_array[ind] += 1
    return list(occupancy_array), list(dates)


def get_daily_bather_load_2(datetime_stamps, occupancy_data):
    dates = []
    for dt in datetime_stamps:
        date_ = dt.date()
        if date_ not in dates:
            dates.append(date_)

    occupancy_array = np.zeros((len(dates),))
    for oc_d in occupancy_data:
        date__ = oc_d['DT-Arrival'].date()
        ind = dates.index(date__)
        occupancy_array[ind] += 1
    return list(occupancy_array), list(dates)


def get_daily_water_treatment(datetime_stamps, chemical_parameters):
    dates = []
    for dt in datetime_stamps:
        date_ = dt.date()
        if date_ not in dates:
            dates.append(date_)

    daily_water_use = np.zeros((len(dates),))
    daily_water_evap = np.zeros((len(dates),))
    daily_water_drain = np.zeros((len(dates),))
    for dt, chem_d in zip(datetime_stamps, chemical_parameters):
        ind = dates.index(dt.date())
        daily_water_use[ind] += chem_d['inW']
        daily_water_evap[ind] += chem_d['Evap']
        daily_water_drain[ind] += chem_d['outW']
    return list(daily_water_use), list(daily_water_evap), list(daily_water_drain)


def get_daily_water_health_quality(datetime_stamps, chemical_parameters, TCM_th):
    dates = []
    for dt in datetime_stamps:
        date_ = dt.date()
        if date_ not in dates:
            dates.append(date_)

    daily_TCM_above_th = np.zeros((len(dates),))
    max_TCM = 0
    daily_TOC_added = np.zeros((len(dates),))
    daily_TCM = np.zeros((len(dates),))
    for dt, chem_d in zip(datetime_stamps, chemical_parameters):
        ind = dates.index(dt.date())
        daily_TOC_added[ind] += chem_d['newTOC']
        daily_TCM[ind] = max(daily_TCM[ind], chem_d['TCM'])
        max_TCM = max(max_TCM, chem_d['TCM'])
        if chem_d['TCM'] > TCM_th:
            daily_TCM_above_th[ind] = 1


    return list(daily_TCM), list(daily_TOC_added), list(daily_TCM_above_th), max_TCM


def plot_bather_load(datetime_stamps, bather_load):
    plt.plot(datetime_stamps, bather_load)
    plt.xlabel("Month-Day Hour")
    plt.ylabel("Bather Load")
    plt.show()


def plot_body_fluid_release(datetime_stamps, body_fluid_release):
    plt.plot(datetime_stamps, body_fluid_release)
    plt.xlabel("Month-Day Hour")
    plt.ylabel("Body Fluid Release (L)")
    plt.show()


def plot_bather_load_and_water_use_twin_chart(dates, bather_load, daily_water_use):
    """
    This function plots a mixed chart of bather load and body fluid release
    :param datetime_stamps: date-time stamps of the input data
    :param bather_load: bather load per the datetime stamps
    :param body_fluid_release: body fluid releases per the datetime stamps
    :return: empty
    """
    x_ticks = []

    for dt_stamp in dates:
        x_ticks.append('{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d")))

    plt.rcParams['grid.color'] = (0.95, 0.95, 0.95, 0.1)

    fig, ax1 = plt.subplots(figsize=(12, 5))

    color = '#117733'

    ax1.set_xlabel('time', weight='bold', size=14)
    ax1.set_ylabel('Bather Load (count)', color=color, weight='bold', size=14)
    g1 = ax1.bar(x_ticks, bather_load, color=color, width=0.5, label='Bather Load')
    ax1.tick_params(axis='y', labelcolor=color)

    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)

    plt.yticks(np.arange(start=0, stop=np.max(bather_load) + 1, step=20).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = '#882255'
    ax2.set_ylabel('Water Use (L)', color=color, weight='bold', size=14)  # we already handled the x-label with ax1
    g2, = ax2.plot(x_ticks, daily_water_use, '--', color=color, label='Daily water use')
    g3, = ax2.plot(x_ticks, np.array(bather_load) * 15, '-', color="black", label='Required daily water use')
    ax2.tick_params(axis='y', labelcolor=color)

    leg = ax2.legend((g1, g2, g3), ('Bather Load', 'Daily water use', 'Required daily water use'), prop={'size': 14})
    counter = 0
    for legobj in leg.legendHandles:
        counter += 1
        if counter == 1:
            legobj.set_linewidth(0.01)
        else:
            legobj.set_linewidth(2.0)


    loc = plticker.MultipleLocator(base=20)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')
    ax2.set_xlim([1, len(x_ticks)-1])
    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_generated_toc_and_tcm_twin_chart_multiple(dates, daily_TOC_added, daily_TCM):
    """
    This function plots a mixed chart of bather load and body fluid release
    :param datetime_stamps: date-time stamps of the input data
    :param bather_load: bather load per the datetime stamps
    :param body_fluid_release: body fluid releases per the datetime stamps
    :return: empty
    """
    methods = list(daily_TOC_added.keys())

    x_ticks = []
    for dt_stamp in dates:
        x_ticks.append('{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d")))

    plt.rcParams['grid.color'] = (0.95, 0.95, 0.95, 0.1)

    fig, ax1 = plt.subplots(figsize=(12, 5))

    color = 'tab:red'

    ax1.set_xlabel('time', weight='bold', size=14)
    ax1.set_ylabel('Daily TOC added (g)', color=color, weight='bold', size=14)
    ax1.bar(x_ticks, np.array(daily_TOC_added[methods[0]]) / 1000, width=0.5, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)
    plt.yticks(np.arange(start=0, stop=np.max(np.array(daily_TOC_added[methods[0]]) / 1000) + 1, step=5).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    line_types = {'Fixed Rate Method': '--', 'Proposed Method': '-', 'Bather Load Method': ':'}
    ax2.set_ylabel('TCM (ug/L)', color=color, weight='bold', size=14)  # we already handled the x-label with ax1
    for method in methods:
        ax2.plot(x_ticks, daily_TCM[method], line_types[method], color=color, linewidth=2, label=method)

    ax2.tick_params(axis='y', labelcolor=color)
    leg = ax2.legend(prop={'size': 14})
    counter = 0
    for legobj in leg.legendHandles:
        counter += 1
        if counter == 1:
            legobj.set_linewidth(2)
        else:
            legobj.set_linewidth(2.0)
    loc = plticker.MultipleLocator(base=20)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')
    ax2.set_xlim([1, len(x_ticks)-1])



    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_generated_toc_and_tcm_twin_chart(dates, daily_TOC_added, daily_TCM):
    """
    This function plots a mixed chart of bather load and body fluid release
    :param datetime_stamps: date-time stamps of the input data
    :param bather_load: bather load per the datetime stamps
    :param body_fluid_release: body fluid releases per the datetime stamps
    :return: empty
    """
    x_ticks = []

    for dt_stamp in dates:

        x_ticks.append('{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d")))

    plt.rcParams['grid.color'] = (0.95, 0.95, 0.95, 0.1)

    fig, ax1 = plt.subplots(figsize=(12, 5))

    color = 'tab:red'

    ax1.set_xlabel('time', weight='bold', size=14)
    ax1.set_ylabel('Daily TOC added (g)', color=color, weight='bold', size=14)
    g1 = ax1.bar(x_ticks, np.array(daily_TOC_added) / 1000, width=0.6, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)
    plt.yticks(np.arange(start=0, stop=np.max(np.array(daily_TOC_added) / 1000) + 1, step=5).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('TCM (ug/L)', color=color, weight='bold', size=14)  # we already handled the x-label with ax1
    g2, = ax2.plot(x_ticks, daily_TCM, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    loc = plticker.MultipleLocator(base=20)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')
    ax2.set_xlim([1, len(x_ticks)-1])

    leg = ax2.legend((g1, g2), ('TCM Concentration', 'Daily Added TOC'), prop={'size': 14})
    counter = 0
    for legobj in leg.legendHandles:
        counter += 1
        if counter == 1:
            legobj.set_linewidth(0.01)
        else:
            legobj.set_linewidth(2.0)

    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_bather_load_and_body_fluid_release_in_one_chart(datetime_stamps, bather_load, body_fluid_release):
    """
    This function plots a mixed chart of bather load and body fluid release
    :param datetime_stamps: date-time stamps of the input data
    :param bather_load: bather load per the datetime stamps
    :param body_fluid_release: body fluid releases per the datetime stamps
    :return: empty
    """

    ticks_period_minutes = 420
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []

    for dt_stamp in datetime_stamps:
        x_ticks.append('{}-{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%a"),
                                         dt_stamp.strftime("%H:%M %p")))

    fig, ax1 = plt.subplots(figsize=(35, 7))

    color = 'tab:red'

    ax1.set_xlabel('time', weight='bold', size=12)
    ax1.set_ylabel('Bather Load (count)', color=color, weight='bold', size=12)
    ax1.plot(x_ticks, bather_load, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    plt.yticks(np.arange(start=0, stop=np.max(bather_load) + 1, step=2).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Sweat Release (L)', color=color, weight='bold', size=12)  # we already handled the x-label with ax1
    ax2.plot(x_ticks, body_fluid_release, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')

    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_bather_load_and_tcm_concentration_in_one_chart(datetime_stamps, bather_load, chemical_parameters):
    """
    This function plots a mixed chart of bather load and tcm concentration
    :param datetime_stamps:
    :param bather_load:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 60 * 24 * 7
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []
    tcms = []
    for dt_stamp, chem_params in zip(datetime_stamps, chemical_parameters):
        tcms.append(chem_params["TCM"])
        x_ticks.append('{}-{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d"),
                                         dt_stamp.strftime("%H:%M %p")))

    fig, ax1 = plt.subplots(figsize=(35, 7))

    color = 'tab:red'

    ax1.set_xlabel('time', weight='bold', size=12)
    ax1.set_ylabel('Bather Load (count)', color=color, weight='bold', size=12)
    ax1.plot(x_ticks, bather_load, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    plt.yticks(np.arange(start=0, stop=np.max(bather_load) + 1, step=2).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('tcm concentration (ug/L)', color=color, weight='bold', size=12)  # we already handled the x-label with ax1
    ax2.plot(x_ticks, np.array(tcms), color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0, 200])
    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')

    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_toc_generated_and_tcm_concentration_in_one_chart(datetime_stamps, chemical_parameters):
    """
    This function plots a mixed chart of bather load and tcm concentration
    :param datetime_stamps:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 60 * 24 * 7
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []
    tcms = []
    tocs = []
    for dt_stamp, chem_params in zip(datetime_stamps, chemical_parameters):
        tcms.append(chem_params["TCM"])
        tocs.append(chem_params["newTOC"])
        x_ticks.append('{}-{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d"),
                                         dt_stamp.strftime("%H:%M %p")))

    fig, ax1 = plt.subplots(figsize=(35, 7))

    color = 'tab:red'

    ax1.set_xlabel('time', weight='bold', size=12)
    ax1.set_ylabel('toc generated (mg)', color=color, weight='bold', size=12)
    ax1.plot(x_ticks, np.array(tocs), color=color)
    ax1.set_ylim([0, 10])
    ax1.tick_params(axis='y', labelcolor=color)

    plt.yticks(np.arange(start=0, stop=np.max(tocs) + 1, step=np.max(tocs) / 10).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('tcm concentration (ug/L)', color=color, weight='bold', size=12)  # we already handled the x-label with ax1
    ax2.plot(x_ticks, np.array(tcms), color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0, 200])
    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax2.xaxis.set_major_locator(loc)
    ax1.xaxis.set_major_locator(loc)
    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')
    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_toc_and_tcm_concentration_in_one_chart(datetime_stamps, chemical_parameters):
    """
    This function plots a mixed chart of bather load and tcm concentration
    :param datetime_stamps:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 60 * 24 * 7
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []
    tcms = []
    tocs = []
    for dt_stamp, chem_params in zip(datetime_stamps, chemical_parameters):
        tcms.append(chem_params["TCM"])
        tocs.append(chem_params["toc"])
        x_ticks.append('{}-{}-{}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d"),
                                         dt_stamp.strftime("%H:%M %p")))

    fig, ax1 = plt.subplots(figsize=(35, 7))

    color = 'tab:red'

    ax1.set_xlabel('time', weight='bold', size=12)
    ax1.set_ylabel('toc concentration (mg/L)', color=color, weight='bold', size=12)
    ax1.plot(x_ticks, np.array(tocs), color=color)
    ax1.set_ylim([0, 10])
    ax1.tick_params(axis='y', labelcolor=color)

    plt.yticks(np.arange(start=0, stop=np.max(tocs) + 1, step=np.max(tocs) / 10).astype(np.int))

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('tcm concentration (ug/L)', color=color, weight='bold', size=12)  # we already handled the x-label with ax1
    ax2.plot(x_ticks, np.array(tcms), color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0, 200])
    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax2.xaxis.set_major_locator(loc)
    ax1.xaxis.set_major_locator(loc)
    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')
    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_tcm_concentration(datetime_stamps, chemical_parameters):
    """
    This function plots a mixed chart of bather load and tcm concentration
    :param datetime_stamps:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 3600
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []
    tcms = []
    for dt_stamp, chem_params in zip(datetime_stamps, chemical_parameters):
        tcms.append(chem_params["TCM"])

    fig, ax1 = plt.subplots(figsize=(35, 7))

    color = 'tab:red'

    ax1.set_ylabel('tcm concentration (ug/L)', color=color, weight='bold', size=12)  # we already handled the x-label with ax1
    ax1.plot(np.array(tcms), color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0, 200])
    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')

    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_toc_concentration(datetime_stamps, chemical_parameters):
    """
    This function plots a mixed chart of bather load and tcm concentration
    :param datetime_stamps:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 3600
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []
    tocs = []
    for dt_stamp, chem_params in zip(datetime_stamps, chemical_parameters):
        tocs.append(chem_params["toc"])

    fig, ax1 = plt.subplots(figsize=(35, 7))

    color = 'tab:red'

    ax1.set_ylabel('toc (mg/L)', color=color, weight='bold', size=12)  # we already handled the x-label with ax1
    ax1.plot(np.array(tocs), color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0, 4])
    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)

    ax1.xaxis.grid(True, linestyle='--')

    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_water_in_one_chart(datetime_stamps, water_evaporation, water_flow_in, water_flow_out, chemical_parameters):
    """

    :param datetime_stamps:
    :param water_evaporation:
    :param water_flow_in:
    :param water_flow_out:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 60 * 24
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds

    x_ticks = []
    Es = []
    wis = []
    wos = []
    Vs = []
    cwu = []
    vowusf = 0
    for dts, e, wi, wo, cp in zip(datetime_stamps, water_evaporation, water_flow_in, water_flow_out,
                                  chemical_parameters):
        vow = cp["VoW"]
        Es.append(e)
        wis.append(wi)
        wos.append(wo)
        Vs.append(vow)
        vowusf += wi
        cwu.append(vowusf)
        x_ticks.append('{}-{}-{}'.format(dts.strftime("%b"), dts.strftime("%d"), dts.strftime("%H:%M %p")))

    fig, ax1 = plt.subplots(figsize=(35, 7))
    ax1.set_xlabel('time', weight='bold', size=12)
    ax1.set_ylabel('liters', weight='bold', size=12)
    ax1.plot(x_ticks, cwu, label="Water Used")
    plt.legend(loc="upper left")

    #plt.yticks(np.arange(start=0, stop=np.max(cwu) + 1, step=5000).astype(np.int))
    ax1.set_ylim([0, 120000])
    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1.xaxis.set_major_locator(loc)
    ax1.xaxis.grid(True, linestyle='--')
    ax1.yaxis.grid(True, linestyle='--')

    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped
    plt.show()


def plot_bather_load_and_tcm_concentration_in_one_chart_v2(datetime_stamps, wf_ins, bather_load, body_fluid_release,
                                                           chemical_parameters):
    """
    This function plots a mixed chart of bather load and tcm concentration
    :param datetime_stamps:
    :param bather_load:
    :param chemical_parameters:
    :return:
    """
    ticks_period_minutes = 60 * 24
    time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds
    ticks_multiplier = ticks_period_minutes * 60 / time_period_seconds
    x_ticks = []

    tcms = []
    water_use = []
    sweat_release = []

    for dt_stamp, chem_params, wf_in, bfa in zip(datetime_stamps, chemical_parameters, wf_ins, body_fluid_release):
        tcms.append(1000 * chem_params["TCM"])
        water_use.append(wf_in)
        sweat_release.append(bfa)
        x_ticks.append('{}-{}, {}'.format(dt_stamp.strftime("%b"), dt_stamp.strftime("%d"),
                                         dt_stamp.strftime("%H:%M")))

    fig, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(20, 15))

    color = 'tab:red'

    ax1[0].set_xlabel('time', weight='bold', size=15)
    ax1[0].set_ylabel('Sweat Release (Liter)', color=color, weight='bold', size=15)
    ax1[0].plot(x_ticks, np.array(sweat_release), color=color)
    ax1[0].tick_params(axis='y', labelcolor=color)

    #plt.yticks(np.arange(start=0, stop=np.max(sweat_release) + 1, step=2).astype(np.int))

    ax2 = ax1[0].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Water Use (Liter)', color=color, weight='bold', size=14)  # we already handled the x-label with ax1
    ax2.plot(x_ticks, np.array(water_use), color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    loc = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1[0].xaxis.set_major_locator(loc)
    ax2.xaxis.set_major_locator(loc)

    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    ax1[0].xaxis.grid(True, linestyle='--')
    ax1[0].yaxis.grid(True, linestyle='--')

    ax1[1].set_xlabel('time', weight='bold', size=15)

    ax1[1].set_ylabel('TCM (ug / Liter)', color=color, weight='bold', size=14)
    ax1[1].plot(x_ticks, np.array(tcms), color=color)

    loc2 = plticker.MultipleLocator(base=ticks_multiplier)  # this locator puts ticks at regular intervals
    ax1[1].xaxis.set_major_locator(loc2)
    ax1[1].set_ylim([30, 50])
    fig.tight_layout()  # Otherwise, the right y-label is slightly clipped

    plt.setp(ax1[0].get_xticklabels(), fontsize=15)
    plt.setp(ax1[1].get_xticklabels(), fontsize=15)
    plt.setp(ax1[1].get_yticklabels(), fontsize=14)
    plt.setp(ax1[0].get_yticklabels(), fontsize=15)
    plt.setp(ax2.get_yticklabels(), fontsize=15)

    plt.show()

    print('hy')