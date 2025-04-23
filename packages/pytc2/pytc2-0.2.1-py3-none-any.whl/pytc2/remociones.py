#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:12:53 2023

@author: mariano
"""

import numpy as np

import sympy as sp
from numbers import Real

##########################################
#%% Variables para el análisis simbólico #
##########################################

from .general import s, a_equal_b_latex_s, print_latex, to_latex, print_console_alert


sig = sp.symbols('sig', real=True)
"""
versión simbólica de sigma, parte real de la variable compleja de Laplace
s = σ + j.ω
En caso de necesitar usarla, importar el símbolo desde este módulo.
"""

sig_pos = sp.symbols('sig_pos', real=True, positive = True)
"""
versión simbólica de sigma, parte real positiva de la variable compleja 
de Laplace s = σ + j.ω
En caso de necesitar usarla, importar el símbolo desde este módulo.
"""


##########################################
#%% Funciones generales para la remoción #
##########################################

def tanque_z( doska, omegasq ):
    '''
    Calcula los valores de L y C que componen un tanque resonante LC 
    (tanque Z), a partir del valor del residuo (:math:`2.k`) y la omega al cuadrado 
    (:math:`\\omega^2`) de la expresión de impedancia dada por:
        
    .. math:: Z_{LC} = \\frac{2.k_i.s}{(s^2+\\omega^2_i)} = \\frac{1}{(s.\\frac{1}{2.k_i} + \\frac{1}{s \\frac{2.k_i}{\\omega^2_i} })}

    .. math:: C = \\frac{1}{2.k_i}
        
    .. math:: L = \\frac{2.k_i}{\\omega^2_i}

        
    Parameters
    ----------
    doska : Symbolic
        Dos veces el residuo.
    omegasq : Symbolic
        Cuadrado de la omega a la que el tanque resuena.


    Returns
    -------
    L : Symbolic
        Valor del inductor
    C : Symbolic
        Valor del capacitor


    Raises
    ------
    ValueError
        Si doska u omegasq no son una instancia de sympy.Expr.


    See Also
    --------
    :func:`tanque_y`
    :func:`trim_func_s`
    :func:`isFRP`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import tanque_z
    >>> k, o = sp.symbols('k, o')
    >>> # Sea la siguiente función de excitación
    >>> L, C = tanque_z( k, o )
    >>> print_latex(a_equal_b_latex_s(sp.symbols('L'), L))
    [LaTex formated equation] '$L=\\frac{k}{o}$'
    >>> print_latex(a_equal_b_latex_s(sp.symbols('C'), C))
    [LaTex formated equation] '$C=\\frac{1}{k}$'

    '''
    
    if not ( isinstance(doska, sp.Expr) and isinstance(omegasq, sp.Expr)):
        raise ValueError('Hay que definir doska y omegasq como expresiones simbólicas.')
    
    L = doska/omegasq
    C = 1/doska
    
    return( (L, C) )

def tanque_y( doska, omegasq ):
    '''
    Calcula los valores de L y C que componen un tanque resonante LC 
    (tanque Y), a partir del valor del residuo (:math:`2.k`) y la omega al cuadrado 
    (:math:`\\omega^2`) de la expresión de admitancia dada por:
        
    .. math:: Y_{LC} = \\frac{2.k_i.s}{(s^2+\\omega^2_i)} = \\frac{1}{(s.\\frac{1}{2.k_i} + \\frac{1}{s \\frac{2.k_i}{\\omega^2_i} })}

    .. math:: L = \\frac{1}{2.k_i}
        
    .. math:: C = \\frac{2.k_i}{\\omega^2_i}


    Parameters
    ----------
    doska : Symbolic
        Dos veces el residuo.
    omegasq : Symbolic
        Cuadrado de la omega a la que el tanque resuena.


    Returns
    -------
    L : Symbolic
        Valor del inductor
    C : Symbolic
        Valor del capacitor


    Raises
    ------
    ValueError
        Si doska u omegasq no son una instancia de sympy.Expr.


    See Also
    --------
    :func:`tanque_z`
    :func:`trim_func_s`
    :func:`isFRP`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import tanque_y
    >>> k, o = sp.symbols('k, o')
    >>> # Sea la siguiente función de excitación
    >>> L, C = tanque_y( k, o )
    >>> print_latex(a_equal_b_latex_s(sp.symbols('L'), L))
    [LaTex formated equation] '$C=\\frac{1}{k}$'
    >>> print_latex(a_equal_b_latex_s(sp.symbols('C'), C))
    [LaTex formated equation] '$L=\\frac{k}{o}$'


    '''
    
    if not ( isinstance(doska , sp.Expr) and isinstance(omegasq , sp.Expr)):
        raise ValueError('Hay que definir doska y omegasq como expresiones simbólicas.')
    
    C = doska/omegasq
    L = 1/doska
    
    return( (L, C) )

def trim_poly_s( this_poly, tol = 10**-6 ):
    '''
    Descarta los coeficientes de un polinomio *this_poly* cuyos valores estén por debajo de 
    *tol*.
    

    Parameters
    ----------
    this_poly : Symbolic polynomial
        Expresión simbólica del polinomio a ajustar.
    tol : float
        Mínimo valor permitido para un coeficiente.


    Returns
    -------
    poly_acc : Symbolic
        Polinomio ajustado.


    Raises
    ------
    ValueError
        Si this_poly no es una instancia de sympy.Expr polinomial.
        Si tol no es un flotante.


    See Also
    --------
    :func:`trim_func_s`
    :func:`modsq2mod_s`
    :func:`isFRP`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s
    >>> from pytc2.remociones import trim_poly_s
    >>> this_poly = sp.poly( 1e-10*s**3 + 2*s**2 + s + 1 , s)
    >>> trim_poly = trim_poly_s( this_poly )
    >>> print(trim_poly)
    2.0*s**2 + 1.0*s + 1.0


    '''
    if not ( isinstance(this_poly, sp.polys.polytools.Poly) and isinstance(tol, Real)):
        raise ValueError('Hay que definir this_poly como polinomio simbólico y tol como un flotante.')

    all_terms = this_poly.as_poly(s).all_terms()
    
    poly_acc = 0
    
    for this_pow, this_coeff in all_terms:
    
        if np.abs(this_coeff) > tol:
            
            poly_acc = poly_acc + this_coeff * s**this_pow[0]


    return(poly_acc)

def trim_func_s( rat_func, tol = 10**-6 ):
    '''
    Descarta los coeficientes de una función racional *rat_func* cuyos valores estén por debajo de 
    *tol*.
    

    Parameters
    ----------
    rat_func : Symbolic expresion
        Expresión simbólica de la función racional a ajustar.
    tol : float
        Mínimo valor permitido para un coeficiente.


    Returns
    -------
    trim_func : Symbolic
        Función racional ajustada.


    Raises
    ------
    ValueError
        Si rat_func no es una instancia de sympy.Expr.
        Si tol no es un flotante.


    See Also
    --------
    :func:`trim_poly_s`
    :func:`isFRP`
    :func:`trim_poly_s`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s
    >>> from pytc2.remociones import trim_func_s
    >>> rat_func = ( 1e-10*s**3 + 2*s**2 + s + 1)/( 4.3e-10*s**2 + 2*s + 5)
    >>> trim_func = trim_func_s( rat_func )
    >>> print(trim_func)
    (2.0*s**2 + 1.0*s + 1.0)/(2.0*s + 5.0)


    '''
    if not ( isinstance(rat_func , sp.Expr) and isinstance(tol, Real)):
        raise ValueError('Hay que definir this_poly como una expresión simbólica y tol como un flotante.')

    num, den = rat_func.as_numer_denom()
    
    num = trim_poly_s(sp.poly(num, s), tol)
    den = trim_poly_s(sp.poly(den, s), tol)
    
    return(num/den)

def modsq2mod_s( this_func, bTryNumeric = False ):
    '''
    Esta función halla una función de variable compleja T(s), cuyo módulo se 
    expresa como la factorización:
        
    .. math:: \\vert T(j\\omega) \\vert^2 = T(j\\omega).T(-j\\omega)
    
    .. math:: T(s) = T(j\\omega)\\Big\\vert_{\\omega = s/j}
    
    Es decir que de todas la singularidades presentes en :math:`\\vert T(j\\omega) \\vert^2`, 
    el factor :math:`T(s)` sólo contendrá aquellas que se encuentren en el semiplano izquierdo.

    Parameters
    ----------
    this_func : Symbolic expresion
        Expresión simbólica de la función :math:`\\vert T(j\\omega) \\vert^2` a factorizar.


    Returns
    -------
    trim_func : Symbolic
        Función :math:`T(s)` factorizada.


    Raises
    ------
    ValueError
        Si this_func no es una instancia de sympy.Expr.
    RuntimeError
        Si falla la factorización en T(s)*T(-s)

    See Also
    --------
    :func:`isFRP`
    :func:`trim_func_s`
    :func:`trim_poly_s`


    Examples
    --------
    >>> import sympy as sp 
    >>> from pytc2.general import s
    >>> from pytc2.remociones import modsq2mod_s
    >>> this_func = ( s**2 + sp.Rational(4)) * ( s**2 + sp.Rational(1/15)*s + sp.Rational(1)) / ( s**2 + sp.Rational(1/2)*s + sp.Rational(1)) / ( s**2 + sp.Rational(5)*s + sp.Rational(1)) / (s+sp.Rational(1))
    >>> this_func_sq = sp.simplify(sp.expand(this_func * this_func.subs(s, -s)))
    >>> factor_func = modsq2mod_s( this_func_sq )
    >>> print(factor_func)
    (s**4 + 0.06667*s**3 + 5.0*s**2 + 0.26667*s + 4.0)/(1.0*s**5 + 6.5*s**4 + 10.0*s**3 + 10.0*s**2 + 6.5*s + 1.0)

    '''
            
    if not isinstance(this_func , sp.Expr):
        raise ValueError('Hay que definir this_func como una expresión simbólica.')

    num, den = sp.fraction(this_func)

    # si hubiera signo quedaría para el otro factor.
    k = sp.Abs(sp.poly(num,s).LC() / sp.poly(den,s).LC())

    print(type(num))
    print(num)

    roots_num = sp.roots(num, s)
    
    poly_acc = sp.Rational('1')
    
    ceros_imaginarios_simples = []

    print(type(roots_num))
    print(roots_num)

    for this_root in roots_num.keys():
        
        if sp.re(this_root) < 0:
            # ceros SPI
            
            # multiplicidad
            mult = roots_num[this_root]

            if mult > 1:
                raise ValueError(f'Hallamos un cero complejo con multiplicidad. {this_root:3.3f}')
                # poly_acc *= (s-this_root)**sp.Rational(mult/2)
            else:
                poly_acc *= (s-this_root)

        elif sp.re(this_root) == 0:
            # ceros imaginarios
            
            # multiplicidad
            mult = roots_num[this_root]

            if mult > 1:
                if mult % 2 == 0:
                    poly_acc *= (s-this_root)**sp.Rational(mult/2)
                else:
                    raise ValueError(f'Hallamos un cero imaginario con multiplicidad impar. {this_root:3.3f}')
            else:
                
                ceros_imaginarios_simples.append(this_root)
                # poly_acc *= (s-this_root)

    cant_cerimg = len(ceros_imaginarios_simples)
    
    if cant_cerimg > 0:
        
        if cant_cerimg % 2 == 0:
            
            cerimg = np.unique(np.abs(ceros_imaginarios_simples))
            
            # cerimg_half = cerimg[:cant_cerimg//4]
            cerimg_half = np.flip(cerimg)[:cant_cerimg//4]
            
            for this_cerimg in cerimg_half:
                
                poly_acc *= (s-this_cerimg*sp.I)*(s+this_cerimg*sp.I)
            
        else:
            raise ValueError(f'Hallamos una cantidad impar de ceros imaginarios simples. {this_root:3.3f}')
                
        
    # probamos que hayamos considerado la mitad de las raíces del numerador
    if (len(num.as_poly(s).all_coeffs())-1)/2 != (len(poly_acc.as_poly(s).all_coeffs())-1):
        raise RuntimeError('Falló la factorización de modsq2mod_s. ¡Revisar!')

    if bTryNumeric:
        num = sp.simplify(sp.expand(poly_acc.evalf()))
    else:
        num = sp.simplify(sp.expand(poly_acc))

    roots_den = sp.roots(den)
    
    poly_acc = sp.Rational('1')

    for this_root in roots_den.keys():
        
        if sp.re(this_root) <= 0:
            
            # multiplicidad
            mult = roots_den[this_root]

            if mult > 1:
                poly_acc *= (s-this_root)**sp.Rational(mult/2)
            else:
                poly_acc *= (s-this_root)

    # probamos que hayamos considerado la mitad de las raíces del denominador
    if (len(den.as_poly(s).all_coeffs())-1)/2 != (len(poly_acc.as_poly(s).all_coeffs())-1):
        raise RuntimeError('Falló la factorización de modsq2mod_s. ¡Revisar!')
    
    if bTryNumeric:
        den = sp.simplify(sp.expand(poly_acc.evalf()))
    else:
        den = sp.simplify(sp.expand(poly_acc))

    poly_acc = 0
    
    for each_term in den.as_poly(s).all_terms():
        
        poly_acc += np.abs(each_term[1]) * s**each_term[0][0]

    den = poly_acc

    return(sp.simplify(sp.expand(sp.sqrt(k) * num/den))) 


# TODO: Habrá que seguir analizando la utilidad de estas funciones
# 
# def clasificar_raices(raices_orig):
#     """
#     Clasifica raíces en complejas conjugadas, no conjugadas y pares simétricos respecto al eje imaginario.

#     Parámetros:
#         raices (list or np.ndarray): Lista de raíces obtenidas con np.roots.

#     Retorna:
#         tuple: Tres listas:
#             - Complejas conjugadas.
#             - Raíces no conjugadas.
#             - Pares simétricos respecto al eje imaginario.
#     """
#     # Convertir las raíces en un formato numérico estable (por redondeo de precisión)
#     raices = np.round(raices_orig, decimals=10)  # Redondeamos para evitar problemas numéricos.

#     conjugadas = []
#     no_conjugadas = []
#     pares_simetricos = []

#     usadas = np.zeros_like(raices, dtype=bool)  # Para marcar qué raíces ya procesamos

#     for i, raiz in enumerate(raices):
#         if usadas[i]:  # Si ya usamos esta raíz, la saltamos
#             continue
        
#         conj = np.conj(raiz)  # Conjugada de la raíz actual
#         if np.isclose(raiz.imag, 0):  # Raíz real (imag. casi 0)
#             no_conjugadas.append(-1*np.abs(raices_orig[i].real))
#             usadas[i] = True
#         elif any(np.isclose(conj, raices)):  # Es parte de un par conjugado
#             usadas[i] = True
#             # Marcar su conjugada como usada
#             idx_conj = np.where(np.isclose(conj, raices))[0][0]
#             usadas[idx_conj] = True

#             if np.isclose(raiz.real, 0):  # Raíz real (imag. casi 0)
#                 # en este caso son imaginarias y no hay otro par en SPD    
#                 conjugadas.append(raices_orig[i])
#                 # conjugadas.append(raices_orig[idx_conj])
            
#             else:
#                 # buscamos el otro par en SPD    

#                 # Verificar si tiene par simétrico respecto al eje imaginario
#                 simetrica = -raiz.real + 1j * raiz.imag  # Par simétrico respecto al eje imaginario
#                 simetrica_conj = -raiz.real - 1j * raiz.imag  # Par simétrico respecto al eje imaginario
#                 if any(np.isclose(simetrica, raices)):
#                     # Marcar también la raíz simétrica como usada
#                     idx_sim_1 = np.where(simetrica == raices)[0][0]
#                     usadas[idx_sim_1] = True
#                     idx_sim_2 = np.where(simetrica_conj == raices)[0][0]
#                     usadas[idx_sim_2] = True
#                     # conjugadas.append(raices_orig[idx_sim_1])
#                     # conjugadas.append(raices_orig[idx_sim_2])
#                     pares_simetricos.append( -1*np.abs(raices_orig[i].real) + 1j * raices_orig[i].imag)
#                     # pares_simetricos.append( -1*np.abs(raices_orig[i].real) - 1j * raices_orig[i].imag)

                    
#         else:  # Raíz no conjugada (compleja sin pareja)
#             no_conjugadas.append(raiz)
#             usadas[i] = True

#     return conjugadas, no_conjugadas, pares_simetricos

# def forzar_raices_imaginarias(raices_orig):

#     raices_imaginarias = np.zeros(2*len(raices_orig), dtype = np.complex128 )
#     raices_imaginarias[:-1:2] =  1j * np.abs(raices_orig)
#     raices_imaginarias[1::2] =  -1j * np.abs(raices_orig)
    
#     return(raices_imaginarias)

################################################################
#%% Bloque de funciones para la síntesis gráfica de imitancias #
################################################################

def isFRP( immit ):
    '''
    Chequear si la expresión simbólica immit es una Función Real y Positiva (FRP).


    Parameters
    ----------
    immit : symbolic rational function
        La inmitancia a chequear si es FRP.


    Returns
    -------
    isFRP : boolean
        A boolean with TRUE value if ff is FRP.


    Raises
    ------
    ValueError
        Si this_func no es una instancia de sympy.Expr.


    See Also
    --------
    :func:`remover_polo_dc`
    :func:`remover_polo_infinito`
    :func:`remover_polo_jw`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s
    >>> from pytc2.remociones import isFRP
    >>> immit = (s**2 + 4*s + 3)/(s**2 + 2*s)
    >>> print(isFRP( immit ))
    True
    >>> immit = (s**2 - 4*s + 3)/(s**2 - 2*s)
    >>> print(isFRP( immit ))
    False


    '''   

    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    # F(s) should give real values for all real values of s.
    
    if  (sp.simplify(sp.expand(sp.im(immit.subs(s,sig))))).is_zero and  \
        (sp.simplify(sp.expand(sp.re(immit.subs(s,sig_pos))))).is_nonnegative:

        return(True)
    
    else:
        return(False)
   
        # num, den = immit.as_numer_denom()
        
        # if is_hurwitz(num) and is_hurwitz(den):
        
    # If we substitute s = jω then on separating the real and imaginary parts, 
    # the real part of the function should be greater than or equal to zero, 
    # means it should be non negative. This most important condition and we will 
    # frequently use this condition in order to find out the whether the function 
    # is positive real or not.
    # On substituting s = jω, F(s) should posses simple poles and the residues 
    # should be real and positive.

def remover_polo_sigma( immit, sigma, isImpedance = True,  isRC = True,  sigma_zero = None ):
    '''
    Se removerá el residuo en sobre el eje :math:`\\sigma` (sigma) de la impedancia 
    o admitancia (immit) de forma completa o parcial.
    Como resultado de la remoción total, quedará otra función racional definida
    como:
        
    .. math:: Z_{R} = Z - \\frac{k_i}{s + \\sigma_i}
    
    siendo 

    .. math:: k_i = \\lim\\limits _{s\\to -\\sigma_i} Z (s + \\sigma_i)
    
    Cabe destacar que :math:`Z_{R}` ya no tiene un polo en :math:`\\sigma_i`.
    
    Sin embargo, en cuanto se especifique :math:`\\sigma_z`, la remoción parcial 
    estará definida como:

    .. math:: Z_{R}\\biggr\\rfloor_{s=-\\sigma_z}= 0 = Z - \\frac{k_i}{s + \\sigma_i}\\biggr\\rfloor_{s=-\\sigma_z}
    
    siendo 
    
    .. math:: k_i = Z.(s + \\sigma_i)\\biggr\\rfloor_{s=-\\sigma_z}
    
    Cabe destacar que, para la remoción parcial, :math:`Z_{R}` tendra un cero en 
    :math:`\\sigma_z` y un polo en :math:`\\sigma_i`.
    

    Parameters
    ----------
    immit: Symbolic
        Inmitancia o función que se utilizará para la remoción. Es una función racional 
        simbólica que tendrá un polo de orden 1 en :math:`\\sigma_i`.
    sigma : float
        Frecuencia :math:`\\sigma_i` a la que la inmitancia deberá tener un polo.
    isImpedance : bool
        Booleano que indica si la función immit es una impedancia o admitancia.
    isRC : bool
        Booleano que indica si la función immit es RC o RL.
    sigma_zero : float
        Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
        de la remoción.

    Returns
    -------
    imit_r : Symbolic
        Imitancia luego de la remoción
    kk : Symbolic
        Expresión completa del término removido :math:`\\frac{k_i}{s + \\sigma_i}`.
    R : Symbolic
        Valor del componente resistivo en la remoción.
    CoL : Symbolic
        Valor del componente capacitivo o inductivo en la remoción.
    
        
    Raises
    ------
    ValueError
        Si immit no es una instancia de sympy.Expr.
        Si sigma o sigma_zero no son flotantes.
        Si isImpedance o isRC no son booleanos.


    See Also
    --------
    :func:`remover_polo_dc`
    :func:`remover_polo_infinito`
    :func:`remover_polo_jw`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import remover_polo_sigma
    >>> # Sea la siguiente función de excitación
    >>> ZZ = (s**2 + 13*s + 32)/(2*(s+1)*(s+6))
    >>> # removemos R1-C1
    >>> sigma_R1C1 = -1
    >>> Z4, ZR1C1, R1, C1 = remover_polo_sigma(ZZ, sigma = sigma_R1C1, isImpedance = True, isRC = True )
    >>> print_latex(a_equal_b_latex_s('Z_3', ZR1C1))
    '$Z_3=\\frac{2}{s + 1}$'
    >>> print_latex(a_equal_b_latex_s('Z_4', Z4))
    '$Z_4=\\frac{s + 8}{2 \\left(s + 6\\right)}$'
    
        
    '''

    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    if not isinstance(sigma , (Real, sp.Expr)):
        raise ValueError('Sigma debe ser un flotante.')

    if not isinstance(isImpedance, bool):
        raise ValueError('isImpedance debe ser un booleano.')

    if not isinstance(isRC, bool):
        raise ValueError('isImpedance debe ser un booleano.')

    if not isinstance(sigma_zero , (Real, type(None))):
        raise ValueError('sigma_zero debe ser un flotante o None.')


    if isImpedance:
        zz = immit
    else:
        yy = immit

    sigma = sp.Abs(sigma)

    if sigma_zero is None:
        # remoción total
        
        if isImpedance:
            if isRC:
                kk = sp.limit(zz*(s + sigma), s, -sigma)
            else:
                # RL
                kk = sp.limit(zz*(s + sigma)/s, s, -sigma)
                
        else:
            if isRC:
                kk = sp.limit(yy*(s + sigma)/s, s, -sigma)
            else:
                kk = sp.limit(yy*(s + sigma), s, -sigma)
        
        
        assert (sp.simplify(sp.im(kk)) == sp.Rational('0') and sp.re(kk) >= sp.Rational('0')), 'Residuo en {:3.3f}: {:s}. Verificar Z/Y RC/RL'.format(-sigma, str(kk))
        
        
    else:
        
        sigma_zero = sp.Abs(sigma_zero)
        
        # remoción parcial
        if isImpedance:
            if isRC:
                kk = sp.simplify(sp.expand(zz*(s + sigma))).subs(s, -sigma_zero)
            else:
                kk = sp.simplify(sp.expand(zz*(s + sigma)/s)).subs(s, -sigma_zero)
            
        else:
            if isRC:
                kk = sp.simplify(sp.expand(yy*(s + sigma)/s)).subs(s, -sigma_zero)
            else:
                kk = sp.simplify(sp.expand(yy*(s + sigma))).subs(s, -sigma_zero)

        assert (sp.simplify(sp.im(kk)) == sp.Rational('0') and sp.re(kk) >= sp.Rational('0')), 'Residuo en {:3.3f}: {:s}. Verificar Z/Y RC/RL'.format(-sigma, str(kk))
        
    
    # extraigo kk
    if isImpedance:
        if isRC:
            # Z_RC        
            R = kk/sigma
            CoL = 1/kk
            kk  = kk/(s+sigma)
        else:
            # Z_RL        
            R = kk
            CoL = kk/sigma
            kk  = kk*s/(s+sigma)
        
    else:

        if isRC:
            # Y_RC        
            CoL = kk/sigma
            R = 1/kk
            kk  = kk*s/(s+sigma)
        else:
            # Y_RL
            R = sigma/kk
            CoL = 1/kk
            kk  = kk/(s+sigma)
        

    if isImpedance:
        imit_r = sp.factor(sp.simplify(sp.expand(zz - kk)))
    
    else:
    
        imit_r = sp.factor(sp.simplify(sp.expand(yy - kk)))

    return( [imit_r, kk, R, CoL] )

def remover_polo_jw( immit, omega = None , isImpedance = True, omega_zero = None ):
    '''
    Se removerá el residuo en sobre el eje :math:`j.\\omega` (jota-omega) de la 
    impedancia o admitancia (immit) de forma completa o parcial.
    Como resultado de la remoción total, quedará otra función racional definida
    como:
        
    .. math:: I_{R}=I-\\frac{2.k.s}{s^{2}+\\omega^{2}}
    
    siendo 

    .. math:: 2.k=\\lim\\limits _{s^2\\to-\\omega^2}I\\frac{s^{2}+\\omega^{2}}{s}
    
    Cabe destacar que :math:`I_{R}` ya no tendrá sendos polos complejos conjugados en en :math:`\pm\\omega`.
    
    Sin embargo, en cuanto se especifique :math:`\\omega_z`, la remoción parcial 
    estará definida como:

    .. math:: I_{R}\\biggr\\rfloor_{s^{2}=-\\omega_{z}^{2}}=0=I-\\frac{2.k^{'}.s}{s^{2}+\\omega^{2}}\\biggr\\rfloor_{s^{2}=-\\omega_{z}^{2}}
    
    siendo 
    
    .. math:: 2.k^{'}=I.\\frac{s^{2}+\\omega^{2}}{s}\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}}
    
    Cabe destacar que, para la remoción parcial, :math:`I_{R}` tendra sendos ceros en 
    :math:`\\pm j.\\omega_z` y sendos polos en :math:`\\pm j.\\omega`.
    

    Parameters
    ----------
    immit: Symbolic
        Inmitancia o función que se utilizará para la remoción. Es una función racional 
        simbólica que tendrá un polo de orden 1 en :math:`j\\omega`.
    omega : float
        Frecuencia :math:`\\sigma_i` a la que la inmitancia deberá tener un polo.
    isImpedance : bool
        Booleano que indica si la función immit es una impedancia o admitancia.
    omega_zero : float
        Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
        de la remoción.

    Returns
    -------
    imit_r : Symbolic
        Imitancia luego de la remoción
    kk : Symbolic
        Expresión completa del término removido :math:`\\frac{2.k.s}{s^{2}+\\omega^{2}}`.
    R : Symbolic
        Valor del componente resistivo en la remoción.
    CoL : Symbolic
        Valor del componente capacitivo o inductivo en la remoción.
    
        
    Raises
    ------
    ValueError
        Si immit no es una instancia de sympy.Expr.
        Si sigma o sigma_zero no son flotantes.
        Si isImpedance o isRC no son booleanos.


    See Also
    --------
    :func:`remover_polo_dc`
    :func:`remover_polo_infinito`
    :func:`remover_polo_sigma`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import remover_polo_jw
    >>> # Sea la siguiente función de excitación
    >>> YY = (s * (3*s**2+7) )/((s**2+1)*(s**2+3))
    >>> # removemos R1-C1
    >>> omega_L2C2 = 1
    >>> Y4, Yt2, L2, C2 = remover_polo_jw(YY, isImpedance = False, omega = omega_L2C2 )
    >>> print_latex(a_equal_b_latex_s('Y_3(s)', Yt2))
    '$Y_3(s)=\\frac{2 s}{s^{2} + 1}$'
    >>> print_latex(a_equal_b_latex_s('Y_4(s)', Y4))
    '$Y_4(s)=\\frac{s}{s^{2} + 3}$'

    '''

    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    if not isinstance(omega , (Real, type(None))):
        raise ValueError('Sigma debe ser un flotante.')

    if not isinstance(isImpedance, bool):
        raise ValueError('isImpedance debe ser un booleano.')

    if not isinstance(omega_zero , (Real, type(None))):
        raise ValueError('sigma_zero debe ser un flotante o None.')


    if omega is None:
        # busco el primer polo finito en immit sobre el jw
        
        _, den = (immit).as_numer_denom()
        faux = sp.factor_list(den)
        
        if sp.degree(faux[1][0][0]) == 2:
            
            tt = faux[1][0][0].as_ordered_terms()
            
            # el último término sería omega**2. Cada factor sería
            # s**2 + omega**2
            omega = sp.sqrt(tt[-1])

    if omega_zero is None:
        # remoción total
        # kk = sp.limit(immit*(s**2+omega**2)/s, s**2, -omega**2)
        kk = sp.simplify(sp.expand(immit*(s**2+omega**2)/s)).subs(s**2, -(omega**2) )
        
    else:
        # remoción parcial
        kk = sp.simplify(sp.expand(immit*(s**2+omega**2)/s)).subs(s**2, -(omega_zero**2) )

    
    if isImpedance:
        # Z_LC
        L = kk/omega**2
        C = 1/kk
        
    else:
        # Y_LC
        C = kk/omega**2
        L = 1/kk

    kk = kk * s / (s**2+omega**2)
    
    # extraigo kk
    imit_r = sp.factor(sp.simplify(sp.expand(immit - kk)))

    return( [imit_r, kk, L, C] )

def remover_polo_dc( immit, omega_zero = None, isSigma = False ):
    '''
    Se removerá el residuo en continua (:math:`j.0`) de la 
    impedancia o admitancia (inmitancia o immit) de forma completa o parcial.
    Como resultado de la remoción total, quedará otra función racional definida
    como:
        
    .. math:: I_{R}=I-\\frac{k_0}{s}
    
    siendo 

    .. math:: k_0=\\lim\\limits _{s\\to0}I.s
    
    Cabe destacar que :math:`I_{R}` ya no tendrá polo en :math:`j.0`.
    
    Sin embargo, en cuanto se especifique :math:`\\omega_z`, la remoción parcial 
    estará definida como:

    .. math:: I_{R}\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}}=0=I-\\frac{k_{0}^{'}}{s}\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}}
    
    siendo 
    
    .. math:: k_{0}^{'}=I.s\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}}
    
    Cabe destacar que, para la remoción parcial, :math:`I_{R}` tendra sendos ceros en 
    :math:`\\pm j.\\omega_z` y un polo en :math:`j.0`.
    

    Parameters
    ----------
    immit: Symbolic
        Inmitancia o función que se utilizará para la remoción. Es una función racional 
        simbólica que tendrá un polo de orden 1 en :math:`j\\omega`.
    isSigma : bool
        Booleano que indica si la función immit es una impedancia o admitancia.
    omega_zero : float
        Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
        de la remoción.

    Returns
    -------
    imit_r : Symbolic
        Imitancia luego de la remoción
    k_cero : Symbolic
        Expresión completa del término removido :math:`\\frac{2.k.s}{s^{2}+\\omega^{2}}`.

        
    Raises
    ------
    ValueError
        Si immit no es una instancia de sympy.Expr.
        Si omega_zero no es flotante.
        Si isSigma o isRC no son booleanos.


    See Also
    --------
    :func:`remover_polo_jw`
    :func:`remover_polo_infinito`
    :func:`remover_polo_sigma`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import remover_polo_dc
    >>> # Sea la siguiente función de excitación
    >>> YY = 3*s*(s**2+sp.Rational(7,3))/(s**2+2)/(s**2+5)
    >>> omega_L2C2 = 1
    >>> Z2, Zc1 = remover_polo_dc(1/YY, omega_zero = omega_L2C2 )
    >>> # Zc1 es la admitancia removida
    >>> # extraigo C1
    >>> C1 = 1/(s*Zc1)
    >>> print_latex(a_equal_b_latex_s('Z_1(s)', Zc1))
    $Z_1(s)=\\frac{1}{s}$
    >>> print_latex(a_equal_b_latex_s('Z_2(s)', Z2))
    $Z_2(s)=\\frac{\\left(s^{2} + 1\\right) \\left(s^{2} + 3\\right)}{s \\left(3 s^{2} + 7\\right)}$'

        
    '''
    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    if not isinstance(isSigma, bool):
        raise ValueError('isSigma debe ser un booleano.')

    if not isinstance(omega_zero , (Real, type(None))):
        raise ValueError('sigma_zero debe ser un flotante o None.')


    if omega_zero is None:
        # remoción total
        k_cero = sp.limit(immit*s, s, 0)
        
    else:
        # remoción parcial en el eje j\omega
    	if isSigma is False:
	        k_cero = sp.simplify(sp.expand(immit*s)).subs(s**2, -(omega_zero**2) )

    	# remoción parcial en el eje \sigma
        # Gracias a: David Moharos.
    	else:
	        k_cero = sp.simplify(sp.expand(immit*s)).subs(s, -omega_zero )

    k_cero = k_cero/s
    
    # extraigo C3
    imit_r = sp.factor(sp.simplify(sp.expand(immit - k_cero)))

    return( [imit_r, k_cero] )

def remover_polo_infinito( immit, omega_zero = None, isSigma = False ):
    '''
    Se removerá el residuo en infinito  de la impedancia o admitancia (inmitancia 
    o immit) de forma completa o parcial. Como resultado de la remoción total, 
    quedará otra función racional definida como:
        
    .. math:: I_R = I - s.k_\\infty 
    
    siendo 

    .. math:: k_{\\infty}=\\lim\\limits _{s\\to\\infty}I.\\frac{1}{s}
    
    Cabe destacar que :math:`I_{R}` ya no tendrá polo en :math:`j.\\infty`.
    
    En cuanto se especifique :math:`\\omega_z`, la remoción parcial estará definida 
    como: 

    .. math:: I_{R}\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}}=0=I-s.k_{\\infty}^{'}\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}}
    
    siendo 
    
    .. math:: k_{\\infty}^{'}=I.\\frac{1}{s}\\biggr\\rfloor_{s^{2}=-\\omega_z^{2}} 

    Cabe destacar que, para la remoción parcial, :math:`I_{R}` tendra sendos ceros en 
    :math:`\\pm j.\\omega_z` y un polo en :math:`j.\\infty`. Lo anterior se cumple 
    siempre que isSigma = False, de lo contrario

    .. math:: I_{R}\\biggr\\rfloor_{s=-\\omega_z}=0=I-s.k_{\\infty}^{'}\\biggr\\rfloor_{s=-\\omega_z}
    
    siendo 
    
    .. math:: k_{\\infty}^{'}=I.\\frac{1}{s}\\biggr\\rfloor_{s=-\\omega_z}
    
    Al igual que antes, destacar que para la remoción parcial, :math:`I_{R}` tendrá
    un cero en :math:`-\\sigma_z = \\omega_z` y un polo en :math:`j.\\infty`.
    

    Parameters
    ----------
    immit: Symbolic
        Inmitancia o función que se utilizará para la remoción. Es una función racional 
        simbólica que tendrá un polo de orden 1 en :math:`j\\omega`.
    isSigma : bool
        Booleano que indica si la función immit tiene las singularidades sobre 
        el eje -sigma. Es importante para realizar correctamente las remociones
        parciales, es decir cuando omega_zero NO es None.
    omega_zero : float
        Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
        de la remoción.

    Returns
    -------
    imit_r : Symbolic
        Imitancia luego de la remoción
    k_inf : Symbolic
        Expresión completa del término removido :math:`s.k_{\\infty}`.

        
    Raises
    ------
    ValueError
        Si immit no es una instancia de sympy.Expr.
        Si omega_zero no es flotante.
        Si isSigma o isRC no son booleanos.


    See Also
    --------
    :func:`remover_polo_dc`
    :func:`remover_polo_jw`
    :func:`remover_polo_sigma`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import remover_polo_infinito
    >>> # Sea la siguiente función de excitación
    >>> YY = 3*s*(s**2+sp.Rational(7,3))/(s**2+2)/(s**2+5)
    >>> Z2, Z1 = remover_polo_infinito(1/YY)
    >>> # Z1 es la admitancia removida
    >>> # extraigo L1
    >>> L1 = Z1/s
    >>> print_latex(a_equal_b_latex_s('Z_1(s)', Z1))
    '$Z_1(s)=\\frac{s}{3}$'
    >>> print_latex(a_equal_b_latex_s('Z_2(s)', Z2))
    '$Z_2(s)=\\frac{2 \\cdot \\left(7 s^{2} + 15\\right)}{3 s \\left(3 s^{2} + 7\\right)}$'
        
        
    '''
    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    if not isinstance(isSigma, bool):
        raise ValueError('isSigma debe ser un booleano.')

    if not isinstance(omega_zero , (Real, type(None))):
        raise ValueError('omega_zero debe ser un flotante o None.')


    if omega_zero is None:
        # remoción total
        k_inf = sp.limit(immit/s, s, sp.oo)
        
    else:
        # remoción parcial en el eje j\omega
        if isSigma is False:
        	k_inf = sp.simplify(sp.expand(immit/s)).subs(s**2, -(omega_zero**2) )
	
    	# remoción parcial en el eje \sigma
        # Gracias David Moharos!
        else:
        	k_inf = sp.simplify(sp.expand(immit/s)).subs(s, -omega_zero )		

    k_inf = k_inf * s

    # extraigo C3
    imit_r = sp.factor(sp.simplify(sp.expand(immit - k_inf)))

    return( [imit_r, k_inf] )

def remover_valor_en_infinito( immit, sigma_zero = None ):
    '''
    Se removerá un valor real de la impedancia o admitancia (inmitancia 
    o immit) de forma completa o parcial. Como resultado de la remoción total, 
    quedará otra función racional definida como:
        
    .. math:: I_R = I - k_\\infty 
    
    siendo 

    .. math:: k_{\\infty}=\\lim\\limits _{s\\to\\infty}I
    
    En cuanto se especifique :math:`\\sigma_z`, la remoción parcial estará definida 
    como: 

    .. math:: I_{R}\\biggr\\rfloor_{s=-\\sigma_z}=0=I-k_{\\infty}^{'}\\biggr\\rfloor_{s=-\\sigma_z}
    
    siendo 
    
    .. math:: k_{\\infty}^{'}=I\\biggr\\rfloor_{s=-\\sigma_z} 

    Cabe destacar que, para la remoción parcial, :math:`I_{R}` tendra un cero en 
    :math:`-\\sigma_z` y un valor real en :math:`\\infty`. 

    Parameters
    ----------
    immit: Symbolic
        Inmitancia o función que se utilizará para la remoción. Es una función racional 
        simbólica que tendrá un polo de orden 1 en :math:`j\\omega`.
    sigma_zero : float
        Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
        de la remoción.

    Returns
    -------
    imit_r : Symbolic
        Imitancia luego de la remoción
    k_inf : Symbolic
        Expresión completa del término removido :math:`s.k_{\\infty}`.

        
    Raises
    ------
    ValueError
        Si immit no es una instancia de sympy.Expr.
        Si sigma_zero no es flotante.


    See Also
    --------
    :func:`remover_valor_en_dc`
    :func:`remover_polo_en_infinito`
    :func:`remover_polo_en_dc`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import remover_valor_en_infinito
    >>> # Sea la siguiente función de excitación
    >>> ZZ = (s**2 + 13*s + 32)/(3*s**2 + 27*s+ 44)
    >>> Z2, Z1 = remover_valor_en_infinito(ZZ)
    >>> print_latex(a_equal_b_latex_s('Z_1(s)', Z1))
    '$Z_1(s)=\\frac{1}{3}$'
    >>> print_latex(a_equal_b_latex_s('Z_2(s)', Z2))
    '$Z_2(s)=\\frac{4 \\cdot \\left(3 s + 13\\right)}{3 \\cdot \\left(3 s^{2} + 27 s + 44\\right)}$'
    
            
    '''
    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    if not isinstance(sigma_zero , (Real, type(None))):
        raise ValueError('sigma_zero debe ser un flotante o None.')


    if sigma_zero is None:
        # remoción total
        k_inf = sp.limit(immit, s, sp.oo)
        
    else:
        # remoción parcial
        k_inf = sp.simplify(sp.expand(immit)).subs(s, - sp.Abs(sigma_zero) )


    assert not k_inf.is_negative, 'Residuo negativo. Verificar Z/Y RC/RL'

    rem_aux = immit - k_inf
    
    bFRP = isFRP(rem_aux)
    
    if bFRP:

        rem = rem_aux
        # extraigo k_inf
        imit_r = sp.factor(sp.simplify(sp.expand( rem )))

    else:    
        # falla la remoción        
        # error
        print_console_alert('Fallo la remoción en infinito')

        print( 'Se intentó remover el valor:')
        
        print_latex(a_equal_b_latex_s('k_{\infty}', k_inf))

        imit_r = immit
        k_inf = s*0

    return( [imit_r, k_inf] )

def remover_valor_en_dc( immit, sigma_zero = None):
    '''
    Se removerá un valor constante en continua (s=0) de la imitancia (immit) de forma 
    completa. Como resultado de la remoción, quedará otra función racional definida
    como:
        
    .. math:: I_R = I - k_0 
    
    siendo 

    .. math:: k_0 = \\lim\\limits _{s \\to 0}I 
    
    En cuanto se especifique :math:`\\sigma_z`, la remoción parcial estará definida 
    como: 

    .. math:: I_{R}\\biggr\\rfloor_{s=-\\sigma_z}=0=I-k_{0}^{'}\\biggr\\rfloor_{s=-\\sigma_z}
    
    siendo 
    
    .. math:: k_{0}^{'}=I\\biggr\\rfloor_{s=-\\sigma_z} 

    Cabe destacar que, para la remoción parcial, :math:`I_{R}` tendra un cero en 
    :math:`-\\sigma_z` y un valor real en 0. 

    Parameters
    ----------
    immit: Symbolic
        Inmitancia o función que se utilizará para la remoción. Es una función racional 
        simbólica que tendrá un polo de orden 1 en :math:`j\\omega`.
    sigma_zero : float
        Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
        de la remoción.

    Returns
    -------
    imit_r : Symbolic
        Imitancia luego de la remoción
    k_0 : Symbolic
        Expresión completa del término removido :math:`k_0`.

        
    Raises
    ------
    ValueError
        Si immit no es una instancia de sympy.Expr.
        Si sigma_zero no es flotante.


    See Also
    --------
    :func:`remover_valor_en_infinito`
    :func:`remover_polo_en_infinito`
    :func:`remover_polo_en_dc`


    Examples
    --------
    >>> import sympy as sp
    >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
    >>> from pytc2.remociones import remover_valor_en_dc
    >>> # Sea la siguiente función de excitación
    >>> ZZ = (s**2 + 13*s + 32)/(3*s**2 + 27*s+ 44)
    >>> Z2, Z1 = remover_valor_en_dc(1/ZZ)
    >>> print_latex(a_equal_b_latex_s('Z_1(s)', Z1))
    :math:`$Z_1(s)=\\frac{11}{8}$`
    >>> print_latex(a_equal_b_latex_s('Z_2(s)', Z2))
    :math:`$Z_2(s)=\\frac{s \\left(13 s + 73\\right)}{8 \\left(s^{2} + 13 s + 32\\right)}$`
    
    '''

    if not isinstance(immit , sp.Expr):
        raise ValueError('Hay que definir immit como una expresión simbólica.')

    if not isinstance(sigma_zero , (Real, type(None))):
        raise ValueError('sigma_zero debe ser un flotante o None.')

    if sigma_zero is None:
        # remoción total
        k0 = sp.limit(immit, s, 0)
        
    else:
        # remoción parcial
        k0 = sp.simplify(sp.expand(immit)).subs(s, - sp.Abs(sigma_zero) )

    assert not k0.is_negative, 'Residuo negativo. Verificar Z/Y RC/RL'
    
    # extraigo k0
    imit_r = sp.factor(sp.simplify(sp.expand(immit - k0)))

    return( [imit_r, k0] )

# TODO: revisar la utilidad de la función "remover_valor". Podría ser removida.

# def remover_valor( immit, sigma_zero):
#     '''
#     Se removerá un valor real de la impedancia o admitancia (inmitancia 
#     o immit) de forma completa o parcial. Como resultado de la remoción total, 
#     quedará otra función racional definida como:
        
#     .. math:: I_R = I - k_\\infty 
    
#     siendo 

#     .. math:: k_{\\infty}=\\lim\\limits _{s\\to\\infty}I
    
#     En cuanto se especifique :math:`\\sigma_z`, la remoción parcial estará definida 
#     como: 

#     .. math:: I_{R}\\biggr\\rfloor_{s=-\\sigma_z}=0=I-k_{\\infty}^{'}\\biggr\\rfloor_{s=-\\sigma_z}
    
#     siendo 
    
#     .. math:: k_{\\infty}^{'}=I\\biggr\\rfloor_{s=-\\sigma_z} 

#     Cabe destacar que, para la remoción parcial, :math:`I_{R}` tendra un cero en 
#     :math:`-\\sigma_z` y un valor real en :math:`\\infty`. 

#     Parameters
#     ----------
#     immit: Symbolic
#         Inmitancia o función que se utilizará para la remoción. Es una función racional 
#         simbólica que tendrá un polo de orden 1 en :math:`j\\omega`.
#     sigma_zero : float
#         Frecuencia :math:`\\sigma_z` a la que la inmitancia tendrá un cero luego 
#         de la remoción.

#     Returns
#     -------
#     imit_r : Symbolic
#         Imitancia luego de la remoción
#     k_inf : Symbolic
#         Expresión completa del término removido :math:`s.k_\\infty `.

        
#     Raises
#     ------
#     ValueError
#         Si immit no es una instancia de sympy.Expr.
#         Si sigma_zero no es flotante.


#     See Also
#     --------
#     :func:`remover_polo_dc`
#     :func:``
#     :func:``


#     Examples
#     --------
#     >>> import sympy as sp
#     >>> from pytc2.general import s, a_equal_b_latex_s, print_latex
#     >>> from pytc2.remociones import remover_valor
#     >>> # Sea la siguiente función de excitación
#     >>> ZZ = (s**2 + 13*s + 32)/(3*s**2 + 27*s+ 44)
#     >>> Z2, Z1 = remover_valor(ZZ)
#     >>> print_latex(a_equal_b_latex_s('Z_1(s)', Z1))
#     '$Z_1(s)=\\frac{s}{3}$'
#     >>> print_latex(a_equal_b_latex_s('Z_2(s)', Z2))
#     '$Z_2(s)=\\frac{2 \\cdot \\left(7 s^{2} + 15\\right)}{3 s \\left(3 s^{2} + 7\\right)}$'
        

# print_latex(a_equal_b_latex_s('Y_B', YB))
# print_latex(a_equal_b_latex_s('Y_6', Y6))
    
            
#     '''

#     if not isinstance(immit , sp.Expr):
#         raise ValueError('Hay que definir immit como una expresión simbólica.')

#     if not isinstance(sigma_zero , Real):
#         raise ValueError('sigma_zero debe ser un flotante o None.')

#     # remoción parcial
#     k_prima = sp.simplify(sp.expand(immit)).subs(s, -sp.Abs(sigma_zero))
    
#     rem_aux = immit - k_prima
    
#     bFRP = isFRP(rem_aux)
    
#     if bFRP:
        
#         rem = rem_aux

#         # extraigo k_prima
#         imit_r = sp.factor(sp.simplify(sp.expand( rem )))
        
#     else:    
#         # falla la remoción        
#         # error
#         print_console_alert('Fallo la remoción')

#         print( 'Se intentó remover el valor:')
        
#         print_latex(a_equal_b_latex_s('k', k_prima))

#         imit_r = immit
#         k_prima = s*0

#     return( [imit_r, k_prima] )
