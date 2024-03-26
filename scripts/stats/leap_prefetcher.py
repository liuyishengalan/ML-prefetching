# This script runs the leap prefetcher on 
# a trace. 

from pandas import *

trace_file = read_csv("../../traces/final_traces/trace-omnetpp-filtered.csv")
#traces = trace_file.readlines()

# Function to find majority element
def findMajority(arr, n):
    candidate = -1
    votes = 0

    # Finding majority candidate
    for i in range (n):
        if (votes == 0):
            candidate = arr[i]
            votes = 1
        else:
            if (arr[i] == candidate):
                votes += 1
            else:
                votes -= 1
    count = 0

    # Checking if majority candidate occurs more than n/2
    # times
    for i in range (n):
        if (arr[i] == candidate):
            count += 1
    
    if (count > n // 2):
        return candidate
    else:
        return -1


count = 0
predicted = 0
not_predicted = 0
while count + 32 < len(trace_file):
    deltas = trace_file['delta_in'][count: count + 32].tolist()
    candidate = findMajority(deltas, 32)
    delta = trace_file['delta_in'][count+32]
    if delta == candidate:
        predicted += 1
    else:
        not_predicted += 1
    count += 1

print("Predicted by Leap: ", predicted)
print("Not predicted by Leap: ", not_predicted)
