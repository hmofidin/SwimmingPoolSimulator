import json
import numpy as np
from matplotlib import pyplot as plt


class ModelChemicalParameters:
    def __init__(self, json_file_path='SwimmingPoolChemicalParameters.json'):
        """
        C2HCl3O2: Trichloroacetic acid (TCAA)
	    C2H2Cl2O2: Dichloroacetic acid (DCAA)
	    CHCl3: Chloroform or trichloromethane (TCM)
        This init function is responsible to initialize parameters of the chemicals modeling
        :param json_file_path: the path of json file containing parameters of chemical modeling
        """
        with open(json_file_path, encoding='utf8') as f:
            try:
                parameters = json.load(f)
                self.r = parameters['R']
                self.bf_2_toc_ratio_mg = parameters['bf_2_toc_ratio_mg']

                self.tcm_ea = parameters['TCM']['EA']
                self.tcm_a = parameters['TCM']['A']
                self.tcm_m = parameters['TCM']['m']
                self.tcm_n = parameters['TCM']['n']
                self.tcm_molar_mass = parameters['TCM']['MolarMass']

                self.dcaa_ea = parameters['DCAA']['EA']
                self.dcaa_a = parameters['DCAA']['A']
                self.dcaa_m = parameters['DCAA']['m']
                self.dcaa_n = parameters['DCAA']['n']
                self.dcaa_molar_mass = parameters['DCAA']['MolarMass']

                self.tcaa_ea = parameters['TCAA']['EA']
                self.tcaa_a = parameters['TCAA']['A']
                self.tcaa_m = parameters['TCAA']['m']
                self.tcaa_n = parameters['TCAA']['n']
                self.tcaa_molar_mass = parameters['TCAA']['MolarMass']

                self.dcan_ea = parameters['DCAN']['EA']
                self.dcan_a = parameters['DCAN']['A']
                self.dcan_m = parameters['DCAN']['m']
                self.dcan_n = parameters['DCAN']['n']
                self.dcan_molar_mass = parameters['DCAN']['MolarMass']

                self.ChlorineUseOfDBPs = {"DCAA": 2, "TCAA": 3, "TCM": 3, "DCAN": 2}
                self.CarbonUseOfDBPs = {"DCAA": 2, "TCAA": 2, "TCM": 1, "DCAN": 2}

                self.carbon_molar_mass = 12.011
                self.chlorine_molar_mass = 35.453

            except ValueError:
                print('error extracting and initializing chemical model parameters!')
# a=[15, 25, 35, 50];b=[0.053, 0.055, 0.125, 0.166]; x = [y * np.exp(22300/(8.3145*(273.15+x))) for (x, y) in zip(a, b)]; A = np.sum(np.array(x))/4;


    def process_chemical_parameters(self, initial_chemical_parameters, datetime_stamps, body_fluid_release,
                                    swimming_pool_water_temperature_celsius, swimming_pool_volume_of_water,
                                    water_evaporation, input_flow_freshwater, output_flow_wastewater):
        """
        This function processes chemical components and parameters of swimming pool in the defines datetime stamps based
        on initial chemical parameters, body fluid releases happening at each datetime stamp, and water temperature
        :param initial_chemical_parameters:
        :param datetime_stamps:
        :param body_fluid_release:
        :param swimming_pool_water_temperature_celsius:
        :param swimming_pool_volume_of_water:
        :param water_evaporation:
        :param input_flow_freshwater:
        :param output_flow_wastewater:
        :return: chemical parameters per each datetime-stamp
        """
        # calculate apparent reaction rate constant of TCM formation

        abs_water_temp = 273.5 + swimming_pool_water_temperature_celsius

        tcm_k1 = self.tcm_a * np.exp(-self.tcm_ea / (self.r * abs_water_temp))
        dcaa_k1 = self.dcaa_a * np.exp(-self.dcaa_ea / (self.r * abs_water_temp))
        tcaa_k1 = self.tcaa_a * np.exp(-self.tcaa_ea / (self.r * abs_water_temp))
        dcan_k1 = self.dcan_a * np.exp(-self.dcan_ea / (self.r * abs_water_temp))

        time_period_seconds = (datetime_stamps[1] - datetime_stamps[0]).seconds

        ratio_hour_2_period = time_period_seconds / 3600
        initial_fac = initial_chemical_parameters["FAC"]
        initial_tcm = initial_chemical_parameters["TCM"]

        initial_cc = initial_chemical_parameters["CC"]
        initial_ph = initial_chemical_parameters["pH"]
        initial_orp = initial_chemical_parameters["ORP"]
        initial_body_fluid_per_liter_of_swimming_pool_water = initial_chemical_parameters["BF"]

        # Evaporation Rate of Chloroform: 11.6 (BuAc=1) link: http://colinmayfield.com/biology447/Assignments/assignment1/chloroform/chloroform.htm
        # Evaporation Rate of Water: 0.3 (BuAc=1)
        tcm_evaporation_rate = 11.6 / 0.3

        percentage_used_4_dbp = 1.0

        tcm_coeff = ratio_hour_2_period * tcm_k1
        dcaa_coeff = ratio_hour_2_period * dcaa_k1
        tcaa_coeff = ratio_hour_2_period * tcaa_k1
        dcan_coeff = ratio_hour_2_period * dcan_k1

        # run simulation of chemical contents
        fac = initial_fac
        cc = initial_cc
        orp = initial_orp
        ph = initial_ph
        tcm = initial_tcm

        dcaa = 0
        tcaa = 0
        dcan = 0

        total_body_fluid = initial_body_fluid_per_liter_of_swimming_pool_water * swimming_pool_volume_of_water

        chemical_parameters = []
        vow = swimming_pool_volume_of_water

        toc = total_body_fluid * self.bf_2_toc_ratio_mg / vow

        tcms = []

        mug_2_mg = 0.001

        for dt_stamp, new_body_fluid_rel, E, inW, outW in zip(datetime_stamps, body_fluid_release, water_evaporation,
                                                              input_flow_freshwater, output_flow_wastewater):

            new_tcm = vow * tcm_coeff * ((toc * percentage_used_4_dbp) *
                                         (self.tcm_m * abs_water_temp + self.tcm_n) - tcm)

            new_dcaa = vow * dcaa_coeff * ((toc * percentage_used_4_dbp) *
                                           (self.dcaa_m * abs_water_temp + self.dcaa_n) - dcaa)

            new_tcaa = vow * tcaa_coeff * ((toc * percentage_used_4_dbp) *
                                           (self.tcaa_m * abs_water_temp + self.tcaa_n) - tcaa)

            new_dcan = vow * dcan_coeff * ((toc * percentage_used_4_dbp) *
                                           (self.tcaa_m * abs_water_temp + self.tcaa_n) - dcan)

            consumed_toc_by_tcm = (self.CarbonUseOfDBPs['TCM'] * ((new_tcm * mug_2_mg) / self.tcm_molar_mass)) \
                                  * self.carbon_molar_mass

            consumed_toc_by_dcaa = (self.CarbonUseOfDBPs['DCAA'] * ((new_dcaa * mug_2_mg) / self.dcaa_molar_mass)) \
                                  * self.carbon_molar_mass

            consumed_toc_by_tcaa = (self.CarbonUseOfDBPs['TCAA'] * ((new_tcaa * mug_2_mg) / self.tcaa_molar_mass)) \
                                   * self.carbon_molar_mass

            consumed_toc_by_dcan = (self.CarbonUseOfDBPs['DCAN'] * ((new_dcan * mug_2_mg) / self.dcan_molar_mass)) \
                                   * self.carbon_molar_mass

            # must be calculated in mol
            consumed_toc = consumed_toc_by_tcm + consumed_toc_by_dcaa + consumed_toc_by_tcaa + consumed_toc_by_dcan

            new_toc = new_body_fluid_rel * self.bf_2_toc_ratio_mg

            toc = ((vow - outW) * toc + new_toc - consumed_toc) / (vow - outW - E + inW)

            # TCM concentration at current datetime stamp
            tcm = ((vow - outW - tcm_evaporation_rate * E) * tcm + new_tcm) / (vow - outW - E + inW)

            dcaa = ((vow - outW - tcm_evaporation_rate * E) * dcaa + new_dcaa) / (vow - outW - E + inW)

            tcaa = ((vow - outW - tcm_evaporation_rate * E) * tcaa + new_tcaa) / (vow - outW - E + inW)

            dcan = ((vow - outW - tcm_evaporation_rate * E) * dcan + new_dcan) / (vow - outW - E + inW)

            vow = vow - outW + inW - E

            #if new_toc > 0:
            #    print('new_toc:{}'.format(new_toc))

            chemical_parameters.append({"FAC": fac, "TCM": tcm, "DCAA": dcaa, "TCAA": tcaa, "TCAA": dcan, "CC": cc,
                                        "pH": ph, "ORP": orp, "toc": toc, "VoW": vow, "newTOC": new_toc,
                                        'Evap': E, 'inW': inW, 'outW': outW})

        return chemical_parameters
