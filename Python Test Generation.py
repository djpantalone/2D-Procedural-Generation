import numpy as np
import matplotlib.pyplot as plt
import random 
from noise import snoise2


#Function to generate Perlin noise (taken from first gen attempt)
def generate_perlin_noise(size, scale, octaves, persistence, lacunarity, seed):
    noise_map = np.zeros(size)
    for x in range(size[0]):
        for y in range(size[1]):
            #Calc the Perlin noise value for the current x,y coordinate
            noise_map[x][y] = snoise2(x / scale,
                                      y / scale,
                                      octaves=octaves,
                                      persistence=persistence,
                                      lacunarity=lacunarity,
                                      base=seed)
    return noise_map

#Function to gen random terrain with Perlin noise
def generate_terrain(size, iterations, noise_scale, octaves, persistence, lacunarity, seed):
    terrain = np.random.rand(size, size)
    
    #Gen Perlin noise w/ specified parameters
    noise = generate_perlin_noise((size, size), noise_scale, octaves, persistence, lacunarity, seed)
    
    for _ in range(iterations):
        #Calculate midpoints in the x and y directions
        midpoints_x = (terrain[0:size-1:2, 0:size-1:2] + terrain[0:size-1:2, 1:size:2]) / 2 #Incorperates essential Diamond-Square alg. components
        midpoints_y = (terrain[0:size-1:2, 0:size-1:2] + terrain[1:size:2, 0:size-1:2]) / 2
        terrain[1:size:2, 1:size:2] = (midpoints_x + midpoints_y) / 2 #Update terrain vals w/ average midpoint
        
        terrain += noise[0:size, 0:size] * (size / (2 ** _)) #Adds perlin noise to terrain

    #Limit the maximum height by scaling down the terrain values 
    #(lower value = less likely to see snow-tipped mountains)
    terrain = terrain * 0.13

    return terrain

#Define the size and number of iterations
size = 1025  #Should be a power of 2 plus 1. This ensures compatability w/ Diamond-Square alg.
iterations = 20 #Each itteration refined terrain further

# Perlin noise parameters
noise_scale = 1025.0 #Scale Perlin noise. Larger value = larger features
octaves = 8 #Level of detail in perlin noise
persistence = 0.65 #How much each octave contributes. Smaller val = smoother terrain, larger val = more ruggedness
lacunarity = 2.0 #Detail added or removed at each octive. Increasing val increases contrast between high and low terrain
seed = random.randint(1, 1000) #Chooses a random seed between 1 and 1000

#Generate terrain with Perlin noise
terrain = generate_terrain(size, iterations, noise_scale, octaves, persistence, lacunarity, seed)

#Pixelate terrain output
plt.figure(figsize=(8, 8))
plt.imshow(terrain, cmap='terrain', interpolation='nearest', vmin=-150, vmax=150) #vmin and vmax can be adjusted, these are the best vals I found to show all color elevation
plt.colorbar()
plt.title(f"DJ's Procedurally Generated Terrain with Perlin Noise ({size}x{size})")
plt.xticks([])  #Hide x-axis labels (useless)
plt.yticks([])  #Hide y-axis labels (useless)
plt.show()
