import json
import numpy as np
# Water Temp: 28
# Lambda = 0.1 {'cost': 1130.5307547912814, 'water_use': 1014.4913956197322, 'health_cost': 1160.3935917154927, 'g_l': 2, 'g_m': 20, 'g_h': 130}
# Lambda = 1.0 {'cost': 1203.040897787921, 'water_use': 1198.3194266608537, 'health_cost': 4.721471127067363, 'g_l': 4, 'g_m': 20, 'g_h': 158}
# Lambda = 10.0 {'cost': 1209.8972370594106, 'water_use': 1208.5131999999896, 'health_cost': 0.13840370594209736, 'g_l': 4, 'g_m': 22, 'g_h': 156}
# Water Temp: 29
# Lambda = 0.1
# Lambda = 1.0 {'cost': 1270.7178261033218, 'water_use': 1266.8580000000647, 'health_cost': 3.859826103257095, 'g_l': 18, 'g_m': 30, 'g_h': 130}
# Lambda = 10.0 {'cost': 1276.3194852495699, 'water_use': 1274.4623980976244, 'health_cost': 0.18570871519455145, 'g_l': 21, 'g_m': 26, 'g_h': 136}
# Lambda = 100.0 {'cost': 1212.7778829323108, 'water_use': 1210.2642266609591, 'health_cost': 0.025136562713516993, 'g_l': 4, 'g_m': 20, 'g_h': 160}
def find_costs_from_json(data, il, im, ih, lambda_water_quality=1):
    time_step_seconds = 360
    time_adj = 60 * 60 / time_step_seconds
    sel_vals = []
    sum_dists = 0
    for d in data:
        l = d["gamma_l"]
        m = d["gamma_m"]
        h = d["gamma_h"]
        dist = ((l-il)**2 + (m-im)**2 + (h-ih)**2)**0.5
        if dist <= 3:
            sel_vals.append({"dist": dist, "water_use": d["water use"], "health_cost": d["health_cost"] / time_adj})

    if len(sel_vals) == 0:
        return 0, 0, 0

    water_use = 0
    health_cost = 0
    sum_score = 0

    for d in sel_vals:
        score = np.exp(-2 * d["dist"]**2)
        water_use += d["water_use"] * score
        health_cost += d["health_cost"] * score
        sum_score += score

    water_use /= sum_score
    health_cost /= sum_score

    return water_use, health_cost, water_use + lambda_water_quality * health_cost


min_l = 2
max_l = 22

min_m = 20
max_m = 82

min_h = 100
max_h = 182

lambda_water_quality = 10.0

min_cost = 10000
selected_params = []
with open("data_T28C_20220807.json", "r") as i:
    data = json.load(i)
    for g_l in np.arange(start=min_l, stop=max_l, step=1):
        print('start for g_l:{}'.format(g_l))
        for g_m in np.arange(start=min_m, stop=max_m, step=1):
            print('start for g_l:{}'.format(g_m))
            costs_hist = []
            for g_h in np.arange(start=min_h, stop=max_h, step=1):
                if g_l < g_m < g_h:
                    water_use, health_cost, cost = find_costs_from_json(data, g_l, g_m, g_h, lambda_water_quality)
                    costs_hist.append(cost)
                    if len(costs_hist) > 5:
                       if  costs_hist[-1] > costs_hist[-2] and costs_hist[-2] > costs_hist[-3] and \
                               costs_hist[-3] > costs_hist[-4] and costs_hist[-4] > costs_hist[-5]:
                           break
                    if water_use == 0:
                        #print({"g_l": g_l, "g_m": g_m, "g_h": g_h,"Failed":True})
                        continue
                    if cost < min_cost:
                        min_cost = cost
                        selected_params = {"cost": cost, "water_use": water_use, "health_cost": health_cost,
                                           "g_l": g_l, "g_m": g_m, "g_h": g_h}
                        print(selected_params)

print("Selected Parameters:{}".format(selected_params))
