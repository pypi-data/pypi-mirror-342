import numpy as np

class NumericalODESolver(object):
    def __init__(self,f,h,eps):
        self._f = f
        self._h = h
        self._max_h = h
        self._eps = eps

    def step(self,y_k,t_k):
        raise NotImplementedError("Need an ODE Solver")

    def reset(self):
        raise NotImplementedError("reset not defined")

class RK45(NumericalODESolver):
    def step(self,y_k,t_k,tbound,**kwargs):
        #Runge-Kutter-Fehlberg
        #kwargs argument allows for forcing terms (heterogenous ODEs)
        self._h = min(self._h,self._max_h)
        self._h = min(self._h,tbound-t_k)
        k1 = self._h*self._f(t_k,y_k,**kwargs)
        k2 = self._h*self._f(t_k+self._h/4., y_k+k1/4.,**kwargs)
        k3 = self._h*self._f(t_k+3.*self._h/8., y_k+3.*k1/32.+9.*k2/32.,**kwargs)
        k4 = self._h*self._f(t_k+12.*self._h/13.,
                       y_k+1932.*k1/2197.-7200.*k2/2197.+7296.*k3/2197.,**kwargs)
        k5 = self._h*self._f(t_k+self._h,
                       y_k+439.*k1/216.-8.*k2+3680.*k3/513.-845.*k4/4104.,**kwargs)
        k6 = self._h*self._f(t_k+self._h/2.,
                       y_k-8.*k1/27.+2.*k2-3544.*k3/2565.+1859.*k4/4104.-11.*k5/40.,**kwargs)
        y_kp1 = y_k + 25.*k1/216.+1408.*k3/2565.+2197.*k4/4104.-k5/5.
        z_kp1 = y_k + 16.*k1/135.+6656.*k3/12825.+28561.*k4/56430.-9.*k5/50.+2.*k6/55.
        R = np.linalg.norm(y_kp1-z_kp1)/self._h
        delta = (self._eps/(2*R))**(1./4.) if R!=0 else 1
        if R<=self._eps:
            t_k += self._h
            y_k = y_kp1
        self._h *= delta
        return y_k,t_k

    def reset(self):
        self._h = self._max_h

# if __name__ == '__main__':
#     #Test that it works
#     #Test 1
#     h=0.2
#     t=0.
#     w=0.5
#     i=0
#     eps=0.00001
#     def f(t,y):
#         return y-(t**2.)+1.
#     rk45 = RK45(f,h,eps)
#     print("Step %d: t= %6.4f, w=%18.15f"%(i,t,w))
#     while t<2:
#         rk45._h = min(rk45._h,2-t)
#         w,t = rk45.step(w,t)
#         i += 1
#         print("Step %d: t=%6.4f, w=%18.15f"%(i,t,w))
#     #Test 2
#     h=0.2
#     y=0.
#     t=0.
#     i=0
#     eps=2e-5
#     def f2(t,y):
#         return 1.+y**2.
#     rk45 = RK45(f2,h,eps)
#     tbound = 1.4
#     print("Step %d: t= %6.4f, y= %3.8f, true y = %.8f, err= %3.8f"%(i,t,y,np.tan(t),y-np.tan(t)))
#     while t<tbound:
#         rk45._h = min(rk45._h,h)
#         rk45._h = min(rk45._h,tbound-t)
#         y,t = rk45.step(y,t)
#         i += 1
#         print("Step %d: t= %6.4f, y= %3.8f, true y = %.8f, err= %3.8f"%(i,t,y,np.tan(t),y-np.tan(t)))
