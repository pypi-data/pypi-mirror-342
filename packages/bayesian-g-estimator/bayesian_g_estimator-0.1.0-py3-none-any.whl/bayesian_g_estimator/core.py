import numpy as np
from scipy.stats import norm


def bayesian_g_estimator(scores, x_start, x_end, n_points=120):
    """
    Estimate the latent trait (g) using a Bayesian method.

    Parameters:
        scores: list of tuples (observed_score, reliability). Observed scores are standardized; reliability is in [0, 1].
        x_start: float, start of latent trait grid
        x_end: float, end of latent trait grid
        n_points: int, number of points in the grid

    Returns:
        mean: posterior mean
        sd: posterior standard deviation
        x_values: grid of latent trait values
        phd: posterior distribution (normalized)
    """
    def gaussian_likelihood(x, u, s):
        return norm.pdf(x, loc=u, scale=s) #s is SD not variance
    def mult(x, scores):
        p = 1
        for score in scores:
            var_exp = score[1]**2
            error_var = 1 - var_exp
            error_sd = error_var**.5
            p *= gaussian_likelihood(score[0], x*score[1], error_sd )  
        return p
    x_values = np.linspace(x_start, x_end, n_points)
    likelihood = mult(x_values, scores)
    prior = gaussian_likelihood(x_values, 0, 1)
    pd = likelihood*prior
    pd = pd.sum()
    phd =  (likelihood*prior)/pd
    mean = sum([x*p for x,p in zip(x_values, phd)])
    var = sum([x*x*p for x,p in zip(x_values, phd)]) - mean**2
    sd = var**.5
    return mean, sd, x_values, phd


def ols_g_estimator(scores, size=200000):
    """
    Estimate the latent trait (g) using an Ordinary Least Squares (OLS) regression approach.

    Parameters:
        scores (list of tuples): Each tuple is (observed_score, reliability).
                                 Observed scores are standardized; reliability is in [0, 1].
        size (int): Number of samples to generate for simulation.

    Returns:
        estimate (float): Estimated latent trait value.
        sd_err (float): Standard error of the estimate.
        b (ndarray): Estimated regression coefficients.
    """
    g = np.random.normal(0,1, size)
    data = np.zeros( (size, len(scores)+1) )
    data[:,0] = 1
    for i, score in enumerate(scores):
        rel = score[1]
        test_score = rel*g + np.random.normal(0, (1 - rel**2)**.5, size) #2nd is SD not var
        data[:,(i+1)] = test_score
    b = np.linalg.inv(data.T @ data) @ (data.T @ g)
    zs = [1]
    zs.extend(np.array([x for x,y in scores]))
    estimate = zs @ b
    var_exp = ((data @ b).std())**2
    sd_err = (1 - var_exp)**.5
    return estimate, sd_err, b

def brute_force_g_estimator(scores, size=20000000, range=.33):
    """
    Estimate the latent trait (g) by brute-force filtering of a large simulated population.

    Parameters:
        scores (list of tuples): Each tuple is (observed_score, reliability).
                                 Observed scores should be standardized.
        size (int): Number of samples to simulate.
        range (float): Tolerance range around each observed score when filtering.

    Returns:
        mean (float): Mean of the g values in the filtered subset.
        std (float): Standard deviation of the g values in the subset.
        subset (ndarray): Array of matched rows, where column 0 is the g value.
    """
    g = np.random.normal(0,1, size)
    data = np.zeros( (size, len(scores)+1) )
    data[:,0] = g
    for i, score in enumerate(scores):
        rel = score[1]
        test_score = rel*g + np.random.normal(0, (1 - rel**2)**.5, size) #2nd is SD not var
        data[:,(i+1)] = (test_score - test_score.mean())/(test_score.std())
    subset = np.copy( data )
    for i, score_tuple in enumerate(scores):
        score = score_tuple[0]
        subset = subset[(subset[:, i+1] >= score-range) & (subset[:, i+1] <= score+range)]
    return subset[:,0].mean(), subset[:,0].std(), subset