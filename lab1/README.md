# Lab 1 — K-Means Parallelization in Python

K-Means clustering (on `enzyme` and `hydrofob`) over a synthetic proteins dataset, in serial, `multiprocessing` and `threading` versions, comparing execution times and speedup.

## Usage

```bash
python proteins-generator.py 50000 <seed>   # generates proteins.csv
python lab1-proteins-serial.py
python lab1-proteins-mp.py
python lab1-Proteins-th.py
```

Choose a seed and run from the folder containing `proteins-generator.py`. Datasets are not committed.

## About the multiprocessing implementations
The implementation lab1-proteins-mp.py uses multiprocessing only in the calculus of the inertia. A process is created for each of the k values.

The implementation lab1_proteins_mp_alt1.py utilizes a version of the KMeansCustom class which parallelizes the centroid updating process (the class is defined in kmeans_scratch_mp1.py). This is a suboptimal solution because each the updating process is done on every iteration of the method, meaning the number of processes created will be enormous. The cost of creating and closing all of these processes greatly outweighs any gains in speedup due to parallelization.

The implementation lab1_proteins_mp_alt2.py utilizes a version of the KMeansCustom class which parallelizes the centroid assigning process (the class is defined in kmeans_scratch_mp2.py). This method is suboptimal for the same reasons as the previous one.

The implementation lab1_proteins_mp_alt3.py uses multiprocessing in the calculus of the inertia (as in lab1-proteins-mp.py) as well as in the finding the optimal k. This method is slower than lab1-proteins-mp.py because finding the optimal k is a very fast process which makes the multiprocessing gains not worth the time spent creating the processes.

The implementation lab1_proteins_mp_alt4.py uses multiprocessing in the calculus of the inertia (as in lab1-proteins-mp.py) as well as in the preprocessing of the data (but not in the reading of the csv). This method does not provide any gains because sending the data to each process is slower than just processing the data serially.

The best multiprocessing implementation we have found is lab1-proteins-mp.py.
Relevant time statistics for lab1-proteins-mp.py vs lab1-proteins-serial.py
Guille's PC:
- Number of cores: 20
- Base speed: 2.4 GHz
- lab1-proteins-serial.py    - Time spent in preprocessing: 2.7133  (2.96%)
    - Time spent calculating the inertia for every k: 87.3853 s (95.18%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 1.3023 s (1.42%)
    - Time spent analyzing the cluster with highest sequence length: 0.4092 s (0.45%)
    - Total program runtime (excluding ploting): 91.8110 seconds.

- lab1-proteins-mp.py
    - Time spent in preprocessing: 3.5208  (11.80%)
    - Time spent calculating the inertia for every k: 24.3996 s (81.80%)
    - Time spent finding the optimal k: 0.0002 s (0.00%)
    - Time spent calculating the final fit: 1.4597 s (4.89%)
    - Time spent analyzing the cluster with highest sequence length: 0.4480 s (1.50%)
    - Total program runtime (excluding ploting): 29.8294 seconds

- Empirical Speedup: 91.8110 / 29.8294 = 3,078 %

- Parallelizable part (Inertia calculation): 95 %
- Maximum theoretical speedup (Amdahl's law): 10.26
Notice that the number of parallel processes cannot be greater than the number of ks to be analyzed (16). Therefore, having more than 16 cores will not improve the empirical speedup, even though Amdahl's law will return a bigger theoretical speedup. 