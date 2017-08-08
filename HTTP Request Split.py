def Parse (file_name):
    """
    Will parse HTTP request file with labels "Normal"/"Abnormal" at the end into header sections/variables
    :param file_name: 
    :return: [{header 1: value, header 2: value}, {header 1: value, header 2: value}]
    """

    f = open(file_name, 'r')

    requests = []

    for line in f:
        if len(line) > 0:
            # print(line)
            headers = {}
            words = line.split()
            print(words)
            if words[0] == 'POST' or words[0] == 'GET':
                # print('words =', words)
                if words[0] == 'POST':
                    headers['URI'] = words[1]
                else:
                    headers['URI'] = words[1][1,]

            requests.append(headers)

    return (requests)

(Parse('normal traffic.txt'))