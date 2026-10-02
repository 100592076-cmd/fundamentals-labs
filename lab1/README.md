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
- lab1-proteins-serial.py    - Time spent in preprocessing: 3.8835  (3.45%)
    - Time spent calculating the inertia for every k: 105.2427 s (93.52%)
    - Time spent finding the optimal k: 0.0079 s (0.01%)
    - Time spent calculating the final fit: 2.7955 s (2.48%)
    - Time spent analyzing the cluster with highest sequence length: 0.5999 s (0.53%)
    - Total program runtime (excluding ploting): 112.5305 seconds

- lab1-proteins-mp.py
    - Time spent in preprocessing: 3.7825  (13.79%)
    - Time spent calculating the inertia for every k: 21.4231 s (78.08%)
    - Time spent finding the optimal k:  0.0003 s (0.00%)
    - Time spent calculating the final fit: 1.5791 s (5.76%)
    - Time spent analyzing the cluster with highest sequence length:  0.6522 s (2.38%)
    - Total program runtime (excluding ploting): 27.4380 seconds seconds
    - Empirical Speedup: 112.5305 / 27.4380 = 4.10126466943655

- lab1-proteins-th4.py
    - Time spent in preprocessing: 3.8448  (6.68%)
    - Time spent calculating the inertia for every k: 50.0080 s (86.86%)
    - Time spent finding the optimal k: 0.0059 s (0.01%)
    - Time spent calculating the final fit: 3.1622 s (5.49%)
    - Time spent analyzing the cluster with highest sequence length: 0.5520 s (0.96%)
    - Total program runtime (excluding ploting): 57.5736 seconds
    - Empirical Speedup: 112.5305 / 57.5736 = 1.95455034946573

- lab1-proteins-th8.py
    - Time spent in preprocessing: 3.7535  (7.64%)
    - Time spent calculating the inertia for every k: 41.5564 s (84.54%)
    - Time spent finding the optimal k: 0.0004 s (0.00%)
    - Time spent calculating the final fit: 3.2546 s (6.62%)
    - Time spent analyzing the cluster with highest sequence length:  0.5925 s (1.21%)
    - Total program runtime (excluding ploting): 49.1583 seconds
    - Empirical Speedup: 112.5305 / 49.1583 = 2.28914547492489

- lab1-proteins-th12.py
    - Time spent in preprocessing:  3.7390  (8.98%)
    - Time spent calculating the inertia for every k: 33.9495 s (81.51%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 3.3823 s (8.12%)
    - Time spent analyzing the cluster with highest sequence length: 0.5797 s (1.39%)
    - Total program runtime (excluding ploting): 41.6515 seconds
    - Empirical Speedup: 112.5305 / 41.6515 = 2.70171542441449

- lab1-proteins-th16.py
    - Time spent in preprocessing: 3.8166  (9.65%)
    - Time spent calculating the inertia for every k: 31.8309 s (80.48%)
    - Time spent finding the optimal k: 0.0005 s (0.00%)
    - Time spent calculating the final fit: 3.3182 s (8.39%)
    - Time spent analyzing the cluster with highest sequence length: 0.5850 s (1.48%)
    - Total program runtime (excluding ploting): 39.5522 seconds.
    - Empirical Speedup: 112.5305 / 39.5522 = 2.84511354614914

- Parallelizable part (Inertia calculation): 93.52 %
- Maximum theoretical speedup (Amdahl's law): 6.897 


 
 
