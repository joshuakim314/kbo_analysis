def convert_ip_to_float(ip):
    ip_string = str(ip).split()
    if len(ip_string) == 1:
        return int(ip)
    ip_fraction = ip_string[1].split('/')
    return float(ip_string[0]) + float(ip_fraction[0])/float(ip_fraction[1])


def sort_team_data(data):
    sorted_data = data[:]
    for i in range(len(sorted_data) - 1):
        for j in range(len(sorted_data) - i - 1):
            if sorted_data[j][0] > sorted_data[j + 1][0]:
                sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
    return sorted_data


def format_num_data(data):
    try:
        data = int(data)
    except:
        pass
    try:
        data = float(data)
    except:
        pass
    return data
