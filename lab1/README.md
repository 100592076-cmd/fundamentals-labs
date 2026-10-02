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
The statistics were obtained on a dataset of 2000000 samples generated with seed = 123. (Make sure to have read the Before using section before running the code).

LOS TIEMPOS NO ESTÁN ACTUALIZADOS
**Guille's PC:**
- Number of physical cores: 20
- Number of logical cores: 20
- Base speed: 2.4 GHz
- RAM: 32 GB
- OS: Windows 11

- lab1-proteins-serial.py    
    - Time spent in preprocessing: 3.2531  (2.92%)
    - Time spent calculating the inertia for every k: 104.3704 s (93.62%)
    - Time spent finding the optimal k: 0.0048 s (0.00%)
    - Time spent calculating the final fit: 3.3963 s (3.05%)
    - Time spent analyzing the cluster with highest sequence length: 0.4550 s (0.41%)
    - Total program runtime (excluding ploting): 111.4801 seconds.

- lab1-proteins-mp.py
    - Time spent in preprocessing: 3.3709  (13.50%)
    - Time spent calculating the inertia for every k: 19.4612 s (77.92%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 1.7015 s (6.81%)
    - Time spent analyzing the cluster with highest sequence length: 0.4405 s (1.76%)
    - Total program runtime (excluding ploting): 24.9751 seconds.
    - Empirical Speedup: 111.4801 / 24.9751 = 4,46364979519602

- lab1-proteins-th4.py
    - Time spent in preprocessing: 2.7864  (5.98%)
    - Time spent calculating the inertia for every k: 40.2074 s (86.24%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 3.2715 s (7.02%)
    - Time spent analyzing the cluster with highest sequence length: 0.3558 s (0.76%)
    - Total program runtime (excluding ploting): 46.6232 seconds.
    - Empirical Speedup: 111.4801 / 46.6232 = 2,3910864119151

- lab1-proteins-th8.py
    - Time spent in preprocessing: 2.8448  (8.24%)
    - Time spent calculating the inertia for every k: 27.8994 s (80.77%)
    - Time spent finding the optimal k: 0.0004 s (0.00%)
    - Time spent calculating the final fit: 3.3609 s (9.73%)
    - Time spent analyzing the cluster with highest sequence length: 0.4362 s (1.26%)
    - Total program runtime (excluding ploting): 34.5423 seconds.
    - Empirical Speedup: 111.4801 / 34.5423 = 3,22735023435035

- lab1-proteins-th12.py
    - Time spent in preprocessing: 2.8953  (7.43%)
    - Time spent calculating the inertia for every k: 32.8127 s (84.24%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 2.8470 s (7.31%)
    - Time spent analyzing the cluster with highest sequence length: 0.3969 s (1.02%)
    - Total program runtime (excluding ploting): 38.9528 seconds.
    - Empirical Speedup: 111.4801 / 38.9528 = 2,86192776899222

- lab1-proteins-th16.py
    - Time spent in preprocessing: 3.0976  (7.89%)
    - Time spent calculating the inertia for every k: 31.7763 s (80.98%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 3.9326 s (10.02%)
    - Time spent analyzing the cluster with highest sequence length: 0.4310 s (1.10%)
    - Total program runtime (excluding ploting): 39.2382 seconds.
    - Empirical Speedup: 111.4801 / 39.2382 = 2,84111146790627

- Parallelizable part (Inertia calculation): 93.6 %
- Maximum theoretical speedup (Amdahl's law): 9.03

Notice that the number of parallel processes cannot be greater than the number of ks to be analyzed (16). Therefore, having more than 16 cores will not improve the empirical speedup, even though Amdahl's law will return a bigger theoretical speedup. We could calculate the maximum speedup taking into account that no more than 16 cores will be used using Amdahl's law
- Maximum theoretical speedup (Amdahl's law, 16 cores): 8.16


LOS TIEMPOS NO ESTÁN ACTUALIZADOS
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


 
 
