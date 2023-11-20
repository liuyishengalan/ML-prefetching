PAGE_SIZE=4096
# Class represents timestamp objects in seconds.nanoseconds
class Timestamp(object):
    def __init__(self, time_string):
        # TODO: add wrong input validation.
        self.sec = int(time_string.split('.')[0])
        self.ns = int(time_string.split('.')[-1])
    # Method to compare two timestamps.
    def __lt__(self, other):
        return ((self.sec < other.sec) or (self.sec == other.sec and self.ns < other.ns))


# Convert hex string addr to page addr
def convert_addr_to_page(addr):
    memory_address = int(addr, 16)
    page_address = memory_address & ~(PAGE_SIZE - 1)
    return page_address

memory_access = None
pagefault = None
unique_pagefaults = set()
prev_addr = None
with open('../../traces/raw_traces/mcf-perf.log') as perf:
    #if memory_access is None:
    #    memory_access = pin.readline()
    pagefault = perf.readline()
    while pagefault:
        pagefault = perf.readline()
        if "mcf" not in pagefault:
            continue
        # Decide how to handle memory accesses.
        # Read pagefaults into a file and write 0 PC to it.
        pc=0
        try:
            page_address = pagefault.split()[6][6:]
            unique_pagefaults.add(page_address)
        except IndexError:
            print("Error:", pagefault)

        with open("../../traces/final_traces/page.txt", "a") as file:
            try:
                file.write((hex(0) + " " + hex(int(page_address , 16)) + "\n"))
            except:
                print("Exception", pagefault)

    print("Unique pages: ", len(unique_pagefaults))
