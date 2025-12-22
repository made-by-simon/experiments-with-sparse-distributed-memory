"""
Sparse Distributed Memory implementation based on Kanerva (1992).

This module implements the fundamental operations of Kanerva's Sparse Distributed
Memory (SDM) model, including writing, reading, and erasing memories using 
Hamming distance activation.

Reference:
    Pentti Kanerva (1992). Sparse Distributed Memory and Related Models.
"""

import numpy as np 

class KanervaSDM: 
    """
    This class provides fundamental SDM functionality for storing and recalling memories. 
    Single letters in parentheses (e.g., (M) for number of locations) indicate notation from Kanerva's original work. 

    """

    def __init__(self, 
                 address_dimension: int, 
                 memory_dimension: int, 
                 num_locations: int, 
                 activation_threshold: int, 
                 random_seed:int = 42
                 ) -> None:
        """
        Initializes the Kanerva SDM.

        Args:
            address_dimension: Length of address vectors (N).
            memory_dimension: Length of memory vectors (U).
            num_locations: Number of hard locations (M).
            activation_threshold: Hamming distance threshold for activation (H).
            random_seed: Seed for reproducible random generation of hard locations. 

        Raises:
            ValueError: If any dimension or threshold is non-positive.
        """
        if address_dimension <= 0 or memory_dimension <= 0 or num_locations <= 0:
            raise ValueError("All dimensions must be positive integers.")
        if activation_threshold < 0:
            raise ValueError("Activation threshold must be non-negative.")
        
        self.address_dimension = int(address_dimension)  # Length of addresses (N). 
        self.memory_dimension = int(memory_dimension)  # Length of memories (U). 
        self.num_locations = int(num_locations)  # Number of locations (M). 
        self.activation_threshold = int(activation_threshold)  # Hamming activation threshold (H). 
        
        rng = np.random.default_rng(random_seed)

        self.address_matrix = rng.integers(
            0, 2, 
            size=(self.num_locations, self.address_dimension), 
            dtype=np.int8
        )

        self.memory_matrix = np.zeros(
            (self.num_locations, self.memory_dimension), 
            dtype=np.float32)  
        
        self.memory_count = 0  # Number of stored memories (T).
       
    def _get_activated_locations(self, address: np.ndarray) -> np.ndarray:
        """
        Finds activated locations based on Hamming distance threshold (H). 

        Args:
            address: Target address vector (x) of shape (address_dimension,).

        Returns:
            Array of indices for activated locations (y).

        Raises:
            ValueError: If address shape doesn't match address_dimension.
        """
        hamming_distances = np.count_nonzero(self.address_matrix != address, axis=1)  # Vectorized Hamming distance. 
        return np.where(hamming_distances <= self.activation_threshold)[0] 

    def write(self, address: np.ndarray, memory: np.ndarray) -> None: 
        """
        Writes a memory to an address. 

        Args:
            address: Target address vector (x) of shape (address_dimension,).
            memory: Memory vector (w) of shape (memory_dimension,). 

        Raises:
            ValueError: If address or memory dimensions are incorrect.
        """
        if memory.shape != (self.memory_dimension,):
            raise ValueError(
                f"Memory shape {memory.shape} doesn't match "
                f"expected ({self.memory_dimension},)"
            )
        
        activated_locations = self._get_activated_locations(address)  # Activation vector (y). 
        polar_memory = 2 * memory - 1  # Convert memory (0 and 1) to polar memory (-1 and +1). 
        self.memory_matrix[activated_locations] += polar_memory  # Add or subtract one to activated locations in memory matrix (C). 
        self.memory_count += 1  # Increment number of stored memories (T). 

    def read(self, address: np.ndarray) -> np.ndarray: 
        """
        Reads a memory from an address. 

        Args:
            address: Target address vector (x) of shape (address_dimension,).

        Returns:
            Recalled memory vector (z) of shape (memory_dimension,).
            Returns all zeros if no locations are activated.

        Raises:
            ValueError: If address dimension is incorrect.
        """
        activated_locations = self._get_activated_locations(address)  # Activation vector (y). 
        if len(activated_locations) == 0: 
            return np.zeros(self.memory_dimension, dtype=np.uint8)
        locations_sum = self.memory_matrix[activated_locations].sum(axis=0)  # Sum all activated locations in memory matrix (s).  
        return (locations_sum >= 0).astype(np.int8)  # Memory vector (z) is binary vector of all location sum entries that are greater than zero. 
    
    def erase_memory(self) -> None: 
        """
        Erases memory matrix (C), but NOT address matrix (A), 
        so locations are preserved. 
        """
        self.memory_matrix.fill(0)
        self.memory_count = 0 