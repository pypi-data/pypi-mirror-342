import numpy as np 
import matplotlib.pyplot as plt
from lalinference.imrtgr.nrutils import bbh_final_spin_projected_spins, bbh_final_mass_projected_spins, bbh_Kerr_trunc_opts

def plot_samples(samples, xlabel):

    plt.figure()
    plt.hist(samples, bins=100, density=True, fill=False, histtype='step')
    plt.axvline(np.median(samples), color='crimson', label='Median')
    plt.xlabel(xlabel)
    plt.legend()

def order_chi1_chi2_samples(m1_samples, m2_samples, chi1_samples, chi2_samples):

    m1_samples_ordered   = np.zeros(len(m1_samples  ))
    m2_samples_ordered   = np.zeros(len(m2_samples  ))
    chi1_samples_ordered = np.zeros(len(chi1_samples))
    chi2_samples_ordered = np.zeros(len(chi2_samples))

    for i in range(len(chi1_samples)):

        if m1_samples[i] < m2_samples[i]: 
            chi1_samples_ordered[i], chi2_samples_ordered[i] = chi2_samples[i], chi1_samples[i]
            m1_samples_ordered[i],   m2_samples_ordered[i]   = m2_samples[i], m1_samples[i]
        else                            : 
            chi1_samples_ordered[i], chi2_samples_ordered[i] = chi1_samples[i], chi2_samples[i]
            m1_samples_ordered[i],   m2_samples_ordered[i]   = m1_samples[i], m2_samples[i]

    return m1_samples_ordered, m2_samples_ordered, chi1_samples_ordered, chi2_samples_ordered

"""

This script generates samples from the prior distributions of the progenitor masses and spins, and then computes derived parameters such as the mass ratio, effective spin, and final spin. The progenitor samples are ordered according to the model convention.

"""

########################
# Start of user inputs #
########################

# Number of samples to generate
Nsamples = 10000

# Prior boundaries for progenitor masses and spins
m_min   =   10
m_max   =  200
chi_min = -  0.8
chi_max =    0.8

######################
# End of user inputs #
######################

samples = {}

# Priors on the progenitors samples

m1_unif   = np.random.uniform(m_min,     m_max, size=Nsamples)
m2_unif   = np.random.uniform(m_min,     m_max, size=Nsamples)
chi1_unif = np.random.uniform(chi_min, chi_max, size=Nsamples)
chi2_unif = np.random.uniform(chi_min, chi_max, size=Nsamples)

# Impose ordering, according to model convention
m1_samples_ordered, m2_samples_ordered, chi1_samples_ordered, chi2_samples_ordered = order_chi1_chi2_samples(m1_unif, m2_unif, chi1_unif, chi2_unif)

samples['m1']   = m1_samples_ordered
samples['m2']   = m2_samples_ordered
samples['chi1'] = chi1_samples_ordered
samples['chi2'] = chi2_samples_ordered

# Compute derived parameters
q_samples_ordered      = samples['m1'] / samples['m2']
chieff_samples_ordered = (samples['m1'] * samples['chi1'] + samples['m2'] * samples['chi2']) / (samples['m1'] + samples['m2'])

tilt1_samples_ordered = np.zeros(len(m1_samples_ordered))
tilt2_samples_ordered = np.zeros(len(m2_samples_ordered))
for i in range(len(m1_samples_ordered)):
    if(chi1_samples_ordered[i] < 0): tilt1_samples_ordered[i] = np.pi
    else: tilt1_samples_ordered[i] = 0.0
    if(chi2_samples_ordered[i] < 0): tilt2_samples_ordered[i] = np.pi
    else: tilt2_samples_ordered[i] = 0.0

chi1_magn_samples_ordered = np.abs(chi1_samples_ordered)
chi2_magn_samples_ordered = np.abs(chi2_samples_ordered)

Mf_samples_ordered = bbh_final_mass_projected_spins(samples['m1'], samples['m2'], chi1_magn_samples_ordered, chi2_magn_samples_ordered, tilt1_samples_ordered, tilt2_samples_ordered, 'UIB2016')
af_samples_ordered = bbh_final_spin_projected_spins(samples['m1'], samples['m2'], chi1_magn_samples_ordered, chi2_magn_samples_ordered, tilt1_samples_ordered, tilt2_samples_ordered, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)

samples['q']         = q_samples_ordered
samples['chieff']    = chieff_samples_ordered
samples['Mf']        = Mf_samples_ordered
samples['af']        = af_samples_ordered

for key in samples.keys(): plot_samples(samples[key], key)
plt.show()