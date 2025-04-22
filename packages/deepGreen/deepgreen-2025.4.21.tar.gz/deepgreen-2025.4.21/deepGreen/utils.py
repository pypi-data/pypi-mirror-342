import torch
import colorama as ca
import numpy as np

def check_cuda():
    p_hint(f'CUDA availability: {torch.cuda.is_available()}')
    p_hint(f'Available GPUs: {torch.cuda.device_count()}')


def p_header(text):
    print(ca.Fore.CYAN + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_hint(text):
    print(ca.Fore.LIGHTBLACK_EX + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_success(text):
    print(ca.Fore.GREEN + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_fail(text):
    print(ca.Fore.RED + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)

def p_warning(text):
    print(ca.Fore.YELLOW + ca.Style.BRIGHT + text + ca.Style.RESET_ALL)


def leakybucket(phi, da_T, da_P, Mmax=0.76, Mmin=0.01, alph=0.093, m_th=4.886, mu_th=5.8, rootd=1000, M0=0.2):
    # This is the monthly version, and the submontly is not implemented yet.
    T = da_T.values.reshape((-1, 12)).T
    P = da_P.values.reshape((-1, 12)).T
    nyrs = T.shape[1]

    # output vars
    M = np.ndarray((12, nyrs))
    potEv = np.ndarray((12, nyrs))

    # Compute normalized daylength (neglecting small difference in calculation for leap-years)
    latr = phi*np.pi/180;  # change to radians
    ndays = np.array([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    cdays = np.cumsum(ndays)

    # calculate mean monthly daylength (used for evapotranspiration in soil moisture calcs)
    jday = cdays[0:12] + .5*ndays[1:13]
    m_star = 1-np.tan(latr)*np.tan(23.439*np.pi/180*np.cos(jday*np.pi/182.625))
    mmm = np.empty(12)
    mmm[:] = np.nan

    for mo in range(12):
        if m_star[mo] < 0:
            mmm[mo] = 0
        elif m_star[mo] >0 and m_star[mo] < 2:
            mmm[mo] = m_star[mo]
        elif m_star[mo] > 2:
            mmm[mo] = 2


    nhrs = 24*np.arccos(1-mmm)/np.pi # the number of hours in the day in the middle of the month
    L = (ndays[1:13]/30)*(nhrs/12) # mean daylength in each month.

    for cyear in range(nyrs):    # begin cycling over years
        for t in range(12):      # begin cycling over months in a year
            # Compute potential evapotranspiration for current month after Thornthwaite:
            if T[t,cyear] < 0:
                Ep = 0
            elif T[t,cyear] >= 0 and T[t,cyear] < 26.5:
                istar = T[:,cyear]/5
                istar[istar<0] = 0

                I = np.sum(istar**1.514)
                a = (6.75e-7)*I**3 - (7.71e-5)*I**2 + (1.79e-2)*I + .49
                Ep = 16*L[t]*(10*T[t,cyear]/I)**a
            elif T[t,cyear] >= 26.5:
                Ep = -415.85 + 32.25*T[t,cyear] - .43* T[t,cyear]**2

            potEv[t,cyear] = Ep
            # Now calculate soil moisture according to the CPC Leaky Bucket model (see J. Huang et al, 1996).
            if t > 0:
                # evapotranspiration:
                Etrans = Ep*M[t-1,cyear]*rootd/(Mmax*rootd)
                # groundwater loss via percolation:
                G = mu_th*alph/(1+mu_th)*M[t-1,cyear]*rootd
                # runoff; contributions from surface flow (1st term) and subsurface (2nd term)
                R = P[t,cyear]*(M[t-1,cyear]*rootd/(Mmax*rootd))**m_th + (alph/(1+mu_th))*M[t-1,cyear]*rootd
                dWdt = P[t,cyear] - Etrans - R - G
                M[t,cyear] = M[t-1,cyear] + dWdt/rootd
            elif t == 0 and cyear > 0:
                # evapotranspiration:
                Etrans = Ep*M[11,cyear-1]*rootd/(Mmax*rootd)
                # groundwater loss via percolation:
                G = mu_th*alph/(1+mu_th)*M[11,cyear-1]*rootd
                # runoff; contributions from surface flow (1st term) and subsurface (2nd term)
                R = P[t,cyear]*(M[11,cyear-1]*rootd/(Mmax*rootd))**m_th + (alph/(1+mu_th))*M[11,cyear-1]*rootd
                dWdt = P[t,cyear] - Etrans - R - G
                M[t,cyear] = M[11,cyear-1] + dWdt/rootd
            elif t == 0 and cyear == 0:
                if M0 < 0:
                    M0 = .20
                # evapotranspiration (take initial soil moisture value to be 200 mm)
                Etrans = Ep*M0*rootd/(Mmax*rootd)
                # groundwater loss via percolation:
                G = mu_th*alph/(1+mu_th)*(M0*rootd)
                # runoff; contributions from surface flow (1st term) and subsurface (2nd term)
                R = P[t,cyear]*(M0*rootd/(Mmax*rootd))**m_th + (alph/(1+mu_th))*M0*rootd
                dWdt = P[t,cyear] - Etrans - R - G
                M[t,cyear] = M0 + dWdt/rootd

            # error-catching:
            if M[t,cyear] <= Mmin:
                M[t,cyear] = Mmin
            if M[t,cyear] >= Mmax:
                M[t,cyear] = Mmax
            if np.isnan(M[t,cyear])==1:
                M[t,cyear] = Mmin

    da_M = da_P.copy()
    da_M.name = 'sm'
    da_M.attrs['long_name'] = 'soil moisture'
    da_M.attrs['units'] = 'v/v'
    da_M.values = M.T.flatten()
    return da_M

def compute_gE(phi):
    gE = np.ones(12)
    gE[:] = np.nan

    # Compute normalized daylength (neglecting small difference in calculation for leap-years)
    latr = phi*np.pi/180;  # change to radians
    ndays = np.array([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    cdays = np.cumsum(ndays)
    sd = np.arcsin(np.sin(np.pi*23.5/180) * np.sin(np.pi * ((np.arange(1,366) - 80)/180)))   # solar declination
    y = -np.tan(np.ones(365)* latr) * np.tan(sd)
    y[y>=1] = 1
    y[y<=-1] = -1
    hdl = np.arccos(y)
    dtsi = (hdl* np.sin(np.ones(365)*latr)*np.sin(sd))+(np.cos(np.ones(365)*latr)*np.cos(sd)*np.sin(hdl))
    ndl=dtsi/np.max(dtsi) # normalized day length

    # calculate mean monthly daylength (used for evapotranspiration in soil moisture calcs)
    jday = cdays[0:12] + .5*ndays[1:13]
    m_star = 1-np.tan(latr)*np.tan(23.439*np.pi/180*np.cos(jday*np.pi/182.625))
    mmm = np.empty(12)
    mmm[:] = np.nan

    for mo in range(12):
        if m_star[mo] < 0:
            mmm[mo] = 0
        elif m_star[mo] >0 and m_star[mo] < 2:
            mmm[mo] = m_star[mo]
        elif m_star[mo] > 2:
            mmm[mo] = 2

    for t in range(12):
        gE[t] = np.mean(ndl[cdays[t]:cdays[t+1]])

    return gE

def nanstd(x, dim=None):
    mask = ~torch.isnan(x)
    count = mask.sum(dim=dim, keepdim=True)
    mean = torch.nanmean(x, dim=dim, keepdim=True)
    var = torch.nansum(((x - mean)**2) * mask, dim=dim, keepdim=True) / count
    return torch.sqrt(var).squeeze() if dim is not None else torch.sqrt(var)