ascii_dict = dict()
for i in range(0,256):
    ascii_dict[chr(i)] = str(i)

def Parse (file_name):
    """
    Will parse HTTP request file with labels "Normal"/"Abnormal" at the end into header sections/variables
    :param file_name: 
    :return: [{header 1: value, header 2: value}, {header 1: value, header 2: value}]
    """

    f = open(file_name, 'r')

    requests = []

    for line in f:
        if len(line) > 1:
            # print(line)
            headers = {}
            words = line.split()
            # print(words)
            if words[0] == 'POST' or words[0] == 'GET':
                # print('words =', words)
                if words[0] == 'POST':
                    headers['URI'] = words[1]
                else:
                    headers['URI'] = words[1][1:]
                headers['Host'] = words[3][0:13]
                headers['User Agent'] = line[(line.find('User-Agent:') + 12):line.find('Accept:')]
                headers['Accept'] = line[(line.find('Accept:') + 8):line.find('Accept-Language:')]
                headers['Accept Language'] = line[(line.find('Accept-Language:') + 17):line.find('Accept-Encoding:')]
                headers['Accept Encoding'] = line[(line.find('Accept-Encoding:') + 17):line.find('DNT:')]
            requests.append(headers)

    return (requests)

def Normalize (headers):
    """
    :param headers: a list of dictionaries mapping each header to its information, with each dictionary representating an HTTP request
    :return: The same list with the information normalized to ASCII character assignments [0:1]
    """
    for dict in headers:
        for key in dict:
            normalized = []
            for i in range(len(dict[key])):
                normalized.append(float(ascii_dict[dict[key][i]])/255.0)
            dict[key] = normalized

    return headers


def Pad (headers):
    """
    :param norm_headers: normalized headers; list of dictionaries
    :return: The same list with every header having a vlaue of 1000 characters long (len(list) = 1000)
    """
    for dict in headers:
        for key in dict:
            # print(dict[key])
            for i in range (1000 - len(dict[key])):
                dict[key].append(0)
    return headers

(Pad(Normalize(Parse('normal traffic.txt'))))