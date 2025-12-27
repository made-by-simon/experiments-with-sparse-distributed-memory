#include "kanerva_sdm.h"
#include <iostream>
#include <iomanip>
#include <vector>
#include <random>
#include <chrono>

// Helper function to generate random binary vector.
std::vector<int> generate_random_vector(int size, std::mt19937& rng) {
    std::uniform_int_distribution<int> dist(0, 1);
    
    std::vector<int> vec(size);
    for (int i = 0; i < size; ++i) {
        vec[i] = dist(rng);
    }
    return vec;
}

int main() {
    KanervaSDM sdm(100, 100, 10000, 37);
    
    const int num_memories = 10000;
    std::mt19937 rng(42);
    
    // Create vectors for storing addresses and memories.
    std::vector<std::vector<int>> addresses(num_memories);
    std::vector<std::vector<int>> memories(num_memories);
    std::vector<std::vector<int>> recalled_memories(num_memories);
    
    // Start timing
    auto start = std::chrono::high_resolution_clock::now();
    
    // Write all memories.
    for (int i = 0; i < num_memories; ++i) {
        std::vector<int> address = generate_random_vector(sdm.get_address_dimension(), rng);
        std::vector<int> memory = generate_random_vector(sdm.get_memory_dimension(), rng);
        addresses[i] = address;
        memories[i] = memory;
        sdm.write(address, memory);
    }
    
    // Read all memories.
    for (int i = 0; i < num_memories; ++i) {
        std::vector<int> address = addresses[i];
        std::vector<int> recalled_memory = sdm.read(address);
        recalled_memories[i] = recalled_memory;
    }
    
    // End timing
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << std::fixed << std::setprecision(5);
    std::cout << "Elapsed time: " << duration.count() / 1000000.0 << "s" << std::endl;
    std::cout.flush();  // Force flush
    
    std::cout << "\nPress Enter to exit..." << std::endl;
    std::cin.get();
    
    return 0;
}