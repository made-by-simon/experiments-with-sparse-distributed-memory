# Experiments with Sparse Distributed Memory

This notebook explores Sparse Distributed Memory (SDM) through various experiments. Core functionality is provided by the `KanervaSDM` module, developed from Pentti Kanerva's 1992 work *Sparse Distributed Memory and Related Models*. The `KanervaSDM` module operates on binary address and memory vectors, and provides a low-level foundation for more sophisticated implementations. This notebook assumes a familiarity with vector and matrix operations, and of course a basic understanding of Sparse Distributed Memory. 

Sparse Distributed Memory (SDM) is an associative (distributed) memory model inspired by human longterm memory that stores information across distributed hard locations in a high-dimensional (sparse) binary space. When storing a memory, the address vector activates hard locations within a certain Hamming distance threshold, and the memory vector is written to the locations at those activated locations. During retrieval, the same address (or a similiar address) reactivates similar hard locations, and the stored memory is reconstructed by summing and thresholding the location values across activated locations. SDM exhibits unique behaviour allowing new memories to either reinforce prior memories or cause them to be forgotten. 

The experiments in this notebook will generally set the address and memory dimensions to be equal and refer to both as simply "dimension", however the `KanervaSDM` module does allow them to be different. Also, SDM of dimension 100 with 10,000 hard locations, and an activation threshold of 37 will be considered the "standard" configuration, as it offers a balance of memory performance and computational speed to make the experiments in this notebook practical.

© 2025 Simon Wong

**Table of Contents**

- 1.0 SDM experiments with address and memory vectors that are different
    - 1.1 Storing and recalling a single memory, then calculating error
    - 1.2 Storing and recalling multiple memories, then calculating error after all memories have been stored
    - 1.3 Storing and recalling multiple memories, calculating error after each new memory is stored
    - 1.4 Varying dimension 
    - 1.5 Varying activation threshold
    - 1.6 Varying number of hard locations 
- 2.0 SDM experiments with address and memory vectors that are the same 
    - 2.1 Storing and recalling a single memory, then calculating error
    - 2.2 Storing and recalling multiple memories, then calculating error after all memories have been stored
    - 2.3 Storing and recalling multiple memories, calculating error after each new memory is stored
    - 2.4 Varying dimension 
    - 2.5 Varying activation threshold
    - 2.6 Varying number of hard locations 
- 3.0 Experiments with visualizing SDM
    - 3.1 Address and memory vectors that are different and both random
    - 3.2 Address and memory vectors that are the same and both random
    - 3.3 Address and memory vectors that are different, with random addresses and non-random memories
    - 3.4 Adddess and memory vectors that are different, with non-random andresses and random memories
    - 3.5 Address and memory vectors that are the same and both non-random
- 4.0 Other Experiments with SDM
    - 4.1 Chaining addresses and memories
    - 4.2 Storing images in SDM and adding random memories
    - 4.3 Storing images in SDM and corrupting the memory addresses
    - 4.4 Storing images in SDM, adding random memories, and corrupting the memory addresses

***