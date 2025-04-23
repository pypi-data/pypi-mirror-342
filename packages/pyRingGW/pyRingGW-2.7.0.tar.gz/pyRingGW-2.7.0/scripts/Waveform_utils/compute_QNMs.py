from pyRing.waveform import QNM, QNM_fit
from pyRing.utils    import qnm_interpolate, F_mrg_Nagar
import lal

########################
# Start of user inputs #
########################

# For QNM fit
Mf    = 70
af    = 0.68
modes = [(2,2,0), (2,2,1), (3,3,0), (2,1,0), (3,2,0)]
fit   = 1

# For peak frequency fit
m1, m2 = 35.0, 35.0
a1, a2 = 0.0, 0.0

######################
# End of user inputs #
######################

for (l,m,n) in modes:

    if(fit):

        f   = QNM_fit(l,m,n).f(Mf, af)
        tau = QNM_fit(l,m,n).tau(Mf, af)

    else:
        # Do it interpolating Berti et al. table

        qnm_interpolants                  = {}
        interpolate_freq, interpolate_tau = qnm_interpolate(2,l,m,n)
        qnm_interpolants[(2,l,m,n)]       = {'freq': interpolate_freq, 'tau': interpolate_tau}

        f   = QNM(2,l,m,n, qnm_interpolants).f(Mf, af)
        tau = QNM(2,l,m,n, qnm_interpolants).tau(Mf, af)


    f_mrg = F_mrg_Nagar(m1*lal.MSUN_SI, m2*lal.MSUN_SI, a1, a2)

    print('(l,m,n)     = ({},{},{})'.format(l,m,n))
    print('M_f [M_sun] = {:.3f}'.format(Mf))
    print('M_f [s]     = {:.3f}'.format(Mf*lal.MTSUN_SI))
    print('a_f         = {:.3f}'.format(af))
    print('f   [Hz]    = {:.3f}'.format(f))
    print('tau [ms]    = {:.3f}'.format(tau*1e3))
    print('tau [M]     = {:.3f}'.format(tau/(Mf*lal.MTSUN_SI)))
    print('f_mrg [Hz]  = {:.3f}'.format(f_mrg))
    print('\n')