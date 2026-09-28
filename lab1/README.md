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