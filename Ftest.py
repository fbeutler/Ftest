
#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f
from scipy.stats import norm

'''
This program performs an ANOVA F test followed by individual t tests
'''

def main():
	# Input parameters
	Nminusk = 10000
	kminus1 = 2
	step = 0.001

	# Integrate the F-distribution to get the critical value
	F = 0.
	integrate = 0
	while integrate < 0.95:
		F += step
		integrate += f.pdf(F, kminus1, Nminusk)*step
		if integrate > 0.95:
			print "F value at 95%% confidence level is %0.1f" % F
			break

	# Plot the F-distribution
	x = np.linspace(0, 100, 1000)
	plt.plot(x,f.pdf(x, kminus1, Nminusk), color="blue", linewidth=3)
	plt.axvline(F, color="black", linestyle="--", linewidth=2)
	plt.xlim(0, 5)
	plt.xlabel('$x$')
	plt.ylabel(r'$F(x, %d, %d)$' % (kminus1, Nminusk))
	plt.title("$F(x, %d, %d)$ Distribution" % (kminus1, Nminusk))
	plt.legend()
	plt.show()

	# Calculate the required number of users
	download_rate_estimate = 0.02
	sigma2_s = download_rate_estimate*(1. - download_rate_estimate)
	N = 5.3792*sigma2_s/(0.1*download_rate_estimate)**2
	print "estimate of N = %d" % round(N)

	# Run the obtained results through the F test
	input_downloads = [500, 620, 490]
	download_fractions = [entry/N for entry in input_downloads]
	print "F test result = %0.4f" % Ftest(download_fractions, sigma2_s, N)

	# Perform individual t-test
	print "The 96.6%% confidence interval is = (%0.2f %0.2f)" % (norm.interval(0.966, loc=0, scale=1))
	for fraction in download_fractions[1:]:
		print "t value = %0.2f (for a measured download rate of %0.4f)" % (ttest(N, fraction, N, download_fractions[0]), fraction)

  	return 

# function to calculate the t value
def ttest(N_A, p_A, N_0, p_0):
	# calculate the variance assuming a Bernoulli distribution
	variance_A = p_A*(1.-p_A)
	variance_0 = p_0*(1.-p_0)
	return (p_A - p_0)/np.sqrt(variance_A/N_A + variance_0/N_0)

# function to calculate the F value
def Ftest(download_fractions, sigma2_s, N):
	# number of participating samples
	k = len(download_fractions)
	# calculate the global mean
	global_download_fraction = sum(download_fractions)/k
	numerator = sum([(local_fraction - global_download_fraction)**2 for local_fraction in download_fractions])/(k - 1)
	# calculate the variance for each sample assuming a Bernoulli distribution
	variances = [local_fraction*(1.-local_fraction) for local_fraction in download_fractions]
	denominator = sum([sigma2_s for sigma2_s in variances])/(N - k)
	return numerator/denominator


if __name__ == '__main__':
  main()
