from sklearn.cluster import KMeans

def kmpp(data_matrix, k):
    """Clusters a data matrix
       kmeans uses eudlidean distances by default http://scikit-learn.org/stable/modules/clustering.html#k-means
       http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
    """
    kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
    c = kmeans.fit(data_matrix)
    centroids = c.cluster_centers_
    labels = c.labels_
    return centroids, labels