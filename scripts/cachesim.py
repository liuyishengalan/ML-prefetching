from cachetools import LRUCache

class MultiLevelCacheSimulator:
    def __init__(self, configurations):
        """
        Initializes multi-level caches based on configurations.
        configurations: A list of tuples (cache_size, block_size) for each level.
        """
        self.levels = [LRUCache(maxsize=conf[0] // conf[1]) for conf in configurations]
        self.hits = [0] * len(configurations)
        self.misses = [0] * len(configurations)
    
    def access_memory(self, address, level=0):
        if level >= len(self.levels):
            # Miss in all levels
            #print(f"Miss at all levels for address {address}")
            # Load into all caches (simplified model)
            for i in range(len(self.levels)):
                self.levels[i][address] = True
                self.misses[i] += 1
            return False

        cache = self.levels[level]
        if address in cache:
            # Hit
            self.hits[level] += 1
            return True
            #print(f"Hit at Level {level+1} for address {address}")
        else:
            # Miss at this level, try next level
            self.misses[level] += 1
            #print(f"Miss at Level {level+1} for address {address}")
            self.access_memory(address, level+1)

    def simulate(self, trace_file_path):
        with open(trace_file_path, 'r') as file, open('miss_trace.out', 'w') as out:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) == 3:
                        _, _, address = parts
                        isHit = self.access_memory(address)
                        if not isHit:
                           out.write(line)
    
    def report(self):
        for i, (hits, misses) in enumerate(zip(self.hits, self.misses)):
            print(f"Level {i+1}: Hits: {hits}, Misses: {misses}")

# Emulatiing Intel Broadwell Processor
configurations = [
    (32*1024, 64),  # Level 1 cache: size 32KB, block size 64 bytes
    (256*1024, 64),   # Level 2 cache: size 256KB, block size 64 bytes
    (1280*1024,64)   # Level 3 cache (LLC): size 1.25 MB 
]
simulator = MultiLevelCacheSimulator(configurations)
simulator.simulate('pinatrace.out')
