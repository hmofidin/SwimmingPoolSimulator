import json
import datetime
import random
import numpy as np
import utils


class ModelOccupancyParameters:
    def __init__(self, json_file_path='SwimmingPoolOccupancyParameters.json'):
        """
        This init function is responsible to initialize parameters of the occupancy modeling
        :param json_file_path: the path of json file containing parameters of occupancy modeling
        """
        with open(json_file_path, encoding='utf8') as f:
            try:
                parameters = json.load(f)

                self.Monthly_InterArrivalTime_Seconds_Mean = {
                    'January': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["January"]["mean"],
                    'February': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["February"]["mean"],
                    'March': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["March"]["mean"],
                    'May': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["May"]["mean"],
                    'April': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["April"]["mean"],
                    'June': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["June"]["mean"],
                    'July': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["July"]["mean"],
                    'August': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["August"]["mean"],
                    'September': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["September"]["mean"],
                    'October': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["October"]["mean"],
                    'November': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["November"]["mean"],
                    'December': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["December"]["mean"]}

                self.Monthly_InterArrivalRate_Seconds_Std = {
                    'January': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["January"]["std"],
                    'February': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["February"]["std"],
                    'March': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["March"]["std"],
                    'May': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["May"]["std"],
                    'April': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["April"]["std"],
                    'June': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["June"]["std"],
                    'July': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["July"]["std"],
                    'August': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["August"]["std"],
                    'September': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["September"]["std"],
                    'October': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["October"]["std"],
                    'November': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["November"]["std"],
                    'December': parameters["MonthlyPattern"]["InterArrivalTime_Seconds"]["December"]["std"]}

                self.Monthly_Gender_Male_Probability = {
                    'January': parameters["MonthlyPattern"]["GenderMaleProbability"]["January"],
                    'February': parameters["MonthlyPattern"]["GenderMaleProbability"]["February"],
                    'March': parameters["MonthlyPattern"]["GenderMaleProbability"]["March"],
                    'May': parameters["MonthlyPattern"]["GenderMaleProbability"]["May"],
                    'April': parameters["MonthlyPattern"]["GenderMaleProbability"]["April"],
                    'June': parameters["MonthlyPattern"]["GenderMaleProbability"]["June"],
                    'July': parameters["MonthlyPattern"]["GenderMaleProbability"]["July"],
                    'August': parameters["MonthlyPattern"]["GenderMaleProbability"]["August"],
                    'September': parameters["MonthlyPattern"]["GenderMaleProbability"]["September"],
                    'October': parameters["MonthlyPattern"]["GenderMaleProbability"]["October"],
                    'November': parameters["MonthlyPattern"]["GenderMaleProbability"]["November"],
                    'December': parameters["MonthlyPattern"]["GenderMaleProbability"]["December"]}

                self.Monthly_Age_Low_Distribution_Mean = {
                    'January': parameters["MonthlyPattern"]["AgeLowDistribution"]["January"]["mean"],
                    'February': parameters["MonthlyPattern"]["AgeLowDistribution"]["February"]["mean"],
                    'March': parameters["MonthlyPattern"]["AgeLowDistribution"]["March"]["mean"],
                    'May': parameters["MonthlyPattern"]["AgeLowDistribution"]["May"]["mean"],
                    'April': parameters["MonthlyPattern"]["AgeLowDistribution"]["April"]["mean"],
                    'June': parameters["MonthlyPattern"]["AgeLowDistribution"]["June"]["mean"],
                    'July': parameters["MonthlyPattern"]["AgeLowDistribution"]["July"]["mean"],
                    'August': parameters["MonthlyPattern"]["AgeLowDistribution"]["August"]["mean"],
                    'September': parameters["MonthlyPattern"]["AgeLowDistribution"]["September"]["mean"],
                    'October': parameters["MonthlyPattern"]["AgeLowDistribution"]["October"]["mean"],
                    'November': parameters["MonthlyPattern"]["AgeLowDistribution"]["November"]["mean"],
                    'December': parameters["MonthlyPattern"]["AgeLowDistribution"]["December"]["mean"]}

                self.Monthly_Age_Low_Distribution_Std = {
                    'January': parameters["MonthlyPattern"]["AgeLowDistribution"]["January"]["std"],
                    'February': parameters["MonthlyPattern"]["AgeLowDistribution"]["February"]["std"],
                    'March': parameters["MonthlyPattern"]["AgeLowDistribution"]["March"]["std"],
                    'May': parameters["MonthlyPattern"]["AgeLowDistribution"]["May"]["std"],
                    'April': parameters["MonthlyPattern"]["AgeLowDistribution"]["April"]["std"],
                    'June': parameters["MonthlyPattern"]["AgeLowDistribution"]["June"]["std"],
                    'July': parameters["MonthlyPattern"]["AgeLowDistribution"]["July"]["std"],
                    'August': parameters["MonthlyPattern"]["AgeLowDistribution"]["August"]["std"],
                    'September': parameters["MonthlyPattern"]["AgeLowDistribution"]["September"]["std"],
                    'October': parameters["MonthlyPattern"]["AgeLowDistribution"]["October"]["std"],
                    'November': parameters["MonthlyPattern"]["AgeLowDistribution"]["November"]["std"],
                    'December': parameters["MonthlyPattern"]["AgeLowDistribution"]["December"]["std"]}

                self.Monthly_Age_High_Distribution_Mean = {
                    'January': parameters["MonthlyPattern"]["AgeHighDistribution"]["January"]["mean"],
                    'February': parameters["MonthlyPattern"]["AgeHighDistribution"]["February"]["mean"],
                    'March': parameters["MonthlyPattern"]["AgeHighDistribution"]["March"]["mean"],
                    'May': parameters["MonthlyPattern"]["AgeHighDistribution"]["May"]["mean"],
                    'April': parameters["MonthlyPattern"]["AgeHighDistribution"]["April"]["mean"],
                    'June': parameters["MonthlyPattern"]["AgeHighDistribution"]["June"]["mean"],
                    'July': parameters["MonthlyPattern"]["AgeHighDistribution"]["July"]["mean"],
                    'August': parameters["MonthlyPattern"]["AgeHighDistribution"]["August"]["mean"],
                    'September': parameters["MonthlyPattern"]["AgeHighDistribution"]["September"]["mean"],
                    'October': parameters["MonthlyPattern"]["AgeHighDistribution"]["October"]["mean"],
                    'November': parameters["MonthlyPattern"]["AgeHighDistribution"]["November"]["mean"],
                    'December': parameters["MonthlyPattern"]["AgeHighDistribution"]["December"]["mean"]}

                self.Monthly_Age_High_Distribution_Std = {
                     'January': parameters["MonthlyPattern"]["AgeHighDistribution"]["January"]["std"],
                     'February': parameters["MonthlyPattern"]["AgeHighDistribution"]["February"]["std"],
                     'March': parameters["MonthlyPattern"]["AgeHighDistribution"]["March"]["std"],
                     'May': parameters["MonthlyPattern"]["AgeHighDistribution"]["May"]["std"],
                     'April': parameters["MonthlyPattern"]["AgeHighDistribution"]["April"]["std"],
                     'June': parameters["MonthlyPattern"]["AgeHighDistribution"]["June"]["std"],
                     'July': parameters["MonthlyPattern"]["AgeHighDistribution"]["July"]["std"],
                     'August': parameters["MonthlyPattern"]["AgeHighDistribution"]["August"]["std"],
                     'September': parameters["MonthlyPattern"]["AgeHighDistribution"]["September"]["std"],
                     'October': parameters["MonthlyPattern"]["AgeHighDistribution"]["October"]["std"],
                     'November': parameters["MonthlyPattern"]["AgeHighDistribution"]["November"]["std"],
                     'December': parameters["MonthlyPattern"]["AgeHighDistribution"]["December"]["std"]}

                self.WeekDaily_InterArrivalTime_Divider = {
                    'Saturday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Saturday"],
                    'Sunday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Sunday"],
                    'Monday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Monday"],
                    'Tuesday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Tuesday"],
                    'Wednesday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Wednesday"],
                    'Thursday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Thursday"],
                    'Friday': parameters["WeekDailyPattern"]["InterArrivalTime_Divider"]["Friday"]}

                self.WeekDaily_Gender_Multiplier = {
                    'Saturday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Saturday"],
                    'Sunday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Sunday"],
                    'Monday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Monday"],
                    'Tuesday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Tuesday"],
                    'Wednesday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Wednesday"],
                    'Thursday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Thursday"],
                    'Friday': parameters["WeekDailyPattern"]["Gender_Multiplier"]["Friday"]}

                self.WeekDaily_AgeLow_Multiplier = {
                    'Saturday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Saturday"],
                    'Sunday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Sunday"],
                    'Monday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Monday"],
                    'Tuesday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Tuesday"],
                    'Wednesday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Wednesday"],
                    'Thursday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Thursday"],
                    'Friday': parameters["WeekDailyPattern"]["AgeLow_Multiplier"]["Friday"]}

                self.WeekDaily_AgeHigh_Multiplier = {
                    'Saturday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Saturday"],
                    'Sunday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Sunday"],
                    'Monday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Monday"],
                    'Tuesday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Tuesday"],
                    'Wednesday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Wednesday"],
                    'Thursday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Thursday"],
                    'Friday': parameters["WeekDailyPattern"]["AgeHigh_Multiplier"]["Friday"]}

                self.Hourly_InterArrivalRate_Divider = {
                    '0': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["0"],
                    '1': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["1"],
                    '2': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["2"],
                    '3': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["3"],
                    '4': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["4"],
                    '5': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["5"],
                    '6': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["6"],
                    '7': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["7"],
                    '8': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["8"],
                    '9': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["9"],
                    '10': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["10"],
                    '11': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["11"],
                    '12': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["12"],
                    '13': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["13"],
                    '14': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["14"],
                    '15': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["15"],
                    '16': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["16"],
                    '17': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["17"],
                    '18': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["18"],
                    '19': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["19"],
                    '20': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["20"],
                    '21': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["21"],
                    '22': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["22"],
                    '23': parameters["HourlyPattern"]["InterArrivalRate_Divider"]["23"]}

                self.Hourly_Gender_Multiplier = {
                    '0': parameters["HourlyPattern"]["Gender_Multiplier"]["0"],
                    '1': parameters["HourlyPattern"]["Gender_Multiplier"]["1"],
                    '2': parameters["HourlyPattern"]["Gender_Multiplier"]["2"],
                    '3': parameters["HourlyPattern"]["Gender_Multiplier"]["3"],
                    '4': parameters["HourlyPattern"]["Gender_Multiplier"]["4"],
                    '5': parameters["HourlyPattern"]["Gender_Multiplier"]["5"],
                    '6': parameters["HourlyPattern"]["Gender_Multiplier"]["6"],
                    '7': parameters["HourlyPattern"]["Gender_Multiplier"]["7"],
                    '8': parameters["HourlyPattern"]["Gender_Multiplier"]["8"],
                    '9': parameters["HourlyPattern"]["Gender_Multiplier"]["9"],
                    '10': parameters["HourlyPattern"]["Gender_Multiplier"]["10"],
                    '11': parameters["HourlyPattern"]["Gender_Multiplier"]["11"],
                    '12': parameters["HourlyPattern"]["Gender_Multiplier"]["12"],
                    '13': parameters["HourlyPattern"]["Gender_Multiplier"]["13"],
                    '14': parameters["HourlyPattern"]["Gender_Multiplier"]["14"],
                    '15': parameters["HourlyPattern"]["Gender_Multiplier"]["15"],
                    '16': parameters["HourlyPattern"]["Gender_Multiplier"]["16"],
                    '17': parameters["HourlyPattern"]["Gender_Multiplier"]["17"],
                    '18': parameters["HourlyPattern"]["Gender_Multiplier"]["18"],
                    '19': parameters["HourlyPattern"]["Gender_Multiplier"]["19"],
                    '20': parameters["HourlyPattern"]["Gender_Multiplier"]["20"],
                    '21': parameters["HourlyPattern"]["Gender_Multiplier"]["21"],
                    '22': parameters["HourlyPattern"]["Gender_Multiplier"]["22"],
                    '23': parameters["HourlyPattern"]["Gender_Multiplier"]["23"]}

                self.Hourly_AgeLow_Multiplier = {
                    '0': parameters["HourlyPattern"]["AgeLow_Multiplier"]["0"],
                    '1': parameters["HourlyPattern"]["AgeLow_Multiplier"]["1"],
                    '2': parameters["HourlyPattern"]["AgeLow_Multiplier"]["2"],
                    '3': parameters["HourlyPattern"]["AgeLow_Multiplier"]["3"],
                    '4': parameters["HourlyPattern"]["AgeLow_Multiplier"]["4"],
                    '5': parameters["HourlyPattern"]["AgeLow_Multiplier"]["5"],
                    '6': parameters["HourlyPattern"]["AgeLow_Multiplier"]["6"],
                    '7': parameters["HourlyPattern"]["AgeLow_Multiplier"]["7"],
                    '8': parameters["HourlyPattern"]["AgeLow_Multiplier"]["8"],
                    '9': parameters["HourlyPattern"]["AgeLow_Multiplier"]["9"],
                    '10': parameters["HourlyPattern"]["AgeLow_Multiplier"]["10"],
                    '11': parameters["HourlyPattern"]["AgeLow_Multiplier"]["11"],
                    '12': parameters["HourlyPattern"]["AgeLow_Multiplier"]["12"],
                    '13': parameters["HourlyPattern"]["AgeLow_Multiplier"]["13"],
                    '14': parameters["HourlyPattern"]["AgeLow_Multiplier"]["14"],
                    '15': parameters["HourlyPattern"]["AgeLow_Multiplier"]["15"],
                    '16': parameters["HourlyPattern"]["AgeLow_Multiplier"]["16"],
                    '17': parameters["HourlyPattern"]["AgeLow_Multiplier"]["17"],
                    '18': parameters["HourlyPattern"]["AgeLow_Multiplier"]["18"],
                    '19': parameters["HourlyPattern"]["AgeLow_Multiplier"]["19"],
                    '20': parameters["HourlyPattern"]["AgeLow_Multiplier"]["20"],
                    '21': parameters["HourlyPattern"]["AgeLow_Multiplier"]["21"],
                    '22': parameters["HourlyPattern"]["AgeLow_Multiplier"]["22"],
                    '23': parameters["HourlyPattern"]["AgeLow_Multiplier"]["23"]}

                self.Hourly_AgeHigh_Multiplier = {
                    '0': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["0"],
                    '1': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["1"],
                    '2': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["2"],
                    '3': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["3"],
                    '4': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["4"],
                    '5': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["5"],
                    '6': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["6"],
                    '7': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["7"],
                    '8': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["8"],
                    '9': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["9"],
                    '10': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["10"],
                    '11': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["11"],
                    '12': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["12"],
                    '13': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["13"],
                    '14': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["14"],
                    '15': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["15"],
                    '16': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["16"],
                    '17': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["17"],
                    '18': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["18"],
                    '19': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["19"],
                    '20': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["20"],
                    '21': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["21"],
                    '22': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["22"],
                    '23': parameters["HourlyPattern"]["AgeHigh_Multiplier"]["23"]}

                self.Hourly_ProbabilityAdult = {
                    '0': parameters["HourlyPattern"]["ProbabilityAdult"]["0"],
                    '1': parameters["HourlyPattern"]["ProbabilityAdult"]["1"],
                    '2': parameters["HourlyPattern"]["ProbabilityAdult"]["2"],
                    '3': parameters["HourlyPattern"]["ProbabilityAdult"]["3"],
                    '4': parameters["HourlyPattern"]["ProbabilityAdult"]["4"],
                    '5': parameters["HourlyPattern"]["ProbabilityAdult"]["5"],
                    '6': parameters["HourlyPattern"]["ProbabilityAdult"]["6"],
                    '7': parameters["HourlyPattern"]["ProbabilityAdult"]["7"],
                    '8': parameters["HourlyPattern"]["ProbabilityAdult"]["8"],
                    '9': parameters["HourlyPattern"]["ProbabilityAdult"]["9"],
                    '10': parameters["HourlyPattern"]["ProbabilityAdult"]["10"],
                    '11': parameters["HourlyPattern"]["ProbabilityAdult"]["11"],
                    '12': parameters["HourlyPattern"]["ProbabilityAdult"]["12"],
                    '13': parameters["HourlyPattern"]["ProbabilityAdult"]["13"],
                    '14': parameters["HourlyPattern"]["ProbabilityAdult"]["14"],
                    '15': parameters["HourlyPattern"]["ProbabilityAdult"]["15"],
                    '16': parameters["HourlyPattern"]["ProbabilityAdult"]["16"],
                    '17': parameters["HourlyPattern"]["ProbabilityAdult"]["17"],
                    '18': parameters["HourlyPattern"]["ProbabilityAdult"]["18"],
                    '19': parameters["HourlyPattern"]["ProbabilityAdult"]["19"],
                    '20': parameters["HourlyPattern"]["ProbabilityAdult"]["20"],
                    '21': parameters["HourlyPattern"]["ProbabilityAdult"]["21"],
                    '22': parameters["HourlyPattern"]["ProbabilityAdult"]["22"],
                    '23': parameters["HourlyPattern"]["ProbabilityAdult"]["23"]}

                self.Hourly_TimeOfStay_Minutes_mean = {
                    '0': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["0"],
                    '1': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["1"],
                    '2': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["2"],
                    '3': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["3"],
                    '4': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["4"],
                    '5': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["5"],
                    '6': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["6"],
                    '7': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["7"],
                    '8': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["8"],
                    '9': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["9"],
                    '10': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["10"],
                    '11': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["11"],
                    '12': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["12"],
                    '13': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["13"],
                    '14': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["14"],
                    '15': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["15"],
                    '16': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["16"],
                    '17': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["17"],
                    '18': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["18"],
                    '19': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["19"],
                    '20': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["20"],
                    '21': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["21"],
                    '22': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["22"],
                    '23': parameters["HourlyPattern"]["TimeOfStay_Minutes_mean"]["23"]}

                self.Hourly_TimeOfStay_Minutes_std = {
                    '0': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["0"],
                    '1': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["1"],
                    '2': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["2"],
                    '3': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["3"],
                    '4': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["4"],
                    '5': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["5"],
                    '6': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["6"],
                    '7': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["7"],
                    '8': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["8"],
                    '9': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["9"],
                    '10': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["10"],
                    '11': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["11"],
                    '12': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["12"],
                    '13': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["13"],
                    '14': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["14"],
                    '15': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["15"],
                    '16': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["16"],
                    '17': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["17"],
                    '18': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["18"],
                    '19': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["19"],
                    '20': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["20"],
                    '21': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["21"],
                    '22': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["22"],
                    '23': parameters["HourlyPattern"]["TimeOfStay_Minutes_std"]["23"]}

                self.Hourly_ActivityLevel_mean = {
                    '0': parameters["HourlyPattern"]["ActivityLevel_mean"]["0"],
                    '1': parameters["HourlyPattern"]["ActivityLevel_mean"]["1"],
                    '2': parameters["HourlyPattern"]["ActivityLevel_mean"]["2"],
                    '3': parameters["HourlyPattern"]["ActivityLevel_mean"]["3"],
                    '4': parameters["HourlyPattern"]["ActivityLevel_mean"]["4"],
                    '5': parameters["HourlyPattern"]["ActivityLevel_mean"]["5"],
                    '6': parameters["HourlyPattern"]["ActivityLevel_mean"]["6"],
                    '7': parameters["HourlyPattern"]["ActivityLevel_mean"]["7"],
                    '8': parameters["HourlyPattern"]["ActivityLevel_mean"]["8"],
                    '9': parameters["HourlyPattern"]["ActivityLevel_mean"]["9"],
                    '10': parameters["HourlyPattern"]["ActivityLevel_mean"]["10"],
                    '11': parameters["HourlyPattern"]["ActivityLevel_mean"]["11"],
                    '12': parameters["HourlyPattern"]["ActivityLevel_mean"]["12"],
                    '13': parameters["HourlyPattern"]["ActivityLevel_mean"]["13"],
                    '14': parameters["HourlyPattern"]["ActivityLevel_mean"]["14"],
                    '15': parameters["HourlyPattern"]["ActivityLevel_mean"]["15"],
                    '16': parameters["HourlyPattern"]["ActivityLevel_mean"]["16"],
                    '17': parameters["HourlyPattern"]["ActivityLevel_mean"]["17"],
                    '18': parameters["HourlyPattern"]["ActivityLevel_mean"]["18"],
                    '19': parameters["HourlyPattern"]["ActivityLevel_mean"]["19"],
                    '20': parameters["HourlyPattern"]["ActivityLevel_mean"]["20"],
                    '21': parameters["HourlyPattern"]["ActivityLevel_mean"]["21"],
                    '22': parameters["HourlyPattern"]["ActivityLevel_mean"]["22"],
                    '23': parameters["HourlyPattern"]["ActivityLevel_mean"]["23"]}

                self.Hourly_ActivityLevel_std = {
                    '0': parameters["HourlyPattern"]["ActivityLevel_std"]["0"],
                    '1': parameters["HourlyPattern"]["ActivityLevel_std"]["1"],
                    '2': parameters["HourlyPattern"]["ActivityLevel_std"]["2"],
                    '3': parameters["HourlyPattern"]["ActivityLevel_std"]["3"],
                    '4': parameters["HourlyPattern"]["ActivityLevel_std"]["4"],
                    '5': parameters["HourlyPattern"]["ActivityLevel_std"]["5"],
                    '6': parameters["HourlyPattern"]["ActivityLevel_std"]["6"],
                    '7': parameters["HourlyPattern"]["ActivityLevel_std"]["7"],
                    '8': parameters["HourlyPattern"]["ActivityLevel_std"]["8"],
                    '9': parameters["HourlyPattern"]["ActivityLevel_std"]["9"],
                    '10': parameters["HourlyPattern"]["ActivityLevel_std"]["10"],
                    '11': parameters["HourlyPattern"]["ActivityLevel_std"]["11"],
                    '12': parameters["HourlyPattern"]["ActivityLevel_std"]["12"],
                    '13': parameters["HourlyPattern"]["ActivityLevel_std"]["13"],
                    '14': parameters["HourlyPattern"]["ActivityLevel_std"]["14"],
                    '15': parameters["HourlyPattern"]["ActivityLevel_std"]["15"],
                    '16': parameters["HourlyPattern"]["ActivityLevel_std"]["16"],
                    '17': parameters["HourlyPattern"]["ActivityLevel_std"]["17"],
                    '18': parameters["HourlyPattern"]["ActivityLevel_std"]["18"],
                    '19': parameters["HourlyPattern"]["ActivityLevel_std"]["19"],
                    '20': parameters["HourlyPattern"]["ActivityLevel_std"]["20"],
                    '21': parameters["HourlyPattern"]["ActivityLevel_std"]["21"],
                    '22': parameters["HourlyPattern"]["ActivityLevel_std"]["22"],
                    '23': parameters["HourlyPattern"]["ActivityLevel_std"]["23"]}

                self.Physical_male_height = {
                    '5': parameters["PhysicalModel"]["male"]["5"]["height"],
                    '10': parameters["PhysicalModel"]["male"]["10"]["height"],
                    '15': parameters["PhysicalModel"]["male"]["15"]["height"],
                    '20': parameters["PhysicalModel"]["male"]["20"]["height"],
                    '30': parameters["PhysicalModel"]["male"]["30"]["height"],
                    '40': parameters["PhysicalModel"]["male"]["40"]["height"],
                    '50': parameters["PhysicalModel"]["male"]["50"]["height"],
                    '60': parameters["PhysicalModel"]["male"]["60"]["height"],
                    '70': parameters["PhysicalModel"]["male"]["70"]["height"],
                    '100': parameters["PhysicalModel"]["male"]["100"]["height"]}

                self.Physical_male_weight = {
                    '5': parameters["PhysicalModel"]["male"]["5"]["weight"],
                    '10': parameters["PhysicalModel"]["male"]["10"]["weight"],
                    '15': parameters["PhysicalModel"]["male"]["15"]["weight"],
                    '20': parameters["PhysicalModel"]["male"]["20"]["weight"],
                    '30': parameters["PhysicalModel"]["male"]["30"]["weight"],
                    '40': parameters["PhysicalModel"]["male"]["40"]["weight"],
                    '50': parameters["PhysicalModel"]["male"]["50"]["weight"],
                    '60': parameters["PhysicalModel"]["male"]["60"]["weight"],
                    '70': parameters["PhysicalModel"]["male"]["70"]["weight"],
                    '100': parameters["PhysicalModel"]["male"]["100"]["weight"]}

                self.Physical_female_height = {
                    '5': parameters["PhysicalModel"]["female"]["5"]["height"],
                    '10': parameters["PhysicalModel"]["female"]["10"]["height"],
                    '15': parameters["PhysicalModel"]["female"]["15"]["height"],
                    '20': parameters["PhysicalModel"]["female"]["20"]["height"],
                    '30': parameters["PhysicalModel"]["female"]["30"]["height"],
                    '40': parameters["PhysicalModel"]["female"]["40"]["height"],
                    '50': parameters["PhysicalModel"]["female"]["50"]["height"],
                    '60': parameters["PhysicalModel"]["female"]["60"]["height"],
                    '70': parameters["PhysicalModel"]["female"]["70"]["height"],
                    '100': parameters["PhysicalModel"]["female"]["100"]["height"]}

                self.Physical_female_weight = {
                    '5': parameters["PhysicalModel"]["female"]["5"]["weight"],
                    '10': parameters["PhysicalModel"]["female"]["10"]["weight"],
                    '15': parameters["PhysicalModel"]["female"]["15"]["weight"],
                    '20': parameters["PhysicalModel"]["female"]["20"]["weight"],
                    '30': parameters["PhysicalModel"]["female"]["30"]["weight"],
                    '40': parameters["PhysicalModel"]["female"]["40"]["weight"],
                    '50': parameters["PhysicalModel"]["female"]["50"]["weight"],
                    '60': parameters["PhysicalModel"]["female"]["60"]["weight"],
                    '70': parameters["PhysicalModel"]["female"]["70"]["weight"],
                    '100': parameters["PhysicalModel"]["female"]["100"]["weight"]}

            except ValueError:
                print('error extracting and initializing occupancy model parameters!')

    def get_a_swimmer_from_model(self, date_time, time_step_seconds):
        """
        This function provides distribution parameters of inter-arrival rate, weight, height, age, gender, and staying
        time of swimmers based on the given date_time specified as the input argument of the function
        :param date_time:
        :param time_step_seconds: time step between samples per seconds
        :return:
        """
        if type(date_time) is not datetime.datetime:
            raise TypeError('arg must be a datetime.datetime, not a %s' % type(date_time))

        dt_day_of_week = date_time.strftime('%A')
        dt_hour = "{}".format(date_time.hour)
        dt_month = date_time.strftime("%B")

        inter_arrival_time_mean = self.Monthly_InterArrivalTime_Seconds_Mean[dt_month] / \
                                  self.WeekDaily_InterArrivalTime_Divider[dt_day_of_week] / \
                                  self.Hourly_InterArrivalRate_Divider[dt_hour]

        inter_arrival_time_std = self.Monthly_InterArrivalRate_Seconds_Std[dt_month]

        inter_arrival_time = random.normalvariate(inter_arrival_time_mean, inter_arrival_time_std)

        time_to_arrival = random.expovariate(1 / inter_arrival_time)

        gender_ismale_probability = self.Monthly_Gender_Male_Probability[dt_month] * \
                                    self.WeekDaily_Gender_Multiplier[dt_day_of_week] * \
                                    self.Hourly_Gender_Multiplier[dt_hour]

        gender = 'male' if random.random() < gender_ismale_probability else 'female'

        probability_adult = self.Hourly_ProbabilityAdult[dt_hour]

        age = 1

        if random.random() < self.Hourly_ProbabilityAdult[dt_hour]:
            age_mean = self.Monthly_Age_High_Distribution_Mean[dt_month] * self.WeekDaily_AgeHigh_Multiplier[dt_day_of_week] * self.Hourly_AgeHigh_Multiplier[dt_hour]
            age_std = self.Monthly_Age_High_Distribution_Std[dt_month]
            age = random.normalvariate(age_mean, age_std)
        else:
            age_mean = self.Monthly_Age_Low_Distribution_Mean[dt_month] * self.WeekDaily_AgeLow_Multiplier[dt_day_of_week] * self.Hourly_AgeLow_Multiplier[dt_hour]
            age_std = self.Monthly_Age_Low_Distribution_Std[dt_month]
            age = random.normalvariate(age_mean, age_std)

        age = max(1, min(100, age))

        min_age_range = 100
        sel_age_key = '100'
        for age_range in self.Physical_female_weight.keys():
            if int(age_range) > age:
                if min_age_range > int(age_range):
                    min_age_range = int(age_range)
                    sel_age_key = age_range

        weight = 0
        height = 0

        if gender == 'male':
            weight = self.Physical_male_weight[sel_age_key]
            height = self.Physical_male_height[sel_age_key]
        else:
            weight = self.Physical_female_weight[sel_age_key]
            height = self.Physical_female_height[sel_age_key]

        time_of_stay_seconds = random.normalvariate(self.Hourly_TimeOfStay_Minutes_mean[dt_hour] * 60,
                                                    self.Hourly_TimeOfStay_Minutes_std[dt_hour] * 60)

        datetime_arrival = date_time + datetime.timedelta(seconds=int(time_to_arrival))
        datetime_leave = date_time + datetime.timedelta(seconds=int(time_to_arrival + time_of_stay_seconds))

        als = []

        for n, dt in enumerate(utils.dates_bwn_two_date_times_generator(datetime_arrival, datetime_leave,
                                                                        time_step_seconds)):
            als.append(np.max([0, np.min([1, random.normalvariate(self.Hourly_ActivityLevel_mean[dt_hour],
                                                                  self.Hourly_ActivityLevel_std[dt_hour])])]) * 100.0)

        return int(time_to_arrival), gender, int(age), weight, height, int(time_of_stay_seconds), als
