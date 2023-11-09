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

memory_access = None
pagefault = None

prev_addr = None
starting_heap_addr=0
end_heap_addr=0


# Convert hex string addr to page addr
def convert_addr_to_page(addr):
    memory_address = int(addr, 16)
    page_address = memory_address & ~(PAGE_SIZE - 1)
    return page_address

def get_start_and_end_heap_addr(heap_range):
    global starting_heap_addr
    global end_heap_addr
    addresses = heap_range.split('-')
    starting_heap_addr = int(addresses[0], 16)
    end_heap_addr = int(addresses[1], 16)

with open('omnetpp_map') as mapped_ranges:
    mapped_addresses = mapped_ranges.readline()
    while mapped_addresses:
        if "heap" in mapped_addresses:
            heap_range = mapped_addresses.split()[0]
            print(heap_range)
            get_start_and_end_heap_addr(heap_range)
        mapped_addresses = mapped_ranges.readline()

starting_heap_addr = int("560ffc33e000" ,16)
end_heap_addr = starting_heap_addr + 5242880
with open('omnetpp-perf.log') as perf:
    #if memory_access is None:
    #    memory_access = pin.readline()
    pagefault = perf.readline()
    while pagefault:
        pagefault = perf.readline()
        if "omnetpp" not in pagefault:
            continue
       
        # Decide how to handle memory accesses.
        # Read pagefaults into a file and write 0 PC to it.
        pc=0
        try:
            page_address = int(pagefault.split()[6][6:] ,16)
            if page_address < starting_heap_addr or page_address > end_heap_addr:
                #print("Starting: ", page_address - starting_heap_addr)
                #print("Ending: ", page_address - end_heap_addr)
                continue
        except IndexError:
            print("Error:", pagefault)

        with open("page.txt", "a") as file:
            try:
                file.write((hex(0) + " " + hex(page_address) + "\n"))
            except:
                print("Exception", pagefault)
