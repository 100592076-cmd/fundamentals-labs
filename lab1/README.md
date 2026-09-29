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
- lab1-proteins-serial.py
    - Time spent in preprocessing: 2.5588  (2.87%)
    - Time spent calculating the inertia for every k: 84.8638 s (95.05%)
    - Time spent finding the optimal k: 0.0003 s (0.00%)
    - Time spent calculating the final fit: 1.4765 s (1.65%)
    - Total program runtime (excluding ploting): 89.2814 seconds

- lab1-proteins-mp.py
    - Time spent in preprocessing: 3.4436  (11.02%)
    - Time spent calculating the inertia for every k: 25.8514 s (82.72%)
    - Time spent finding the optimal k: 0.0028 s (0.01%)
    - Time spent calculating the final fit: 1.4898 s (4.77%)
    - Total program runtime (excluding ploting): 31.2527 seconds
- Empirical Speedup: 89.2814/31.2527=2.857%
- Number of cores: 20
- Parallelizable part (Inertia calculation): 95 %
- Maximum theoretical speedup (Amdahl's law): 10.26