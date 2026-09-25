import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from kmeans_scratch import KMeansCustom  # Import custom K-Means class



def preprocess_dataset(df):
    # In order to work with the feature sequence, we work with length sequence.
    df["seq_length"] = df["sequence"].str.len()
    X = df[["enzyme", "hydrofob"]].to_numpy()
    return df, X


def compute_wcss(X, k_range, seed=123):
    # Function that computes inertia for a range of k values using the custom KMeans implementation.
    wcss_list = []
    for k in k_range:
        km = KMeansCustom(k=k, seed=seed)
        km.fit(X)
        wcss_list.append(km.inertia_)
    return wcss_list


# In order to find the optimal number of clusters (k), we are going to use elbow method, which consists of obtaining
# the value of k where inertia convexity changes. For doing that, we are going to find the maximum distance from the line that
# connects the first and last points of the inertia curve. This point is the optimal k. 

def find_optimal_k_elbow(k_values, wcss_list):
    # Finds optimal k using normalized perpendicular distance to the secant line
    k_arr = np.array(k_values, dtype=float)
    wcss_arr = np.array(wcss_list, dtype=float)

    # Min-Max normalization to standard scale [0, 1]
    k_norm = (k_arr - k_arr.min()) / (k_arr.max() - k_arr.min())
    wcss_norm = (wcss_arr - wcss_arr.min()) / (wcss_arr.max() - wcss_arr.min())

    p1 = np.array([k_norm[0], wcss_norm[0], 0])
    p2 = np.array([k_norm[-1], wcss_norm[-1], 0])

    distances = []
    for kn, wn in zip(k_norm, wcss_norm):
        p0 = np.array([kn, wn, 0])
        # Perpendicular distance formula
        dist = np.abs(np.cross(p2 - p1, p1 - p0)) / np.linalg.norm(p2 - p1)
        distances.append(dist)

    optimal_idx = np.argmax(distances)
    return k_values[optimal_idx], distances


def get_cluster_highest_seq_length(df):
    # Sequence analysis: Finds cluster with the longest sequence.
    # Tie-breaker rule: if several have maximum length, pick the one with maximum Hydrofob.

    sorted_df = df.sort_values(by=["seq_length", "hydrofob"], ascending=[False, False])
    max_seq_row = sorted_df.iloc[0]

    target_cluster_id = int(max_seq_row["cluster"])
    target_cluster_df = df[df["cluster"] == target_cluster_id]
    avg_seq_length = target_cluster_df["seq_length"].mean()

    return target_cluster_id, max_seq_row["protid"], max_seq_row["seq_length"], avg_seq_length
    
    

def project_point_to_segment(x1, y1, x2, y2, x0, y0):
    # Project (x0, y0) on the line defined by [(x1, y1), (x2, y2)]

    AB = np.array([x2 - x1, y2 - y1])
    AP = np.array([x0 - x1, y0 - y1])
    denom = np.dot(AB, AB)
    if denom == 0:
        return x1, y1
    t = np.dot(AP, AB) / denom
    t = max(0, min(1, t))
    x_proj = x1 + t * (x2 - x1)
    y_proj = y1 + t * (y2 - y1)
    return x_proj, y_proj


def plot_elbow(ax, k_range, wcss_list, optimal_k):
    k_arr = np.array(k_range, dtype=float)
    wcss_arr = np.array(wcss_list, dtype=float)

    # Normalisation for calculating the perpendicular distance to the line connecting the first and last points of the inertia curve.
    k_norm = (k_arr - k_arr.min()) / (k_arr.max() - k_arr.min())
    wcss_norm = (wcss_arr - wcss_arr.min()) / (wcss_arr.max() - wcss_arr.min())

    opt_idx = k_range.index(optimal_k)

    # We use auxiliar function defined before in order to make the projections
    xn_proj, yn_proj = project_point_to_segment(k_norm[0], wcss_norm[0], k_norm[-1], wcss_norm[-1], k_norm[opt_idx], wcss_norm[opt_idx])

    # We revert normalisaton to get the values of the projected point
    x_proj = xn_proj * (k_arr.max() - k_arr.min()) + k_arr.min()
    y_proj = yn_proj * (wcss_arr.max() - wcss_arr.min()) + wcss_arr.min()

    # Plot 
    ax.plot(k_range, wcss_list, "bo-", label="Inertia")
    ax.plot([k_range[0], k_range[-1]], [wcss_list[0], wcss_list[-1]], "r--", label="Reference Line")

    # Line which joins optimal k and projected point
    ax.plot([optimal_k, x_proj], [wcss_list[opt_idx], y_proj], color="g", linestyle="--", linewidth=2, label=f"Perpendicular Dist (k={optimal_k})")
    ax.set_title("Elbow Graph")
    ax.set_xlabel("Number of Clusters (k)")
    ax.set_ylabel("Inertia")
    ax.legend()
    ax.grid(True)


def plot_clusters(ax, df, final_km, optimal_k):
    # Generates cluster scatter plot with centroids marked.
    sns.scatterplot(data=df, x="enzyme", y="hydrofob", hue="cluster", palette="viridis", alpha=0.6, ax=ax, s=20)
    ax.scatter(final_km.centroids_[:, 0], final_km.centroids_[:, 1], c="red", marker="X", s=200, label="Centroids")
    ax.set_title(f"Clustering K-Means (k={optimal_k})")
    ax.set_xlabel("Enzyme")
    ax.set_ylabel("Hydrofob")
    ax.legend()


def plot_centroids_heatmap(ax, final_km, optimal_k):
    # Plots a heatmap of the centroids for each cluster.
    centroid_df = pd.DataFrame(final_km.centroids_, columns=["Enzyme", "Hydrofob"], index=[f"Cluster {i}" for i in range(optimal_k)])
    sns.heatmap(centroid_df, annot=True, cmap="YlGnBu", fmt=".3f", ax=ax)
    ax.set_title("Heatmap of Centroids")


# Serial execution

if __name__ == "__main__":
    # Start global timer
    start = time.time()
    print("Sequential execution started...")

    # Load and preprocess dataset
    df = pd.read_csv("proteins.csv")
    print("Successfully loaded 'proteins.csv'.")
    df, X = preprocess_dataset(df)

    # Calculate optimal k using Elbow Method
    print("\nCalculating optimal k using the Elbow Method (sequential)...")
    t_start_elbow = time.time()
    k_range = list(range(1, 16))
    wcss_list = compute_wcss(X, k_range, seed=123)
    optimal_k, _ = find_optimal_k_elbow(k_range, wcss_list)
    t_elbow_total = time.time() - t_start_elbow
    print(f"Optimal number of clusters (k) found: {optimal_k}")

    # Run K-Means with optimal k
    print(f"\nClustering data into {optimal_k} clusters (manual K-Means)...")
    t_start_final_fit = time.time()
    final_km = KMeansCustom(k=optimal_k, seed=123)
    final_km.fit(X)
    df["cluster"] = final_km.labels_
    t_final_fit = time.time() - t_start_final_fit
    print("Clustering complete.")

    # Sequence analysis
    print("\n--- Analysis of Cluster with Highest Total Sequence Length ---")
    target_cluster_id, max_protid, max_seq_len, avg_seq_len = get_cluster_highest_seq_length(df)

    print(f"Cluster ID with longest sequence : {target_cluster_id}")
    print(f"  - Protein ID                  : {max_protid}")
    print(f"  - Maximum sequence length     : {max_seq_len}")
    print(f"  - Average sequence length     : {avg_seq_len:.2f}")

    end = time.time()
    total_execution_time = end - start

    print(f"\nTotal program runtime: {total_execution_time:.4f} seconds.")
    print("Generating plots...")

    # Build figures
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    plot_elbow(axes[0], k_range, wcss_list, optimal_k)
    plot_clusters(axes[1], df, final_km, optimal_k)
    plot_centroids_heatmap(axes[2], final_km, optimal_k)
    plt.tight_layout()

    # Amdahl's Law parallelizable calculations
    parallelizable_time = t_elbow_total + t_final_fit
    p_factor = (parallelizable_time / total_execution_time) * 100

    print("\n--- Amdahl's Law Metrics ---")
    print(f"Parallelizable code computing Elbow Method : {t_elbow_total:.4f} s ({(t_elbow_total / total_execution_time) * 100:.2f}%)")
    print(f"Parallelizable code computing Final Fit    : {t_final_fit:.4f} s ({(t_final_fit / total_execution_time) * 100:.2f}%)")
    print(f"Total parallelizable percentage (p)        : {p_factor:.2f}% (for Amdahl's Law)")
    print("\nDisplaying plots. Close plot windows to exit.")
    plt.show()