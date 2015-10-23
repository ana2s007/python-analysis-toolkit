import numpy as np
import matplotlib.pyplot as plt
import hashlib

from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.utils.extmath import fast_dot

from python_analysis_toolkit.machine_learning import clustering

_colors = ['r', 'b', 'g', 'k', 'm', 'c', 'y']  

def pca_biplot_with_clustering(data_matrix, feature_labels, mean_normalize = False, k_means_post = True, K = 5, n_components=2, f_out = "foo"):
    """
    Inputs:
        data_matrix: numpy array of shape n x f where n is the number of samples and f is the number of features (variables)
        feature_labels: the list of human-interpretable labels for the rows in data_matrix. Used for the biplot
        mean_normalize: if true, each row i of data_matrix is replaced with i - mean(i)
        k_means_post: if True, k means is run after the PCA analysis on the projected data matrix. I.e., in the reduced space. 
                      if False, it is run before the PCA, and before the mean_normalization, and then the clusters are projected into the space. 
        n_components: the number of PCA vectors you want. 
        f_out: the path to write the graph (as PDF) to
        
        TODO: the graph currently only supports n=2. 
    
    Outputs:
        r_loadings: the loading vectors
        
    Side Effects:
        file created on disk at f_out
    
    References:
        http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
        https://github.com/teddyroland/python-biplot/blob/master/biplot.py
        http://stackoverflow.com/questions/21217710/factor-loadings-using-sklearn
        http://stackoverflow.com/questions/14716965/r-principle-component-analysis-label-of-component
        http://nxn.se/post/36838219245/loadings-with-scikit-learn-pca
    """    
    data_matrix = np.nan_to_num(data_matrix) #clustering does not allow infs, nans
    
    if not k_means_post: 
        centroids, labels = clustering.kmpp(data_matrix, K)
        
    if mean_normalize:   
        for iindex, i in enumerate(data_matrix):
            data_matrix[iindex] = i - np.mean(i)

    rows, variables = np.shape(data_matrix)
    pca = PCA(n_components=n_components)
    pca.fit(data_matrix)
    
    r_loadings = np.matrix.transpose(pca.components_) #components is n_components x f; transpase to get rows as features, like R does it 
    
    transformed_matrix = fast_dot(data_matrix, r_loadings)
    
    loading_vectors = []
    loading_labels = []
            
    for i in range(0, variables):
        loading_vectors.append((list(r_loadings[i])))
        loading_labels.append(str(feature_labels[i]))
    
    if k_means_post: 
        centroids, labels = clustering.kmpp(transformed_matrix, K)
    
    #do the plot
    fig, ax = plt.subplots()

    for l in range(0, K):
        transformed_matrix_i = [transformed_matrix[i] for i in range(0, rows) if labels[i] == l]                     
        ax.scatter([x[0] for x in transformed_matrix_i], 
                   [x[1] for x in transformed_matrix_i], 
                   color = _colors[l % len(_colors)],
                   label = "cluster" + str(l))

    pxs = [i[0] for i in loading_vectors]
    pys =  [i[1] for i in loading_vectors]    
    for xindex, x in enumerate(pxs):     
        ax.arrow(0, 0, pxs[xindex], pys[xindex], linewidth=3, width=0.0005, head_width=0.0025, color="r", label = "loading")
        ax.arrow(0, 0, pxs[xindex]*5, pys[xindex]*5, alpha = .5, linewidth = 1, linestyle="dashed", width=0.0005, head_width=0.0025, color="r")
        ax.text(pxs[xindex]*5, pys[xindex]*5, loading_labels[xindex], color="r")
    
    ax.legend(loc='best')
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_xlim(min(x0, y0), max(x1,y1)) #make it square
    ax.set_ylim(min(x0, y0), max(x1,y1))      
    ax.set_xlabel("PCA[0]")
    ax.set_ylabel("PCA[1]") 
    ax.set_title("", fontsize = 20)
    ax.grid(b=True, which='major', color='k', linestyle='--')

    fig.savefig(f_out + "{0}{1}{2}".format(K, "_meannormalized" if mean_normalize else "", "_kmpost" if k_means_post else "_kmfirst") + ".pdf", format="pdf")    
    plt.close() #THIS IS CRUCIAL SEE:  http://stackoverflow.com/questions/26132693/matplotlib-saving-state-between-different-uses-of-io-bytesio
    return r_loadings


