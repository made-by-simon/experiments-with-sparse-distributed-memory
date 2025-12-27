from KanervaSDM import KanervaSDM
import numpy as np
import time 
from tqdm import tqdm
import os

SDM = KanervaSDM(
    address_dimension=100,
    memory_dimension=100, 
    num_locations=10000, 
    activation_threshold=37
)

num_memories = 10000

# Create arrays for storing addresses and memories. 
addresses = np.empty((num_memories, SDM.address_dimension))
memories = np.empty((num_memories, SDM.memory_dimension))
recalled_memories = np.empty((num_memories, SDM.memory_dimension))
errors = np.empty(num_memories)

# Write all memories. 
start = time.time()
for i in tqdm(range(num_memories)): 
    address = np.random.randint(0, 2, SDM.address_dimension)
    memory = np.random.randint(0, 2, SDM.memory_dimension)
    addresses[i] = address
    memories[i] = memory
    SDM.write(address, memory)
    
# Read all memories.  
for i in tqdm(range(num_memories)): 
    address = addresses[i]
    recalled_memory = SDM.read(address)
    recalled_memories[i] = recalled_memory

end = time.time()

time.sleep(0.1)
os.system('cls' if os.name == 'nt' else 'clear')
print(f"\n\n\n\n\nElapsed time: {end-start:.5f}s\n\n\n\n\n")