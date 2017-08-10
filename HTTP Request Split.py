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

def DictToLists (headers):
    """
    Transform list of dictionaries (of which the values are lists), to a list of lists
    """
    header_list = []
    for dict in headers:
        request_list = []
        for key in dict:
            request_list.append(dict[key])
        header_list.append(request_list)

    return header_list

def NeuralNetwork (input1, input2):
    """
    :param input1: Normalized & Padded list of lists; NORMAL EXAMPLES
    :param input2: Normalized & Padded list of lists; ABNORMAL EXAMPLES
    :return: ANN output will be 0 if normal, 1 if abnormal
    """
    import numpy as np

    def nonlin (x, deriv = False):
        """
        sigmoid function 
        """
        if deriv == True:
            return x*(1-x)
        return 1/(1+np.exp(-x))

    #defining all inputs
    input1.append(input2)
    X = np.array(input1)
    #defining outputs for 1
    output1 = []
    for i in range (len(input1)):
        output1.append(0)
    #defining outputs for 2
    output2 = []
    for i in range(len(input2)):
        output2.append(1)
    #defining all outputs
    merge = output1 + output2
    y = []
    y.append(merge)
    Y = np.array(y).T

    #seed random; DETERMINISTIC
    np.random.seed(1)

    #initialize weights with mean 0
    syn0 = 2*np.random.random((3,1)) - 1

    print(X)

    for iteration in xrange(10):
        #forward propogation
        l0 = X
        l1 = nonlin(np.dot(l0, syn0))

        l1_error = y - l1

        l1_delta = l1_error * nonlin(l1, True)

        #update weights
        syn0 += np.dot(l0.T, l1_delta)

    return l1

norm = DictToLists(Pad(Normalize(Parse('normal traffic.txt'))))
abnorm = DictToLists(Pad(Normalize(Parse('abnormal traffic.txt'))))

NeuralNetwork(norm, abnorm)