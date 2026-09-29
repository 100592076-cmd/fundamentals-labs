# Lab 1 — K-Means Parallelization in Python

K-Means clustering (on `enzyme` and `hydrofob`) over a synthetic proteins dataset, in serial, `multiprocessing` and `threading` versions, comparing execution times and speedup.
 
## Before using
In order to correctly show the speedup obtain with the parallelization we have implemented, we will tell NumPy's BLAS library to avoid using multithreading itself. To do this we first need to install the library threadpoolctl.

```bash
python -m pip install threadpoolctl
```
We can now check how many threads are being used by BLAS by running:

```bash
python -c "import numpy as np; from threadpoolctl import threadpool_info; np.ones((2, 2)) @ np.ones((2, 2)); print(threadpool_info())"
```
We can force BLAS to use only one thread with the command:

```bash
$env:OPENBLAS_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'; $env:OMP_NUM_THREADS = '1';
```
Running the same command with different numbers allows us to return to the original configuration. 

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

- Parallelizable part (Inertia calculation): 95 %
- Maximum theoretical speedup (Amdahl's law): 10.26
Notice that the number of parallel processes cannot be greater than the number of ks to be analyzed (16). Therefore, having more than 16 cores will not improve the empirical speedup, even though Amdahl's law will return a bigger theoretical speedup. We could calculate the maximum speedup taking into account that no more than 16 cores will be used using Amdahl's law
- Maximum theoretical speedup (Amdahl's law, 16 cores): 9.14



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
    - Time spent in preprocessing: 3.7366  (12.69%)
    - Time spent calculating the inertia for every k: 23.8731 s (81.10%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 1.2687 s (4.31%)
    - Time spent analyzing the cluster with highest sequence length: 0.5572 s (1.89%)
    - Total program runtime (excluding ploting): 29.4372 seconds

- Empirical Speedup: 112.5305 / 29.4372 = 3,823 

- Parallelizable part (Inertia calculation): 95 %
- Maximum theoretical speedup (Amdahl's law): 6.897 

- lab1-proteins-th.py
    - Time spent in preprocessing: 3.7482  (8.80%)
    - Time spent calculating the inertia for every k: 34.9975 s (82.20%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 3.2360 s (7.60%)
    - Time spent analyzing the cluster with highest sequence length: 0.5935 s (1.39%)
    - Total program runtime (excluding ploting): 42.5762 seconds

- Empirical Speedup: 112.5305 / 42.5762 = 2.643 

- Parallelizable part (Inertia calculation): 95 %
- Maximum theoretical speedup (Amdahl's law): 6.897  
 
 
