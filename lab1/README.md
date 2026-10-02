# Lab 1 — K-Means Parallelization in Python

K-Means clustering (on `enzyme` and `hydrofob`) over a synthetic proteins dataset, in serial, `multiprocessing` and `threading` versions, comparing execution times and speedup.


## Usage

```bash
python proteins-generator.py 50000 <seed>   # generates proteins.csv for development
python proteins-generator.py 2000000 <seed> # generates proteins.csv for final version
python lab1-proteins-serial.py
python lab1-proteins-mp.py
python lab1-Proteins-th4.py
python lab1-Proteins-th8.py
python lab1-Proteins-th12.py
python lab1-Proteins-th16.py
python lab1-Proteins-th20.py
```

Choose a seed and run from the folder containing `proteins-generator.py`. Datasets are not committed.

## About the multiprocessing implementations
The implementation lab1-proteins-mp.py uses multiprocessing only in the calculus of the inertia. A process is created for each of the k values.

The implementation lab1_proteins_mp_alt1.py utilizes a version of the KMeansCustom class which parallelizes the centroid updating process (the class is defined in kmeans_scratch_mp1.py). This is a suboptimal solution because each the updating process is done on every iteration of the method, meaning the number of processes created will be enormous. The cost of creating and closing all of these processes greatly outweighs any gains in speedup due to parallelization.

The implementation lab1_proteins_mp_alt2.py utilizes a version of the KMeansCustom class which parallelizes the centroid assigning process (the class is defined in kmeans_scratch_mp2.py). This method is suboptimal for the same reasons as the previous one.

The implementation lab1_proteins_mp_alt3.py uses multiprocessing in the calculus of the inertia (as in lab1-proteins-mp.py) as well as in the finding the optimal k. This method is slower than lab1-proteins-mp.py because finding the optimal k is a very fast process which makes the multiprocessing gains not worth the time spent creating the processes.

The implementation lab1_proteins_mp_alt4.py uses multiprocessing in the calculus of the inertia (as in lab1-proteins-mp.py) as well as in the preprocessing of the data (but not in the reading of the csv). This method does not provide any gains because sending the data to each process is slower than just processing the data serially.

The best multiprocessing implementation we have found is lab1-proteins-mp.py.


## Time statistics:
The statistics were obtained on a dataset of 2000000 samples generated with seed = 123.

**Guille's PC:**
- Number of physical cores: 20
- Number of logical cores: 20
- Base speed: 2.4 GHz
- RAM: 32 GB
- OS: Windows 11

- lab1-proteins-serial.py    
    - Time spent in preprocessing: 2.1980  (1.35%)
    - Time spent calculating the inertia for every k: 156.0769 s (95.87%)
    - Time spent finding the optimal k: 0.0052 s (0.00%)
    - Time spent calculating the final fit: 3.9991 s (2.46%)
    - Time spent analyzing the cluster with highest sequence length: 0.5283 s (0.32%)
    - Total program runtime (excluding ploting): 162.8082 seconds.

- lab1-proteins-mp.py
    - Time spent in preprocessing: 3.6728  (8.52%)
    - Time spent calculating the inertia for every k: 34.5442 s (80.10%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 4.4725 s (10.37%)
    - Time spent analyzing the cluster with highest sequence length: 0.4348 s (1.01%)
    - Total program runtime (excluding ploting): 43.1257 seconds.
    - Empirical Speedup: 162.8082 / 43.1257 = 3,77520133006537

- lab1-proteins-th4.py
    - Time spent in preprocessing: 3.4765  (5.84%)
    - Time spent calculating the inertia for every k: 51.7512 s (86.89%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 3.8710 s (6.50%)
    - Time spent analyzing the cluster with highest sequence length: 0.4600 s (0.77%)
    - Total program runtime (excluding ploting): 59.5593 seconds.
    - Empirical Speedup: 162.8082 / 59.5593 = 2,7335479093945

- lab1-proteins-th8.py
    - Time spent in preprocessing: 3.7146  (6.80%)
    - Time spent calculating the inertia for every k: 45.5553 s (83.37%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 4.9206 s (9.01%)
    - Time spent analyzing the cluster with highest sequence length: 0.4503 s (0.82%)
    - Total program runtime (excluding ploting): 54.6418 seconds.
    - Empirical Speedup: 162.8082 / 54.6418 = 2,97955411424953

- lab1-proteins-th12.py
    - Time spent in preprocessing: 3.5414  (10.01%)
    - Time spent calculating the inertia for every k: 27.1865 s (76.87%)
    - Time spent finding the optimal k: 0.0001 s (0.00%)
    - Time spent calculating the final fit: 4.1939 s (11.86%)
    - Time spent analyzing the cluster with highest sequence length: 0.4446 s (1.26%)
    - Total program runtime (excluding ploting): 35.3678 seconds.
    - Empirical Speedup: 162.8082 / 35.3678 = 4,60328886727475

- lab1-proteins-th16.py
    - Time spent in preprocessing: 3.3032  (8.24%)
    - Time spent calculating the inertia for every k: 31.6305 s (78.89%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 4.7406 s (11.82%)
    - Time spent analyzing the cluster with highest sequence length: 0.4207 s (1.05%)
    - Total program runtime (excluding ploting): 40.0960 seconds.
    - Empirical Speedup: 162.8082 / 40.0960 = 4,060459896249

- Parallelizable part (Inertia calculation): 95.87 %
- Maximum theoretical speedup (Amdahl's law): 1/((1-0.9587+0.9587/20)) = 11,2063652154424

Notice that the number of parallel processes cannot be greater than the number of ks to be analyzed (16). Therefore, having more than 16 cores will not improve the empirical speedup, even though Amdahl's law will return a bigger theoretical speedup. We could calculate the maximum speedup taking into account that no more than 16 cores will be used using Amdahl's law
- Maximum theoretical speedup (Amdahl's law, 16 cores): 1/((1-0.9587+0.9587/16)) = 9,87959246681074


**Alfredo's PC:**
- Number of physical cores: 10
- Number of logical cores: 16
- Base speed: 1.9 GHz
- RAM: 32GB
- OS: Windows
- lab1-proteins-serial.py    - Time spent in preprocessing: 3.8066  (2.62%)
    - Time spent calculating the inertia for every k: 137.1874 s (94.29%)
    - Time spent finding the optimal k: 0.0009 s (0.00%)
    - Time spent calculating the final fit: 3.7143 s (2.55%)
    - Time spent analyzing the cluster with highest sequence length: 0.7891 s (0.54%)
    - Total program runtime (excluding ploting): 145.4990 seconds

- lab1-proteins-mp.py
    - Time spent in preprocessing: 2.3774  (7.27%)
    - Time spent calculating the inertia for every k: 27.4523 s (83.96%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 2.4875 s (7.61%)
    - Time spent analyzing the cluster with highest sequence length:  0.3787 s (1.16%)
    - Total program runtime (excluding ploting): 32.6969 seconds seconds
    - Empirical Speedup: 145.4990 / 32.6969 = 4.44993256241417

- lab1-proteins-th4.py
    - Time spent in preprocessing: 2.4597  (4.71%)
    - Time spent calculating the inertia for every k: 46.9191 s (89.90%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 2.4461 s (4.69%)
    - Time spent analyzing the cluster with highest sequence length: 0.3618 s (0.69%)
    - Total program runtime (excluding ploting): 52.1880 seconds
    - Empirical Speedup: 145.4990 / 52.1880 = 2.78797807925194

- lab1-proteins-th8.py
    - Time spent in preprocessing: 3.7764  (7.36%)
    - Time spent calculating the inertia for every k: 43.1329 s (84.11%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 3.7888 s (7.39%)
    - Time spent analyzing the cluster with highest sequence length:  0.5795 s (1.13%)
    - Total program runtime (excluding ploting): 51.2787 seconds
    - Empirical Speedup: 145.4990 / 51.2787 = 2.83741592513071

- lab1-proteins-th12.py
    - Time spent in preprocessing:  3.7727  (8.39%)
    - Time spent calculating the inertia for every k: 36.9427 s (82.14%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 3.6964 s (8.22%)
    - Time spent analyzing the cluster with highest sequence length: 0.5638 s (1.25%)
    - Total program runtime (excluding ploting): 44.9764 seconds
    - Empirical Speedup: 145.4990 / 44.9764 = 3.2350076929234

- lab1-proteins-th16.py
    - Time spent in preprocessing:  3.9843  (9.80%)
    - Time spent calculating the inertia for every k: 32.3588 s (79.57%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 3.7366 s (9.19%)
    - Time spent analyzing the cluster with highest sequence length: 0.5856 s (1.44%)
    - Total program runtime (excluding ploting): 40.6667 seconds
    - Empirical Speedup: 145.4990 / 40.6667 = 3.57784132963825

- Parallelizable part (Inertia calculation): 93.52 %
- Maximum theoretical speedup (Amdahl's law): 6.897 


 
 
