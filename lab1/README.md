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

The implementation lab1_proteins_mp_alt1.py utilizes a version of the KMeansCustom class which parallelizes the centroid updating process (the class is defined in kmeans_scratch_mp.py). This is a suboptimal solution because each update is computationally cheap (it only involves calculating means and I/O operations), but there is a great number of them.

One possible implementation would be to combine the ideas in lab1-proteins-mp.py and lab1_proteins_mp_alt1.py, parallelizing both the KMeansCustom class and the calculus of the inertia. This is not possible because Python does not allow nested multiprocessing with pools (a function running inside a multiprocessing.pool cannot create another pool). Regardless of whether or not it can be implemented, it would carry all the drawbacks of the lab1_proteins_mp_alt1.py implementation (too many processes created to parallelize cheap tasks), so it would not be worth it in any case.