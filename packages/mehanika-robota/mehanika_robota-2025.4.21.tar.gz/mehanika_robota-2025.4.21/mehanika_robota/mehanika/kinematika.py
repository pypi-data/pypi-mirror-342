"""
Kinematika
==========
Modul za odredjivanje kinematike robota, sto podrazumeva:\n
- direktnu kinematiku,\n
- jakobijan,\n
- parametri manipulabilnosti,\n
- inverzna kinematika,\n
- orgininalna Paden-Kahanova podproblema sa prosirenim drugim podproblemom za
slucaj paralelnih osa koje se ne ukrstaju i\n
- prva tri Pardos-Gotorova podproblema.\n

Funkcije rade i sa prostornim koordinatama i koordinatama hvataca.

Preporucen nacin uvoza modula je
>>> import mehanika_robota.mehanika.kinematika as kin
"""

"""
*** BIBLIOTEKE ***
"""
import numpy as np
from numpy.typing import NDArray
from mehanika_robota.mehanika import mat_prostor as mp
from mehanika_robota import _alati
from typing import Any, Literal, Optional, Sequence, Tuple
from collections import namedtuple
import warnings

"""
*** PRIVATNE FUNKCIJE ***
"""
def _vek_proj3(
    u: NDArray[np.float64],
    v: NDArray[np.float64]
) -> NDArray[np.float64]:
    # Funkcija koja vektorski projektuje 3D vektore `u` na `v`.
    # Vektori mogu biti dimenzije 3x1 i 1x3.
    # Izlazni vektor je dimenzije vektora `v`
    
    return v*np.dot(u.reshape(3), v.reshape(3))/np.linalg.norm(v)**2

"""
*** API KLASE ***
"""
Manip = namedtuple("Manip", ['V', "kond_broj"])
"""Klasa koja sadrzi osnovne informacije o manipulabilnosti robota. Klasa je
namedtuple koji je odredjen na osnovu karakteristike matrice `A = J@J.T` i
sadrzi atribute:

V : np.float64
    Proporcionalna zapremina elipsoida manipulabilnosti koji je odredjen kao
    `np.sqrt(np.linalg.det(A))`

kond_broj : np.float64
    Kondicijski broj koji je odredjen kao `np.linalg.cond(A)`
"""

class InvKinError(Exception):
    """Greska kada inverzna kinematika nema resenja
    """
    pass

class PadenKahanError(Exception):
    """Greska kada neki Paden-Kahanov podproblem nema resenja
    """
    def __init__(
        self,
        broj_podproblema: Literal[1, 2, 3],
        objekat: Optional[Any] = None
    ) -> None:
        """Poruka greske u formatu:
        f"{broj_podproblema}. Paden-Kahanov podproblem nema resenja. {objekat}"
        
        broj_podproblema : Literal[1, 2, 3]
            Redni broj Paden-Kahanovog podproblema
        objekat : Any, opcionalno
            Dodatni objekat koji ima dunder __repr__ ili __str__ za dodatan
            opis greske (automatska vrednost je None, tj. nema dodatne poruke)
        """
        if broj_podproblema not in (1, 2, 3):
            raise ValueError(
                "Invalidan \"broj_podproblema\", postoje samo podproblemi od "
                "1 do 3"
            )
        
        if objekat is None:
            self._poruka =  f"{broj_podproblema}. " \
                + "Paden-Kahanov podproblem nema resenja"
        else:
            self._poruka =  f"{broj_podproblema}. " \
                + "Paden-Kahanov podproblem nema resenja. " \
                + f"{objekat}"
            
        super().__init__(self._poruka)
        
    def __repr__(self) -> str:
        return self._poruka

class PardosGotorError(Exception):
    """Greska kada neki Pardos-Gotor podproblem nema resenja
    """
    def __init__(
        self,
        broj_podproblema: Literal[1, 2, 3],
        objekat: Optional[Any] = None
    ) -> None:
        """Poruka greske u formatu:
        f"{broj_podproblema}."
        f"Pardos-Gotorov podproblem nema resenja. {objekat}"
        
        broj_podproblema : Literal[1, 2, 3]
            Redni broj Pardos-Gotorovog podproblema
        objekat : Any, opcionalno
            Dodatni objekat koji ima dunder __repr__ ili __str__ za dodatan
            opis greske (automatska vrednost je None, tj. nema dodatne poruke)
        """
        if broj_podproblema not in (1, 2, 3):
            raise ValueError(
                "Invalidan \"broj_podproblema\", postoje samo podproblemi od "
                "1 do 3"
            )
        
        if objekat is None:
            self._poruka =  f"{broj_podproblema}. " \
                + "Pardos-Gotorov podproblem nema resenja"
        else:
            self._poruka =  f"{broj_podproblema}. " \
                + "Pardos-Gotorov podproblem nema resenja. " \
                + f"{objekat}"
            
        super().__init__(self._poruka)
        
    def __repr__(self) -> str:
        return self._poruka

"""
*** API FUNKCIJE ***
"""
def dir_kin(
    M: Sequence | NDArray,
    S_lista: Sequence | NDArray,
    teta_lista: Sequence | NDArray | np.int32 | np.float64,
    koord_sistem_prostor: bool = True,
    vek_kolona: bool = False
) -> NDArray[np.float64]:
    """Odredjuje direktnu kinematiku gde su parametri proracuna u prostornom
    koordinatnom sistemu ili u koordinatnom sistemu zakacen za telo od
    interesa. Proracun je namenjen za robote sa otvorenim kinematskim lancem

    Parametri
    ---------
    M : Sequence | NDArray
        Pocetna konfiguracija (orijentacija i pozicija) hvataca robota kada
        su svi zglobovi u svojoj nultoj, odnosno pocetnoj, poziciji. Matrica je
        iz grupe SE(3)
    S_lista : Sequence | NDArray
        Spisak/lista ose zavrtnja svih zglobova robota kada je robot u svojoj
        pocetnoj konfiguraciji. Zavisno od parametra `vek_kolona`, individualne
        ose zavrtnjeva mogu biti u obliku vektora kolone (`vek_kolona` je True)
        ili u obliku vektora reda (`vek_kolona` je False). Dimenzije su nx6
        kada je `vek_kolona` False i 6xn kada je `vek_kolona` True, gde je n
        broj vektora ose zavrtnja S. Ose zavrtnja ne moraju biti normirane,
        tj. svejedno je da li je `S_lista` sastavljena od ose zavrtnja, vektora
        prostornih brzina ili neke kombinacije istih
    teta_lista : Sequence | NDArray | np.int32 | np.float64
        Spisak/lista uglova rotacije zglobova (u slucaju da neka osa
        predstavlja iskljucivo linearno kretanje, teta za taj zglob predstavlja
        duzinu linearnog kretanja). Dimenzije su 1xn ili nx1 gde je n broj
        vektora ose zavrtnja  U slucaju da je `S_lista` dimenzije 6x1 ili 1x6
        onda `teta_lista` ne mora biti niz tipa Sequence ili NDArray
    koord_sistem_prostor : bool, opcionalno
        Odredjuje da li se ose zavrtnjeva iz `S_lista` smatra da su definise u
        prostornom koordinatnom sistemu ili u koordinatnom sistemu zakacen za
        telo od interesa (automatska vrednost je True) 
    vek_kolona : bool, opcionalno
        Odredjuje nacin prikazivanja ose zavrtnja unutar `S_lista` (automatska
        vrednost je False). Kada je `vek_kolona` False onda elementi spiska ose
        zavrtnja (ose zavrtnja za individualne zglobove) se smatraju da su
        poredjani po redovima, inace se smatra da su poredjani po kolonama 

    Povratna vrednost
    -----------------
    NDArray[np.float64]
        Homogena transformaciona matrica iz grupe SE(3) koja predstavlja
        konfiguraciju robota u prostornom koordinatnom sistemu

    Greske
    ------
    ValueError
        Nepravilne dimenzije ulaznih parametara
    
    Primeri
    -------
    >>> M = [[-1, 0,  0, 0],
             [ 0, 1,  0, 6],
             [ 0, 0, -1, 2],
             [ 0, 0,  0, 1]]
    >>> S_lista_prostor = [[0, 0,    0],
                           [0, 0,    0],
                           [1, 0,   -1],
                           [4, 0,   -6],
                           [0, 3,    0],
                           [0, 0, -0.1]]
    >>> teta_lista = [np.pi / 2, 3, np.pi]
    >>> dir_kin(M, S_lista_prostor, teta_lista, vek_kolona=True)
    np.array([[0.0, 1.0,  0.0,  -5.0],
              [1.0, 0.0,  0.0,   4.0],
              [0.0, 0.0, -1.0, 1.686],
              [0.0, 0.0,  0.0,   1.0]])
    >>> S_lista_telo = [[0, 0, -1, 2, 0,   0],
                        [0, 0,  0, 0, 1,   0],
                        [0, 0,  1, 0, 0, 0.1]]
    >>> dir_kin(M, S_lista_telo, teta_lista, koord_sistem_prostor=False)
    np.array([[0.0, 1.0,  0.0,  -5.0],
              [1.0, 0.0,  0.0,   4.0],
              [0.0, 0.0, -1.0, 1.686],
              [0.0, 0.0,  0.0,   1.0]])
    """
    T = np.array(M, dtype=float)
    _alati._mat_provera(T, (4, 4), 'M')
    
    # Lista uglova mora biti u obliku 1D niza
    S_lista = np.array(S_lista, dtype=float)
    teta_lista = np.atleast_1d(np.array(teta_lista, dtype=float))
    
    # Algoritam je napravljen da funkcionise sa matricom `S_lista`
    if S_lista.ndim == 1:
        S_lista = S_lista[np.newaxis, :]
        
    # Za proracun sa smatra da je `S_lista` matrica gde su ose zavrtnja vektori
    # kolone. Zato, ako je uneta `S_lista` gde su ose zavrtnja vektori reda,
    # transponovati `S_lista`
    if not vek_kolona:
        S_lista = S_lista.T
        
    # Proveri da li vektori iz `S_lista` imaju 6 komponenti i da li
    # `teta_lista` ima elemenata koliko `S_lista` ima vektora
    _alati._mat_provera(S_lista, (6, S_lista.shape[1]), "S_lista")
    _alati._vek_provera(teta_lista, S_lista.shape[1], "teta_lista")
        
    # Normirati vektore ose zavrtnja
    S_lista = np.apply_along_axis(mp.v_prostor_norm, 0, S_lista)

    if koord_sistem_prostor:
        for i in range(teta_lista.shape[0] - 1, -1, -1):
            T = mp.exp(
                mp.lijeva_algebra_od_vek(teta_lista[i]*S_lista[:, i])
            ) @ T
    else:
        for i in range(teta_lista.shape[0]):
            T = T @ mp.exp(
                mp.lijeva_algebra_od_vek(teta_lista[i]*S_lista[:, i])
            )        

    return T

def jakobijan(
    S_lista: Sequence | NDArray,
    teta_lista: Optional[
        Sequence | NDArray | np.int32 | np.float64
    ] = None,
    koord_sistem_prostor: bool = True,
    vek_kolona: bool = False
) -> NDArray[np.float64]:
    """Odredjuje Jakobijan u prostornom koordinatnom sistemu ili u
    koordinatnom sistemu zakacen za telo od interesa. Proracun je namenjen za
    robote sa otvorenim kinematskim lancem

    Parametri
    ---------
    S_lista : Sequence | NDArray
        Spisak/lista ose zavrtnja svih zglobova robota kada je robot u svojoj
        pocetnoj konfiguraciji. Zavisno od parametra `vek_kolona`, individualne
        ose zavrtnjeva mogu biti u obliku vektora kolone (`vek_kolona` je True)
        ili u obliku vektora reda (`vek_kolona` je False). Dimenzije su nx6
        kada je `vek_kolona` False i 6xn kada je `vek_kolona` True, gde je n
        broj vektora ose zavrtnja S. Ose zavrtnja ne moraju biti normirane,
        tj. svejedno je da li je `S_lista` sastavljena od ose zavrtnja, vektora
        prostornih brzina ili neke kombinacije istih
    teta_lista : Optional[Sequence | NDArray | int | float | np.int32 |
    np.float64], opcionalno
        Spisak/lista uglova rotacije zglobova (u slucaju da neka osa
        predstavlja iskljucivo linearno kretanje, teta za taj zglob predstavlja
        duzinu linearnog kretanja). Dimenzije su 1x(n - 1) ili (n - 1)x1 gde je
        n broj vektora ose zavrtnja. U slucaju da je `len(S_lista) == 1` onda
        `teta_lista` mora biti `teta_lista == None` (automatska vrednost je
        None). Ukoliko `teta_lista` se sastoji od jednog elementa, parametar
        ne mora biti niz tipa Sequence ili NDArray
    koord_sistem_prostor : bool, opcionalno
        Odredjuje da li se ose zavrtnjeva iz `S_lista` smatra da su definise u
        prostornom koordinatnom sistemu ili u koordinatnom sistemu zakacen za
        telo od interesa (automatska vrednost je True) 
    vek_kolona : bool, opcionalno
        Odredjuje nacin prikazivanja ose zavrtnja unutar `S_lista` (automatska
        vrednost je False). Kada je `vek_kolona` False onda elementi spiska ose
        zavrtnja (ose zavrtnja za individualne zglobove) se smatraju da su
        poredjani po redovima, inace se smatra da su poredjani po kolonama 

    Povratna vrednost
    -----------------
    NDArray
        Geometrijski jakobijan dimenzije 6xm gde je `m == len(S_lista)
        == len(teta_lista) + 1`

    Greske
    ------
    ValueError
        Nepravilne dimenzije ulaznih parametara
    
    Primeri
    -------
    >>> jakobijan([9, 0, 0, 0, 0, 9])
    np.array([[1.0],
              [0.0],
              [0.0],
              [0.0],
              [0.0],
              [1.0]])
    >>> jakobijan([[1, 0, 0, 0, 0, 1],
                   [0, 0, 0, 2, 3, 0]], 2.3)
    np.array([[1.0,    0.0],
              [0.0,    0.0],
              [0.0,    0.0],
              [0.0,  0.555],
              [0.0, -0.554],
              [1.0,  0.620]])
    >>> jakobijan(
        [[0,   1,  0,   1],
         [0,   0,  5,   0],
         [1,   0,  0,   0],
         [0,   2,  0, 0.2],
         [0.2, 0, 10, 0.3],
         [0.2, 3,  5, 0.4]],
        [0.2, 1.1, 0.1],
        vek_kolona=True     
    )
    np.array([[0.0, 0.980, -0.090,  0.957],
              [0.0, 0.199,  0.445,  0.285],
              [1.0,   0.0,  0.891, -0.045],
              [0.0, 1.952, -2.216, -0.512],
              [0.2, 0.437, -2.437,  2.775],
              [0.2, 2.960,  3.236,  2.225]])
    >>> jakobijan(
        [[0, 0, 1,   0, 0.2, 0.2],
         [1, 0, 0,   2,   0,   3],
         [0, 1, 0,   0,   2,   1],
         [1, 0, 0, 0.2, 0.3, 0.4]],
        [[1.1],
         [0.1],
         [1.2]],
        koord_sistem_prostor=False
    )
    np.array([[-0.045,  0.995,    0.0, 1.0],
              [ 0.744,  0.093,  0.362, 0.0],
              [-0.667,  0.036, -0.932, 0.0],
              [ 2.326,  1.668,  0.564, 0.2],
              [-1.443,  2.946,  1.433, 0.3],
              [-2.066,  1.828, -1.589, 0.4]])
    """
    T = np.eye(4)
    S_lista = np.array(S_lista, dtype=float)

    # Algoritam je napravljen da funkcionise sa matricom `S_lista`
    if S_lista.ndim == 1:
        S_lista = S_lista[np.newaxis, :]
        
    # Za proracun sa smatra da je `S_lista` matrica gde su ose zavrtnja vektori
    # kolone. Zato, ako je uneta `S_lista` gde su ose zavrtnja vektori reda,
    # transponovati `S_lista`
    if not vek_kolona:    
        S_lista = S_lista.T

    # Ukoliko je `teta_lista` prazno, onda proveriti da li je dat iskljucivo
    # jedan vektor ose zavrtnja i upravo taj vektor predstavlja jakobijan 
    # 
    # Provera da li vektori iz `S_lista` imaju 6 komponenti i da li 
    # `teta_lista` ima elemenata koliko `S_lista` ima vektora
    if teta_lista is None:
        _alati._mat_provera(S_lista, (6, 1), "S_lista")
        return mp.v_prostor_norm(S_lista)
    else:
        _alati._mat_provera(S_lista, (6, S_lista.shape[1]), "S_lista")
        
        # Lista uglova mora biti u obliku 1D niza
        teta_lista = np.atleast_1d(np.array(teta_lista, dtype=float))

        _alati._vek_provera(teta_lista, S_lista.shape[1] - 1, "teta_lista")
        
    # Normirati vektore ose zavrtnja
    S_lista = np.apply_along_axis(mp.v_prostor_norm, 0, S_lista)

    J = S_lista.copy()

    if koord_sistem_prostor:
        for i in range(teta_lista.shape[0]):
            T = T @ mp.exp(
                mp.lijeva_algebra_od_vek(teta_lista[i]*S_lista[:, i])
            )
            J[:, i + 1] = mp.Ad(T) @ J[:, i + 1]
    else:
        for i in range(teta_lista.shape[0] - 1, -1, -1):
            T = T @ mp.exp(
                mp.lijeva_algebra_od_vek(-teta_lista[i]*S_lista[:, i + 1])
            )        
            J[:, i] = mp.Ad(T) @ J[:, i]

    return J

def manip(
    J: Sequence | NDArray,
    tip_jakob: Literal['J', "J_omega", "J_v"] = 'J',
    elipsoid_sile = False
) -> Manip:
    """Odredjuje parametre manipulabilnosti Jakobijana-proporcionalna zapremina
    elipsoida manipulabilnosti i kondicijski broj

    Parametri
    ---------
    J : Sequence | NDArray
        Geometrijski jakobijan dimenzije 6xn

    Povratna vrednost
    -----------------
    Manip
        namedtuple objekat koji je odredjen na osnovu karakteristike matrice
        `A = J@J.T` i sadrzi atribute:

    V : np.float64
        Proporcionalna zapremina elipsoida manipulabilnosti koji je odredjen
        kao `np.sqrt(np.linalg.det(A))`

    kond_broj : np.float64
        Kondicijski broj koji je odredjen kao `np.linalg.cond(A)`

    Greske
    ------
    ValueError
        Nepravilne dimenzije Jakobijana
    
    Primeri
    -------
    >>> J = [[0, 0, 0, 0, 1, 0],
             [0, 0, 0, 1, 0, 0],
             [1, 1, 1, 0, 0, 0],
             [2, 0, 0, 4, 5, 0],
             [0, 2, 3, 0, 5, 0],
             [0, 1, 3, 4, 0, 1]]
    >>> manip(J)
    Manip(V=np.float64(2.0), kond_broj=np.float64(49055.5030446))
    >>> manip(J, "J_omega")
    Manip(V=np.float64(1.73205080757), kond_broj=np.float64(3.0))
    >>> manip(J, "J_v")
    Manip(V=np.float64(151.400132100), kond_broj=np.float64(4.90676068982))
    >>> manip(J, ellipsoid_sile=True)
    Manip(V=np.float64(0.5), kond_broj=np.float64(49055.5030446))
    >>> manip(J, "J_omega", True)
    Manip(V=np.float64(0.57735026919), kond_broj=np.float64(3.0))
    >>> manip(J, "J_v", True)
    Manip(V=np.float64(0.00660501405), kond_broj=np.float64(4.90676068982))
    >>> manip(J).V*manip(J, ellipsoid_sile=True).V
    np.float64(1.0) 
    >>> J3 = [[0, 0, 0],
              [0, 0, 0],
              [1, 1, 1],
              [2, 0, 0],
              [0, 2, 3],
              [0, 1, 3]]
    >>> manip(J3)
    Manip(V=np.float64(0.0), kond_broj=np.inf)
    >>> manip(J3, 'J_omega')
    Manip(V=np.float64(0.0), kond_broj=np.inf)
    >>> manip(J3, 'J_v')
    Manip(V=np.float64(6.0), kond_broj=np.float64(56.7601597865))
    >>> manip(J3, elipsoid_sile=True)
    Manip(V=np.inf, kond_broj=np.float64(0))
    >>> manip(J3, "J_omega", True)
    Manip(V=np.inf, kond_broj=np.float64(0))
    >>> manip(J3, "J_v", True)
    Manip(V=np.float64(0.166666666666), kond_broj=np.float64(56.7601597865))
    """
    J = np.array(J, dtype=float)
    
    _alati._mat_provera(J, (6, J.shape[1]), 'J')
    if not np.allclose(
        J,
        np.apply_along_axis(mp.v_prostor_norm, 0, J)
    ):
        raise ValueError(
            "Kolone Jakobijana \"J\" nisu ose zavrtnja, tj. normirane"
        )
        
    match tip_jakob:
        case 'J':
            pass
        case "J_omega":
            J = np.array(J)[:3]
        case "J_v":
            J = np.array(J)[3:]
        case _:
            raise ValueError(
                "Nepoznat tip Jakobijana \"tip_jakob\", unesite \"J\", "
                "\"J_omega\" ili \"J_v\""
            )

    det = np.linalg.det(J@J.T)

    # Za matricu A = J@J.T i B = np.linalg.inv(A) vazi da je
    # np.linalg.det(A)  == 1/np.linalg.det(B) (sto je korisno kada je B
    # singularna matrica) i np.linalg.cond(A) == np.linalg.cond(B).
    if np.isclose(det, 0.0):
        return Manip(
            np.inf if elipsoid_sile else np.float64(0.0),
            np.inf
        )
    else:
        return Manip(
            np.sqrt(1/det if elipsoid_sile else det),
            np.linalg.cond(J@J.T)
        )    

def inv_kin(
    M: Sequence | NDArray,
    S_lista: Sequence | NDArray,
    teta_lista0: Sequence | NDArray | np.int64 | np.float64,
    Tk: Sequence | NDArray,
    tol_omega: np.float64,
    tol_v: np.float64,
    max_iter: np.int64 = 20,
    koord_sistem_prostor: bool = True,
    vek_kolona: bool = False
) -> NDArray[np.float64]:
    """Odredjuje inverznu kinematiku gde su parametri proracuna u prostornom
    koordinatnom sistemu ili u koordinatnom sistemu zakacen za telo od
    interesa. Proracun je namenjen za robote sa otvorenim kinematskim lancem

    Parametri
    ---------
    M : Sequence | NDArray
        Pocetna konfiguracija (orijentacija i pozicija) hvataca robota kada
        su svi zglobovi u svojoj nultoj, odnosno pocetnoj, poziciji. Matrica je
        iz grupe SE(3)
    S_lista : Sequence | NDArray
        Spisak/lista ose zavrtnja svih zglobova robota kada je robot u svojoj
        pocetnoj konfiguraciji. Zavisno od parametra `vek_kolona`, individualne
        ose zavrtnjeva mogu biti u obliku vektora kolone (`vek_kolona` je True)
        ili u obliku vektora reda (`vek_kolona` je False). Dimenzije su nx6
        kada je `vek_kolona` False i 6xn kada je `vek_kolona` True, gde je n
        broj vektora ose zavrtnja S. Ose zavrtnja ne moraju biti normirane,
        tj. svejedno je da li je `S_lista` sastavljena od ose zavrtnja, vektora
        prostornih brzina ili neke kombinacije istih
    teta_lista0 : Sequence | NDArray | np.int32 | np.float64
        Spisak/lista uglova rotacije zglobova (u slucaju da neka osa
        predstavlja iskljucivo linearno kretanje, teta za taj zglob predstavlja
        duzinu linearnog kretanja) kao prvi nagadjaj u iterativnoj metodi.
        Dimenzije su 1xn ili nx1 gde je n broj vektora ose zavrtnja. U slucaju
        da je `S_lista` dimenzije 6x1 ili 1x6 onda `teta_lista0` ne mora biti
        niz tipa Sequence ili NDArray
    Tk : Sequence | NDArray
        SE(3) matrica konacne/zeljene konfiguracije robota
    tol_omega : np.float64
        Dozvoljena tolerancija za odstupanje po uglu od zeljene konfiguracije 
    tol_v : np.float64
        Dozvoljena tolerancija za odstupanje po poziciji od zeljene
        konfiguracije
    max_iter : np.int64, opcionalno
        Maksimalan broj iteracija funkcije `inv_kin`, posle cega se pojavljuje
        greska ukoliko funkcija ne konvergira. Automatska vrednost je 0.0
    koord_sistem_prostor : bool, opcionalno
        Odredjuje da li se ose zavrtnjeva iz `S_lista` smatra da su definise u
        prostornom koordinatnom sistemu ili u koordinatnom sistemu zakacen za
        telo od interesa (automatska vrednost je True) 
    vek_kolona : bool, opcionalno
        Odredjuje nacin prikazivanja ose zavrtnja unutar `S_lista` (automatska
        vrednost je False). Kada je `vek_kolona` False onda elementi spiska ose
        zavrtnja (ose zavrtnja za individualne zglobove) se smatraju da su
        poredjani po redovima, inace se smatra da su poredjani po kolonama 

    Povratna vrednost
    -----------------
    NDArray
        Lista generalisanih koordinata zglobova cija direktna kinematika
        priblizno odgovara (unutar tolerancija `tol_omega` i `tol_v`) zeljenoj
        konfiguraciji `Tk`

    Greske
    ------
    ValueError
        Nepravilne dimenzije ulaznih parametara
    InvKinError
        Algoritam nije konvergiraro u roku od broja iteracija jednako
        `max_iter`
    
    Primeri
    -------
    >>> M = [[-1, 0,  0, 0],
             [ 0, 1,  0, 6],
             [ 0, 0, -1, 2],
             [ 0, 0,  0, 1]]
    >>> S_lista_prostor = [[0, 0,    0],
                           [0, 0,    0],
                           [1, 0,   -1],
                           [4, 0,   -6],
                           [0, 3,    0],
                           [0, 0, -0.1]]
    >>> Tk = [[0, 1,  0,     -5],
              [1, 0,  0,      4],
              [0, 0, -1, 1.6858],
              [0, 0,  0,      1]]
    >>> teta_lista0 = [1.5, 2.5, 3]
    >>> tol_omega = 0.01
    >>> tol_v = 0.001
    >>> inv_kin(
        M,
        S_lista_prostor,
        teta_lista0,
        Tk,
        tol_omega,
        tol_v,
        vek_kolona=True
    )
    np.array([1.571, 3.0, 3.142])
    >>> S_lista_telo = [[0, 0, -1, 2, 0,   0],
                        [0, 0,  0, 0, 1,   0],
                        [0, 0,  1, 0, 0, 0.1]]
    >>> inv_kin(
        M,
        S_lista_telo,
        teta_lista0,
        Tk,
        tol_omega,
        tol_v,
        koord_sistem_prostor=False
    )
    np.array([1.571, 3.0, 3.142])
    """
    _alati._tol_provera(tol_omega, "tol_omega")
    _alati._tol_provera(tol_v, "tol_v")

    Tk = np.array(Tk, dtype=float)
    M = np.array(M, dtype=float)
    _alati._mat_provera(Tk, (4, 4), "Tk")
    _alati._mat_provera(M, (4, 4), 'M')
    
    if max_iter < 1:
        raise ValueError(
            "Broj iteracija algoritma \"max_iter\" ne sme biti <0"
    )

    # Lista uglova mora biti u obliku 1D niza
    teta_lista = np.atleast_1d(np.array(teta_lista0, dtype=float))
    
    S_lista = np.array(S_lista, dtype=float)
    
    # Algoritam je napravljen da funkcionise sa matricom `S_lista`
    if S_lista.ndim == 1:
        S_lista = S_lista[np.newaxis, :]

    # Za proracun sa smatra da je `S_lista` matrica gde su ose zavrtnja vektori
    # kolone. Zato, ako je uneta `S_lista` gde su ose zavrtnja vektori reda,
    # transponovati `S_lista`
    if not vek_kolona:
        S_lista = S_lista.T
        
    # Proveri da li vektori iz `S_lista` imaju 6 komponenti i da li
    # `teta_lista` ima elemenata koliko `S_lista` ima vektora
    _alati._mat_provera(S_lista, (6, S_lista.shape[1]), "S_lista")
    _alati._vek_provera(teta_lista, S_lista.shape[1], "teta_lista0")
        
    # Normirati vektore ose zavrtnja
    S_lista = np.apply_along_axis(mp.v_prostor_norm, 0, S_lista)
    
    # Algoritam je namenjen za izracunavanje u koordinatnom sistemu hvataca
    if koord_sistem_prostor:
        S_lista = np.apply_along_axis(
            lambda S: mp.Ad(mp.inv(M)) @ S,
            0,
            S_lista
        )
    
    Vb = mp.vek_od_lijeve_algebre(mp.log(mp.inv(
        dir_kin(M, S_lista, teta_lista, False, True)
    ) @ Tk))

    greska = np.linalg.norm(Vb[:3]) > tol_omega \
        or np.linalg.norm(Vb[3:]) > tol_v
    
    i = 0
    while greska and i < max_iter:
        teta_lista = teta_lista \
            + np.linalg.pinv(
                jakobijan(S_lista, teta_lista[1:], False, True)
            )@Vb

        i = i + 1
        Vb = mp.vek_od_lijeve_algebre(mp.log(mp.inv(
            dir_kin(M, S_lista, teta_lista, False, True)
        ) @ Tk))

        greska = np.linalg.norm(Vb[:3]) > tol_omega \
            or np.linalg.norm(Vb[3:]) > tol_v

    if i == max_iter:
        raise InvKinError(
            f"Proracun inverzne kinematike nije konvergirao nakon maksimalnog "
            f"broja iteracija \"max_iter\" = {max_iter}"
        )

    return teta_lista

def paden_kahan1(
    osa_zavrtnja: Sequence | NDArray,
    vek_pocetak: Sequence | NDArray,
    vek_kraj: Sequence | NDArray
) -> np.float64:
    """Resava 1. Paden-Kahanov podproblem rotacije tacke `vek_pocetak` oko
    ose zavrtnja (koja je cista rotacija, `korak == 0`) za odredjeni ugao do
    tacke `vek_kraj`

    Parametri
    ----------
    osa_zavrtnja : Sequence | NDArray
        Osa zavrtnja oko koje treba rotirati tacku `vek_pocetak` do tacke
        `vek_kraj`. Vektor ne mora biti normalizovan i korak ose zavrtnja mora
        biti 0
    vek_pocetak : Sequence | NDArray
        Pocetna tacka rotacije cije su dimenzije 1x3 ili 3x1
    vek_kraj : Sequence | NDArray
        Krajnja tacka rotacije cije su dimenzije 1x3 ili 3x1

    Povratna vrednost
    -----------------
    np.float64
        Ovaj Paden-Kahanov podproblem moze imati jedno resenje i nijedno
        resenje (tada se prijavljuje greska PadenKahanError). Takodje, na
        osnovu dobijenih resenja moze se odrediti citav skup resenja koje su u
        korelaciji sa povratnom vrednoscu ove funkcije (videti odeljak
        Beleske).
                
    Beleske
    -------
        Za resenje `teta` vazi da je validno resenje takodje
        `teta+-*2*k*np.pi` gde je `k` ceo broj. Npr ako imamo resenje
        `np.pi/4` onda vazi da je `-7*np.pi/4`, tj. `np.pi/4+-*2*k*np.pi`
        takodje resenje podproblema

    Greske
    ------
    ValueError
        Dimenzije unetih vektora su nepravilne. Osa zavrtnja nije cista
        rotacija, tj. njen korak nije jednak nuli
    PadenKahanError
        Paden-Kahanov podproblem nema resenja za zadate parametre

    Primeri
    -------
    >>> paden_kahan1(
        [0, -1, 0, 0, 0, 0],
        [0, 3, 1],
        [-1, 3, 0]
    )
    np.float64(1.571)
    >>> paden_kahan1(
        [[0],
         [0],
         [3],
         [3],
         [-9],
         [0]],
        [4, 1, 0],
        [[2],
         [1],
         [0]]
    )
    np.float64(3.142)
    """
    osa_zavrtnja = np.array(osa_zavrtnja, dtype=float)
    vek_pocetak = np.array(vek_pocetak, dtype=float)
    vek_kraj = np.array(vek_kraj, dtype=float)

    _alati._vek_provera(osa_zavrtnja, 6, "osa_zavrtnja")
    _alati._vek_provera(vek_pocetak, 3, "vek_pocetak")
    _alati._vek_provera(vek_kraj, 3, "vek_kraj")

    # Potrebni su vektori red za proracun
    vek_pocetak = vek_pocetak.reshape(3)
    vek_kraj = vek_kraj.reshape(3)
    
    vek_ose, omegaS, korak_zavrtnja \
        = mp.param_ose_zavrtnja(osa_zavrtnja.reshape(6))
    
    if not np.isclose(korak_zavrtnja, 0.0):
        raise ValueError(
            "Osa zavrtnja nije cista rotacija. Korak zavrtnja mora biti 0"
        )
    
    u = vek_pocetak - vek_ose
    v = vek_kraj - vek_ose

    u_prim = u - _vek_proj3(u, omegaS)
    v_prim = v - _vek_proj3(v, omegaS)
    
    if not (
        np.allclose(np.dot(omegaS, u), np.dot(omegaS, v))
        and np.allclose(np.linalg.norm(u_prim), np.linalg.norm(v_prim))
    ):
        raise PadenKahanError(1)
    
    return np.arctan2(
        np.dot(omegaS, np.cross(u_prim, v_prim)),
        np.dot(u_prim, v_prim)
    )

def paden_kahan2(
    osa_zavrtnja1: Sequence | NDArray,
    osa_zavrtnja2: Sequence | NDArray,
    vek_pocetak: Sequence | NDArray,
    vek_kraj: Sequence | NDArray
) -> Tuple[np.float64, np.float64] \
    | Tuple[Tuple[np.float64, np.float64], Tuple[np.float64, np.float64]]:
    """Resava 2. Paden-Kahanov podproblem rotacije tacke `vek_pocetak` oko
    dve ose zavrtnja (koje su ciste rotacije, `korak == 0`) za odredjene uglove
    do tacke `vek_kraj`. Takodje, resava podproblem i u slucaju da se ose
    zavrtnja ne presecaju ali jesu paralelne

    Parametri
    ---------
    osa_zavrtnja1 : Sequence | NDArray
        Prva osa zavrtnja oko koje treba rotirati tacku `vek_pocetak`. Vektor
        ne mora biti normalizovan i korak ose zavrtnja mora biti 0
    osa_zavrtnja2 : Sequence | NDArray
        Druga osa zavrtnja oko koje treba rotirati tacku nakon prve rotacije
        oko prve ose zavrtnja. Vektor ne mora biti normalizovan i korak ose
        zavrtnja mora biti 0    
    vek_pocetak : Sequence | NDArray
        Pocetna tacka rotacije cije su dimenzije 1x3 ili 3x1
    vek_kraj : Sequence | NDArray
        Krajnja tacka rotacije cije su dimenzije 1x3 ili 3x1
    
    Povratna vrednost
    -----------------
    Tuple[np.float64, np.float64]
    | Tuple[Tuple[np.float64, np.float64], Tuple[np.float64, np.float64]]
        Ovaj Paden-Kahanov podproblem moze imati jedan par resenja, dva para
        resenja i nijedno resenje (tada se prijavljuje greska PadenKahanError).
        Takodje, na osnovu dobijenih resenja moze se odrediti citav skup
        resenja koje su u korelaciji sa povratnom vrednoscu ove funkcije
        (videti odeljak Beleske). U prvom slucaju je tip podataka povratne
        vrednosti `Tuple[np.float64, np.float64]`, a u drugom je tip podataka
        povratne vrednosti `Tuple[Tuple[np.float64, np.float64],
        Tuple[np.float64, np.float64]]`. Ukoliko se ose zavrtnja poklapaju
        `osa_zavrtnja1 == osa_zavrtnja_2 or osa_zavrtnja1 == -osa_zavrtnja_2`
        onda funkcija vraca 1 par resenja gde je ugao rotacije druge ose
        jednako nuli (videti drugi primer u odeljku Primeri). U sustini, u ovom
        slucaju, svaka kombinacija uglova rotacije koja zadovoljava
        `teta = teta1 +- teta2` je validno resenje. Npr. ako je resenje
        `(np.pi/4, 0)` onda su podjednako valdina
        resenja `(0, np.pi/4)`, `(np.pi/8, np.pi/8)`, `(np.pi/2, -np.pi/4)`,
        itd. Resenje takodje postoji ukoliko su ose zavrtnja paralelne i to cak
        i kada su odvojene. 

    Beleske
    -------
        Za svaki par resenja vazi da je validno resenje za `teta` takodje
        `teta+-*2*k*np.pi` gde je `k` ceo broj. Npr ako imamo 2 para resenja
        `((np.pi/4, 0), (np.pi, np.pi/3))` onda vazi da je
        `((-7*np.pi/4, 0), (-np.pi, 7*np.pi/3))`, tj. `((np.pi/4+-*2*k*np.pi,
        0+-*2*k*np.pi), (np.pi+-*2*k*np.pi, np.pi/3+-*2*k*np.pi))` takodje
        resenje podproblema. U slucaju da imamo jedan par resenja onda vazi da
        je `(teta1+-*2*k*np.pi, teta2+-*2*k*np.pi)` podjednako validno resenje
        podproblema. Vise informacija o dopunjenom 2. Paden-Kahanovom
        podproblemu za slucaj kada su ose zavrtnja paralelne se mogu naci u
        radu: Dimovski I., Trompeska M., Samak S., Dukovski V., Cvetkoska D.,
        "Algorithmic Approach to Geometric Solution of Generalized Paden-Kahan
        Subproblem and its Extension", International Journal of Advanced
        Robotic Systems 15(1), 2018.

    Greske
    ------
    ValueError
        Dimenzije unetih vektora su nepravilne. Ose zavrtnja nisu ciste
        rotacije, tj. koraci nisu jednaki nuli. Ose zavrtnja se ne presecaju,
        poklapaju i nisu paralelne
    PadenKahanError
        Paden-Kahanov podproblem nema resenja za zadate parametre
        
    Primeri
    -------
    >>> paden_kahan2(
        [1, 0, 0, 0, 0, 0],
        [0, np.sqrt(2)/2, np.sqrt(2)/2, 0, 0, 0],
        [[0],
        [0],
        [1]],
        [0, -np.sqrt(3)/2, 1/2]
    )
    (
        (np.float64(1.047), np.float64(0.0)),
        (np.float64(2.618), np.float64(3.142))
    )
    >>> paden_kahan2(
        [[0],
         [0],
         [1],
         [0],
         [0],
         [0]],
        [0, 0, 1, 0, 0, 0],
         [1, 0, 0],
         [0, 1, 0]
    )
    (np.float64(1.571), np.float64(0.0))
    >>> paden_kahan2(
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, -1, 1],
        [1, -1, 0]
    )
    (np.float64(1.571), np.float64(0.0))
    >>> paden_kahan2(
        [0, 0, 1, 3, 5, 0],
        [0, 0, 1, 3, 0, 0],
        [ 0, 3, 0],
        [-5, 8, 0]
    )
    (np.float64(1.571), np.float64(0.0))
    >>> paden_kahan2(
        [0, 0, 1, 3, 5, 0],
        [0, 0, 1, 3, 0, 0],
        [ 3, 3, 0],
        [-8, 3, 0]
    )
    (
        (np.float64(-2.556), np.float64(3.727)),
        (np.float64( 2.559), np.float64(2.559))
    )
    """
    osa_zavrtnja1 = np.array(osa_zavrtnja1, dtype=float)
    osa_zavrtnja2 = np.array(osa_zavrtnja2, dtype=float)
    vek_pocetak = np.array(vek_pocetak, dtype=float)
    vek_kraj = np.array(vek_kraj, dtype=float)

    _alati._vek_provera(osa_zavrtnja1, 6, "osa_zavrtnja1")
    _alati._vek_provera(osa_zavrtnja2, 6, "osa_zavrtnja2")
    _alati._vek_provera(vek_pocetak, 3, "vek_pocetak")
    _alati._vek_provera(vek_kraj, 3, "vek_kraj")
    
    # Potrebni su vektori red za proracun
    vek_pocetak = vek_pocetak.reshape(3)
    vek_kraj = vek_kraj.reshape(3)
    osa_zavrtnja1 = osa_zavrtnja1.reshape(6)
    osa_zavrtnja2 = osa_zavrtnja2.reshape(6)

    osa_zavrtnja1 = mp.v_prostor_norm(osa_zavrtnja1)
    osa_zavrtnja2 = mp.v_prostor_norm(osa_zavrtnja2)

    vek_ose1, omegaS1, korak_zavrtnja1 \
        = mp.param_ose_zavrtnja(osa_zavrtnja1)
    
    vek_ose2, omegaS2, korak_zavrtnja2 \
        = mp.param_ose_zavrtnja(osa_zavrtnja2)
    
    if not np.isclose(korak_zavrtnja1, 0.0):
        raise ValueError(
            "Osa zavrtnja 1 nije cista rotacija. Korak zavrtnja mora biti 0"
        )
    
    if not np.isclose(korak_zavrtnja2, 0.0):
        raise ValueError(
            "Osa zavrtnja 2 nije cista rotacija. Korak zavrtnja mora biti 0"
        )
        
    # Prema jednacini <a, b> = ||a||*||b||*cos(a, b) dobijamo da ukoliko je
    # a == b ili a == -b sledi da je, |<a, b>| = ||a||*||b||. Ako smatramo da
    # je a == osa_zavrtnja1 i b == osa_zavrtnja_2, Paden-Kahan 2 mozemo svesti
    # na Paden-Kahan 1 jer su ose zavrtnja kolinearne
    if np.isclose(
        np.abs(np.dot(osa_zavrtnja1, osa_zavrtnja2)),
        np.linalg.norm(osa_zavrtnja1)*np.linalg.norm(osa_zavrtnja2)
    ):
        ugao = paden_kahan1(osa_zavrtnja1, vek_pocetak, vek_kraj)
        return (ugao, np.float64(0.0))
    
    # U opstem slucaju vek_ose1 != vek_ose2. Iz uslova da je
    # vek_ose1 = r - ksi_1*omegaS1 i vek_ose2 = r - ksi_2*omegaS2
    # odredjujemo tacku presecanja ose r. Prvo iz jednacine
    # np.vstack([omegaS1, omegaS2]).T @ ksi = vek_ose1 - vek_ose2
    # odredjujemo vektor ksi = [ksi1, ksi2] i poredjenjem
    # vek_ose1 - ksi[0]*omegaS1 == vek_ose2 - ksi[1]*omegaS2 proveravamo da li
    # se ose uopste presecaju 
    ksi = np.linalg.lstsq(
        np.vstack([omegaS1, -omegaS2]).T,
        vek_ose1 - vek_ose2,
        rcond=None
    )[0]
    
    r = vek_ose1 - ksi[0]*omegaS1
    
    try:
        # Provera da li se ose zavrtnja presecaju
        if np.allclose(r, vek_ose2 - ksi[1]*omegaS2):
            u = vek_pocetak - r
            v = vek_kraj - r
            
            alfa = (
                np.dot(omegaS1, omegaS2)
                *np.dot(omegaS2, u)
                - np.dot(omegaS1, v)
            )/(np.dot(omegaS1, omegaS2)**2 - 1)

            beta = (
                np.dot(omegaS1, omegaS2)
                *np.dot(omegaS1, v)
                - np.dot(omegaS2, u)
            )/(np.dot(omegaS1, omegaS2)**2 - 1)

            # Ukoliko je pod korenom negativna vrednost, zanemaricemo poruku
            # upozorenja i objaviti gresku PadenKahanError(2)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)        
                gama = np.sqrt(
                    (
                        np.linalg.norm(u)**2
                        - alfa*(alfa + 2*beta*np.dot(omegaS1, omegaS2))
                        - beta**2
                    )
                )/np.linalg.norm(np.cross(omegaS1, omegaS2))

            if np.isnan(gama):
                raise PadenKahanError(2)

            # S obzirom da za male numericke vrednost od gamma**2, kvadratni
            # koren znacajno povecava gresku ukoliko nam je vrednost blizu 0,
            # povecavamo toleranciju za funkciju np.isclose()
            if np.isclose(gama, 0.0, 1e-3, 1e-4):
                # Podproblem ima 1 par resenja jer je gama == 0
                c = r + alfa*omegaS1 + beta*omegaS2
                return (
                    paden_kahan1(-osa_zavrtnja1, vek_kraj, c),
                    paden_kahan1(osa_zavrtnja2, vek_pocetak, c)
                )
            else:
                # Podproblem ima 2 para resenja za uglove teta1 i teta2 u
                # zavisnosti od
                # (c1, c2) = r
                #          + alfa*omegaS1
                #          + beta*omegaS2
                #          +- gama*||omegaS1 x omegaS2||
                # gde za c1 imamo jedan par resenja i za c2 imamo drugi par
                # resenja
                c = r + alfa*omegaS1 + beta*omegaS2
                return (
                    (
                        paden_kahan1(
                            -osa_zavrtnja1,
                            vek_kraj,
                            c + gama*np.cross(omegaS1, omegaS2)
                        ),
                        paden_kahan1(
                            osa_zavrtnja2,
                            vek_pocetak,
                            c + gama*np.cross(omegaS1, omegaS2)
                        )
                    ),
                    (
                        paden_kahan1(
                            -osa_zavrtnja1,
                            vek_kraj,
                            c - gama*np.cross(omegaS1, omegaS2)
                        ),
                        paden_kahan1(
                            osa_zavrtnja2,
                            vek_pocetak,
                            c - gama*np.cross(omegaS1, omegaS2)
                        )
                    )
                )
        
        # Koristeci istu logiku kao u prethodnim linijama koda u istoj funkciji
        # za odredjivanje da li je osa_zavrtnja1 == osa_zavrtnja2 ili
        # osa_zavrtnja1 == -osa_zavrtnja2, odredicemo da li su ose zavrtnja
        # paralelne
        elif np.isclose(
            np.abs(np.dot(omegaS1, omegaS2)),
            np.linalg.norm(omegaS1)*np.linalg.norm(omegaS2)
        ):
            # Tacka oko koje se rotira vektor vek_pocetak nakon rotacije oko
            # prve ose zavrtnja. Korespondira rotaciji oko ose_zavrtnja1
            centar_rotacije1 = vek_ose1 \
            + _vek_proj3(vek_kraj - vek_ose1, omegaS1)
            
            # Prvi glavni uslov postojanja resenja podproblema
            if not np.isclose(
                np.dot(omegaS1, vek_pocetak - centar_rotacije1),
                0.0
            ):
                raise PadenKahanError(2)
            
            delta = np.linalg.norm(vek_kraj - centar_rotacije1)
            
            u = vek_pocetak - vek_ose2
            
            u_prim = (
                vek_pocetak
                - vek_ose2
                - _vek_proj3(vek_pocetak - vek_ose2, omegaS1)
            )
            
            v_prim = (
                centar_rotacije1
                - vek_ose2
                - _vek_proj3(centar_rotacije1 - vek_ose2, omegaS1)
            )
            
            # Drugi glavni uslov postojanja resenja podproblema
            if np.abs(
                np.linalg.norm(u_prim)**2
                + np.linalg.norm(v_prim)**2
                - delta**2
            ) > 2*np.linalg.norm(u_prim)*np.linalg.norm(v_prim):
                raise PadenKahanError(2)

            if np.allclose(u_prim, np.zeros_like(u_prim)):
                if not np.isclose(
                    delta,
                    np.linalg.norm(vek_pocetak - centar_rotacije1)
                ):
                    raise PadenKahanError(2)
                
                # U ovom slucaju postoje beskonacno mnogo resenja za drugi
                # ugao, tj. resenje za drugi ugao je bilo koji broj iz skupa
                # realnih brojeva
                else:
                    return (
                        paden_kahan1(osa_zavrtnja1, vek_pocetak, vek_kraj),
                        np.float64(0.0)
                    )
            
            # U ovom slucaju postoje beskonacno mnogo resenja za prvi ugao, tj.
            # resenje za prvi ugao je bilo koji broj iz skupa realnih brojeva
            if np.isclose(delta, 0.0):
                return (
                    np.float64(0.0),
                    paden_kahan3(
                        osa_zavrtnja2,
                        vek_pocetak,
                        centar_rotacije1,
                        0.0
                    )
                )
                
            ugao2 = paden_kahan3(
                osa_zavrtnja2,
                vek_pocetak,
                centar_rotacije1,
                delta
            )

            if isinstance(ugao2, tuple):
                return (
                    (
                        paden_kahan1(
                            osa_zavrtnja1,
                            mp.SE3_proizvod_3D(
                                mp.exp_vek_ugao(osa_zavrtnja2, ugao2[0]),
                                vek_pocetak
                            ),
                            vek_kraj
                        ),
                        ugao2[0]
                    ),
                    (
                        paden_kahan1(
                            osa_zavrtnja1,
                            mp.SE3_proizvod_3D(
                                mp.exp_vek_ugao(osa_zavrtnja2, ugao2[1]),
                                vek_pocetak
                            ),
                            vek_kraj
                        ),
                        ugao2[1]
                    )
                )
            else:
                return (
                    paden_kahan1(
                        osa_zavrtnja1,
                        mp.SE3_proizvod_3D(
                            mp.exp_vek_ugao(osa_zavrtnja2, ugao2),
                            vek_pocetak
                        ),
                        vek_kraj
                    ),
                    ugao2
                )
        else:
            raise ValueError(
                "Ose zavrtnja 1 i 2 se ne presecaju i nisu paralelne"
            )
    
    except PadenKahanError:
        # paden_kahan1() moze prijaviti gresku PadenKahanError(1), a zelimo da
        # korisnik vidi PadenKahanError(2)
        raise PadenKahanError(2) from None

def paden_kahan3(
    osa_zavrtnja: Sequence | NDArray,
    vek_pocetak: Sequence | NDArray,
    vek_kraj: Sequence | NDArray,
    delta: np.float64
) -> np.float64 | Tuple[np.float64, np.float64]:
    """Resava 3. Paden-Kahanov podproblem rotacije tacke `vek_pocetak` oko
    ose zavrtnja (koja je cista rotacija, `korak == 0`) za odredjeni ugao
    tako da je udaljena za `delta` od tacke `vek_kraj`
    
    Parametri
    ---------
    osa_zavrtnja : Sequence | NDArray
        Osa zavrtnja oko koje treba rotirati tacku `vek_pocetak` do tacke koja
        je udaljena od `vek_kraj` za `delta`. Vektor ne mora biti normalizovan
        i korak ose zavrtnja mora biti 0
    vek_pocetak : Sequence | NDArray
        Pocetna tacka rotacije cije su dimenzije 1x3 ili 3x1
    vek_kraj : Sequence | NDArray
        Druga tacka rotacije cije su dimenzije 1x3 ili 3x1
    delta : float | np.float64
        Distanca izmedju rotirate tacke `vek_pocetak` oko ose `osa_zavrtnja` i
        tacke `vek_kraj`
    
    Povratna vrednost
    -----------------
    np.float64 | Tuple[np.float64, np.float64]
        Ovaj Paden-Kahanov podproblem moze imati dva resenja za ugao `teta`,
        jedno resenje i nijedno resenje (tada se prijavljuje greska
        PadenKahanError). Takodje, na osnovu dobijenih resenja moze se odrediti
        citav skup resenja koje su u korelaciji sa povratnom vrednoscu ove
        funkcije (videti odeljak Beleske). U slucaju da imamo dva resenja, oba
        resenja imaju svoj skup resenja kome pripadaju. Kada imamo jedno
        resenje onda je tip podataka povratne vrednost `np.float64`, a kada
        imamo dva onda je tip podataka povratne vrednosti
        `Tuple[np.float64, np.float64]`

    Beleske
    -------
        Za resenje `teta` vazi da je validno resenje takodje
        `teta+-*2*k*np.pi` gde je `k` ceo broj. Npr ako imamo resenje
        `np.pi/4` onda vazi da je `-7*np.pi/4` tj. `np.pi/4+-*2*k*np.pi`. U
        slucaju da imamo jedan par resenja onda vazi za nase resenje koje npr.
        glasi `(np.pi, np.pi/3)` onda vazi da je `(-np.pi, 7*np.pi/3))`, tj.
        `(teta1+-*2*k*np.pi, teta2+-*2*k*np.pi)` takodje resenje podproblema
    
    Greske
    ------
    ValueError
        Dimenzije unetih vektora su nepravilne. Osa zavrtnja nije cista
        rotacija, tj. njen korak nije jednak nuli. Parametar `delta` nije >= 0
    PadenKahanError
        Paden-Kahanov podproblem nema resenja za zadate parametre
    
    Primeri
    -------
    >>> paden_kahan3(
        [0, 0, 5, 0, 0, 0],
        [[ 1],
         [-2],
         [0]],
        [3, 3, 3],
        np.sqrt(14)        
    )
    (np.float64(2.214), np.float64(1.571))
    >>> paden_kahan3(
        [[4],
         [0],
         [0],
         [0],
         [0],
         [0]],
        [0, -1, 0],
        [[0],
         [2],
         [2]],
        (np.sqrt(9 - 4*np.sqrt(2)))        
    )
    np.float64(-2.356)
    >>> paden_kahan3(
        [0, 1, 0, 0, 0, 1],
        [0, 1, 0],
        [1, 1, 1],
        0
    )
    np.float64(1.571)
    """
    if np.isclose(delta, 0.0):
        try:
            return paden_kahan1(osa_zavrtnja, vek_pocetak, vek_kraj)
        except PadenKahanError:
            # paden_kahan1() moze prijaviti gresku PadenKahanError(1), a zelimo
            # da korisnik vidi PadenKahanError(3)
            raise PadenKahanError(3) from None
    elif delta < 0.0:
        raise ValueError("Parametar duzine \"delta\" mora biti >= 0")
    
    osa_zavrtnja = np.array(osa_zavrtnja, dtype=float)
    vek_pocetak = np.array(vek_pocetak, dtype=float)
    vek_kraj = np.array(vek_kraj, dtype=float)
    delta = np.float64(delta)
    
    _alati._vek_provera(osa_zavrtnja, 6, "osa_zavrtnja")
    _alati._vek_provera(vek_pocetak, 3, "vek_pocetak")
    _alati._vek_provera(vek_kraj, 3, "vek_kraj")
    
    osa_zavrtnja = mp.v_prostor_norm(osa_zavrtnja)
    
    # Potrebni su vektori red za proracun
    vek_pocetak = vek_pocetak.reshape(3)
    vek_kraj = vek_kraj.reshape(3)
    
    vek_ose, omegaS, korak_zavrtnja \
        = mp.param_ose_zavrtnja(osa_zavrtnja.reshape(6))

    if not np.isclose(korak_zavrtnja, 0.0):
        raise ValueError(
            "Osa zavrtnja nije cista rotacija. Korak zavrtnja mora biti 0"
        )

    u_prim = vek_pocetak - vek_ose - _vek_proj3(vek_pocetak - vek_ose, omegaS)
    v_prim = vek_kraj - vek_ose - _vek_proj3(vek_kraj - vek_ose, omegaS)

    # Zbog greske pri numerickom proracunu, mozemo dobiti da je cos(fi) malo
    # veci od 1 ili malo manji od -1 i ako to uvrstimo u fi = arccos(cos(fi))
    # dobijamo np.nan, zato mora na malo drugaciji nacin da se pristupi
    # proracunu ugla fi
    cos_fi = (
            np.linalg.norm(u_prim)**2
            + np.linalg.norm(v_prim)**2
            - delta**2
            + np.abs(np.dot(omegaS, vek_pocetak - vek_kraj))**2
    )/(2*np.linalg.norm(u_prim)*np.linalg.norm(v_prim))
    
    if np.isclose(cos_fi, 1.0) and cos_fi > 1.0:
        fi = 0.0
    elif np.isclose(cos_fi, -1.0) and cos_fi < -1.0:
        fi = np.pi
    else:
        # Ukoliko je pod np.arccos() vrednost van domena funkcije, zanemaricemo
        # poruku upozorenja i objaviti gresku PadenKahanError(3)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            fi = np.arccos(cos_fi)

    if np.isnan(fi):
        raise PadenKahanError(3)

    if np.isclose(fi, 0.0):
        teta = np.arctan2(
                np.dot(omegaS, np.cross(u_prim, v_prim)),
                np.dot(u_prim, v_prim)
            )
    # Kada je fi == np.pi, tada je razlika izmedju 2 dobijena resenja 2*np.pi,
    # tako da nema potrebe da se vracaju nazad oba resenja vec samo jedno jer
    # je drugo u skupu resenja prvog (videti Povratna vrednost i Beleske u
    # docstring ove funkcije)
    elif np.isclose(fi, np.pi):
        teta = np.arctan2(
                np.dot(omegaS, np.cross(u_prim, v_prim)),
                np.dot(u_prim, v_prim)
            ) - np.pi
        
        # Posto je teta == 2*np.pi pun okret, validno resenje je takodje
        # teta == 0.0
        if np.isclose(teta, 2*np.pi):
            teta = np.float64(0.0)
    else:
        teta = (
            np.arctan2(
                np.dot(omegaS, np.cross(u_prim, v_prim)),
                np.dot(u_prim, v_prim)
            ) + fi,
            np.arctan2(
                np.dot(omegaS, np.cross(u_prim, v_prim)),
                np.dot(u_prim, v_prim)
            ) - fi
        )
    
    if isinstance(teta, tuple):
        if not np.isclose(np.linalg.norm(
            vek_kraj
            - (
                mp.exp_vek_ugao(osa_zavrtnja, teta[0])
                @ mp.homogeni_vek(vek_pocetak)
            )[:3]
        ), delta):
            raise PadenKahanError(3)
    else:
        if not np.isclose(np.linalg.norm(
            vek_kraj
            - (
                mp.exp_vek_ugao(osa_zavrtnja, teta)
                @ mp.homogeni_vek(vek_pocetak)
            )[:3]
        ), delta):
            raise PadenKahanError(3)

    return teta

def pardos_gotor1(
    osa_zavrtnja: Sequence | NDArray,
    vek_pocetak: Sequence | NDArray,
    vek_kraj: Sequence | NDArray
) -> np.float64:
    """Resava 1. Pardos-Gotorov podproblem rotacije tacke `vek_pocetak` duz
    ose zavrtnja (koja je cista translacija,
    `np.linalg.norm(osa_zavrtnja[:3]) == 0.0`) za vrednost do tacke `vek_kraj`

    Parametri
    ----------
    osa_zavrtnja : Sequence | NDArray
        Osa zavrtnja duz koje treba translirati tacku `vek_pocetak` do tacke
        `vek_kraj`. Vektor ne mora biti normalizovan i vektor ose rotacije od
        ose zavrtnja mora biti nulti vektor
    vek_pocetak : Sequence | NDArray
        Pocetna tacka translacije cije su dimenzije 1x3 ili 3x1
    vek_kraj : Sequence | NDArray
        Krajnja tacka translacije cije su dimenzije 1x3 ili 3x1

    Povratna vrednost
    -----------------
    np.float64
        Ovaj Pardos-Gotorov podproblem moze imati jedno resenje i nijedno
        resenje (tada se prijavljuje greska PardosGotorError)

    Beleske
    -------
    Vise detalja o Pardos-Gotorovim podproblemima su dostupni na: Pardos-Gotor
    J., "Screw Theory in Robotics: an Illustrated and Practicable Introduction
    to Modern Mechanics", CRC Press, USA, 2022.
    
    Greske
    ------
    ValueError
        Dimenzije unetih vektora su nepravilne. Osa zavrtnja nije cista
        translacija, tj. njena osa rotacije nije jednaka nultom vektoru
    PardosGotorError
        Pardos-Gotorov podproblem nema resenja za zadate parametre

    Primeri
    -------
    >>> pardos_gotor1(
        [0, 0, 0, 1, 0, 0],
        [1, 1, 0],
        [4, 1, 0]
    )
    np.float64(3.000)
    >>> pardos_gotor1(
        [[0],
         [0],
         [0],
         [4],
         [0],
         [0]],
        [1, 1, 0],
        [[1],
         [1],
         [0]]
    )
    np.float64(0.000)
    """
    osa_zavrtnja = np.array(osa_zavrtnja, dtype=float)
    vek_pocetak = np.array(vek_pocetak, dtype=float)
    vek_kraj = np.array(vek_kraj, dtype=float)

    _alati._vek_provera(osa_zavrtnja, 6, "osa_zavrtnja")
    _alati._vek_provera(vek_pocetak, 3, "vek_pocetak")
    _alati._vek_provera(vek_kraj, 3, "vek_kraj")

    # Potrebni su vektori red za proracun
    vek_pocetak = vek_pocetak.reshape(3)
    vek_kraj = vek_kraj.reshape(3)
    osa_zavrtnja = mp.v_prostor_norm(osa_zavrtnja).reshape(6)
    
    if not np.isclose(np.linalg.norm(osa_zavrtnja[:3]), 0.0):
        raise ValueError(
            "Osa zavrtnja nije translacija rotacija. Osa rotacije ose "
            "zavrtnja mora biti nulti vektor"
        )
    
    resenje = np.dot(osa_zavrtnja[3:], vek_kraj - vek_pocetak)
    
    # S obzirom na izvor odakle je uzeto resenje, nisu navedeni uslovi
    # postojanja podproblema, prema temo cemo proveriti resenja na osnovu
    # glavne jednacine:
    # mp.SE3_proizvod_3D(mp.exp_vek_ugao(osa_zavrtnja, resenje), vek_pocetak)
    # == vek_kraj
    # Sto se drugacije moze napisati kao
    # resenje*osa_zavrtnja.reshape[3:] + vek_pocetak == vek_kraj
    # zato sto je osa zavrtnja cista translacija
    if np.allclose(
        resenje*osa_zavrtnja[3:] + vek_pocetak,
        vek_kraj
    ):
        return resenje
    else:
        raise PardosGotorError(1)

def pardos_gotor2(
    osa_zavrtnja1: Sequence | NDArray,
    osa_zavrtnja2: Sequence | NDArray,
    vek_pocetak: Sequence | NDArray,
    vek_kraj: Sequence | NDArray
) -> Tuple[np.float64, np.float64]:
    """Resava 2. Pardos-Gotorov podproblem translacije tacke `vek_pocetak` duz
    dve ose zavrtnja (koje su ciste translacije,
    `np.linalg.norm(osa_zavrtnja[:3]) == 0.0`) za odredjene vrednosti do tacke
    `vek_kraj`. Takodje, resava podproblem i u slucaju da se ose zavrtnja ne
    presecaju ali jesu paralelne

    Parametri
    ---------
    osa_zavrtnja1 : Sequence | NDArray
        Prva osa zavrtnja duz koje treba translirati tacku `vek_pocetak`.
        Vektor ne mora biti normalizovan i osa rotacije ose zavrtnja mora biti
        nulti vektor
    osa_zavrtnja2 : Sequence | NDArray
        Druga osa zavrtnja duz koje treba translirati tacku `vek_pocetak` nakon
        prve translacije duz prve ose zavrtnja. Vektor ne mora biti
        normalizovan i osa rotacije ose zavrtnja mora biti nulti vektor
    vek_pocetak : Sequence | NDArray
        Pocetna tacka translacije cije su dimenzije 1x3 ili 3x1
    vek_kraj : Sequence | NDArray
        Krajnja tacka translacije cije su dimenzije 1x3 ili 3x1
    
    Povratna vrednost
    -----------------
    Tuple[np.float64, np.float64]
        Ovaj Pardos-Gotorov podproblem moze imati jedan par resenja i nijedno
        resenje (tada se prijavljuje greska PardosGotorError). Ukoliko se ose
        zavrtnja poklapaju `osa_zavrtnja1 == osa_zavrtnja_2 or
        osa_zavrtnja1 == -osa_zavrtnja_2` onda funkcija vraca par resenja gde
        je vrednost translacije duz druge ose jednako nuli (videti drugi
        primer u odeljku Primeri) ali svaka vrednost iz skupa realnih brojeva 
        predstavlja resenje za drugu vrednost translacije. Npr. ako je resenje
        `(3.0, 0)` onda su podjednako valdina resenja `(3.0, -12)`, `(3.0, 3)`,
        `(3.0, 3.0)`, itd. 

    Beleske
    -------
    Vise detalja o Pardos-Gotorovim podproblemima su dostupni na: Pardos-Gotor
    J., "Screw Theory in Robotics: an Illustrated and Practicable Introduction
    to Modern Mechanics", CRC Press, USA, 2022.

    Greske
    ------
    ValueError
        Dimenzije unetih vektora su nepravilne. Ose zavrtnja nisu ciste
        translacije, tj. ose rotacije ose zavrtnja nisu nulti vektori. Ose
        zavrtnja se ne presecaju, poklapaju i nisu paralelne
    PardosGotorError
        Pardos-Gotorov podproblem nema resenja za zadate parametre
        
    Primeri
    -------
    >>> pardos_gotor2(
        [0, 0, 0, 1, 0, 0],
        [[0],
         [0],
         [0],
         [np.sqrt(2)/2],
         [np.sqrt(2)/2],
         [0]],
        [0, 1, 0],
        [[2],
         [2],
         [0]]
    )
    (np.float64(1.0), np.float64(1.414))
    >>> pardos_gotor2(
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [1, 0, 0],
            [4, 0, 0]
    )
    (np.float64(3.0), np.float64(0.0))
    >>> pardos_gotor2(
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [2, 0, 0],
        [1, 0, 0]
    )
    (np.float64(0.0), np.float64(-1.0))
    """
    osa_zavrtnja1 = np.array(osa_zavrtnja1, dtype=float)
    osa_zavrtnja2 = np.array(osa_zavrtnja2, dtype=float)
    vek_pocetak = np.array(vek_pocetak, dtype=float)
    vek_kraj = np.array(vek_kraj, dtype=float)

    _alati._vek_provera(osa_zavrtnja1, 6, "osa_zavrtnja1")
    _alati._vek_provera(osa_zavrtnja2, 6, "osa_zavrtnja2")
    _alati._vek_provera(vek_pocetak, 3, "vek_pocetak")
    _alati._vek_provera(vek_kraj, 3, "vek_kraj")
    
    # Potrebni su vektori red za proracun
    vek_pocetak = vek_pocetak.reshape(3)
    vek_kraj = vek_kraj.reshape(3)
    osa_zavrtnja1 = osa_zavrtnja1.reshape(6)
    osa_zavrtnja2 = osa_zavrtnja2.reshape(6)

    osa_zavrtnja1 = mp.v_prostor_norm(osa_zavrtnja1)
    osa_zavrtnja2 = mp.v_prostor_norm(osa_zavrtnja2)
    
    if not np.isclose(np.linalg.norm(osa_zavrtnja1[:3]), 0.0):
        raise ValueError(
            "Osa zavrtnja nije translacija rotacija. Osa rotacije ose "
            "zavrtnja mora biti nulti vektor"
        )
    
    if not np.isclose(np.linalg.norm(osa_zavrtnja2[:3]), 0.0):
        raise ValueError(
            "Osa zavrtnja nije translacija rotacija. Osa rotacije ose "
            "zavrtnja mora biti nulti vektor"
        )
        
    # Prema jednacini <a, b> = ||a||*||b||*cos(a, b) dobijamo da ukoliko je
    # a == b ili a == -b sledi da je, |<a, b>| = ||a||*||b||. Ako smatramo da
    # je a == osa_zavrtnja1 i b == osa_zavrtnja_2, Pardos-Gotor 2 mozemo svesti
    # na Pardos-Gotor 1 jer su ose zavrtnja kolinearne
    if np.isclose(
        np.abs(np.dot(osa_zavrtnja1, osa_zavrtnja2)),
        np.linalg.norm(osa_zavrtnja1)*np.linalg.norm(osa_zavrtnja2)
    ):
        ugao = pardos_gotor1(osa_zavrtnja1, vek_pocetak, vek_kraj)
        return (ugao, np.float64(0.0))
    
    c = vek_kraj \
        + (
            np.linalg.norm(np.cross(osa_zavrtnja2[3:], vek_pocetak - vek_kraj))
            /np.linalg.norm(np.cross(osa_zavrtnja2[3:], osa_zavrtnja1[3:]))
        ) \
        *osa_zavrtnja1[3:] \
        *np.sign(np.dot(
            np.cross(osa_zavrtnja2[3:], vek_pocetak - vek_kraj),
            np.cross(osa_zavrtnja2[3:], osa_zavrtnja1[3:])
        ))

    try:
        resenje1 = pardos_gotor1(osa_zavrtnja1, c, vek_kraj)
        resenje2 = pardos_gotor1(osa_zavrtnja2, vek_pocetak, c)
    except PardosGotorError:
        # pardos_gotor1() moze prijaviti gresku PardosGotorError(1), a zelimo
        # da korisnik vidi PardosGotorError(2)
        raise PardosGotorError(2) from None
    
    # S obzirom na izvor odakle je uzeto resenje, nisu navedeni uslovi
    # postojanja podproblema, prema temo cemo proveriti resenja na osnovu
    # glavne jednacine:
    # mp.SE3_proizvod_3D(
    #   mp.exp_vek_ugao(osa_zavrtnja1, resenje)
    #       *mp.exp_vek_ugao(osa_zavrtnja2, resenje),
    #   vek_pocetak
    # )
    # == vek_kraj
    # Sto se drugacije moze napisati kao
    # resenje1*osa_zavrtnja1.reshape[3:] \
    #   + resenje2*osa_zavrtnja2.reshape[3:] \
    #   + vek_pocetak \
    # == vek_kraj
    # zato sto su ose zavrtnja ciste translacije
    if np.allclose(
        resenje1*osa_zavrtnja1[3:] + resenje2*osa_zavrtnja2[3:] + vek_pocetak,
        vek_kraj
    ):
        return (resenje1, resenje2)
    else:
        raise PardosGotorError(2)

def pardos_gotor3(
    osa_zavrtnja: Sequence | NDArray,
    vek_pocetak: Sequence | NDArray,
    vek_kraj: Sequence | NDArray,
    delta: np.float64
) -> np.float64 | Tuple[np.float64, np.float64]:
    """Resava 3. Pardos-Gotorov podproblem translacije tacke `vek_pocetak` duz
    ose zavrtnja (koja je cista rotacija,
    `np.linalg.norm(osa_zavrtnja[:3]) == 0.0`) za odredjenu vrednost tako da je
    udaljena za `delta` od tacke `vek_kraj`
    
    Parametri
    ---------
    osa_zavrtnja : Sequence | NDArray
        Osa zavrtnja duz koje treba translirati tacku `vek_pocetak` do tacke
        `vek_kraj`. Vektor ne mora biti normalizovan i osa rotacije ose
        zavrtnja mora biti nulti vektor
    vek_pocetak : Sequence | NDArray
        Pocetna tacka translacije cije su dimenzije 1x3 ili 3x1
    vek_kraj : Sequence | NDArray
        Druga tacka cije su dimenzije 1x3 ili 3x1
    delta : float | np.float64
        Distanca izmedju translirane tacke `vek_pocetak` duz ose `osa_zavrtnja`
        i tacke `vek_kraj`
    
    Povratna vrednost
    -----------------
    np.float64 | Tuple[np.float64, np.float64]
        Ovaj Pardos-Gotorov podproblem moze imati dva resenja, jedno resenje i
        i nijedno resenje (tada se prijavljuje greska PardosGotorError). Kada
        imamo jedno resenje onda je tip podataka povratne vrednost
        `np.float64`, a kada imamo dva onda je tip podataka povratne vrednosti
        `Tuple[np.float64, np.float64]`

    Beleske
    -------
    Vise detalja o Pardos-Gotorovim podproblemima su dostupni na: Pardos-Gotor
    J., "Screw Theory in Robotics: an Illustrated and Practicable Introduction
    to Modern Mechanics", CRC Press, USA, 2022.
    
    Greske
    ------
    ValueError
        Dimenzije unetih vektora su nepravilne. Osa zavrtnja nije cista
        translacija, tj. njena osa rotacije nije jednaka nultom vektoru
    PardosGotorError
        Pardos-Gotorov podproblem nema resenja za zadate parametre
    
    Primeri
    -------
    >>> pardos_gotor3(
        [0, 0, 0, 5, 0, 0],
        [1, 0, 0],
        [[3],
         [2],
         [0]],
        3
    )
    (np.float64(4.236), np.float64(-0.236))
    >>> pardos_gotor3(
        [0, 0, 0, 1, 0, 0],
        [1, 0, 0],
        [3, 3, 0],
        3
    )
    np.float64(2.0)
    >>> pardos_gotor3(
        [0, 0, 0, 0, 1, 0],
        [0, 1, 0],
        [0, 3, 0],
        0
    )
    np.float64(2.0)
    """
    if not np.isclose(delta, 0.0) and delta < 0.0:
        raise ValueError("Parametar duzine \"delta\" mora biti >= 0")

    osa_zavrtnja = np.array(osa_zavrtnja, dtype=float)
    vek_pocetak = np.array(vek_pocetak, dtype=float)
    vek_kraj = np.array(vek_kraj, dtype=float)
    delta = np.float64(delta)

    _alati._vek_provera(osa_zavrtnja, 6, "osa_zavrtnja")
    _alati._vek_provera(vek_pocetak, 3, "vek_pocetak")
    _alati._vek_provera(vek_kraj, 3, "vek_kraj")

    osa_zavrtnja = mp.v_prostor_norm(osa_zavrtnja)

    # Potrebni su vektori red za proracun
    vek_pocetak = vek_pocetak.reshape(3)
    vek_kraj = vek_kraj.reshape(3)
    osa_zavrtnja = osa_zavrtnja.reshape(6)

    if not np.isclose(np.linalg.norm(osa_zavrtnja[:3]), 0.0):
        raise ValueError(
            "Osa zavrtnja nije translacija rotacija. Osa rotacije ose "
            "zavrtnja mora biti nulti vektor"
        )
    
    primarno_resenje = np.dot(osa_zavrtnja[3:], vek_kraj - vek_pocetak)
    
    if np.isclose(delta, 0.0):
        resenje = primarno_resenje
    else:
        resenje = (
            primarno_resenje + np.sqrt(
                primarno_resenje**2
                - np.linalg.norm(vek_kraj - vek_pocetak)**2
                + delta**2
            ),
            primarno_resenje - np.sqrt(
                primarno_resenje**2
                - np.linalg.norm(vek_kraj - vek_pocetak)**2
                + delta**2
            )
        )
    
    # S obzirom na izvor odakle je uzeto resenje, nisu navedeni uslovi
    # postojanja podproblema, prema temo cemo proveriti resenja na osnovu
    # glavne jednacine:
    # np.linalg.norm(
    #   mp.SE3_proizvod_3D(
    #       mp.exp_vek_ugao(osa_zavrtnja, resenje),
    #       vek_pocetak
    #   )
    # - vek_kraj
    # )
    # == delta
    # Sto se drugacije moze napisati kao
    # np.linalg.norm(
    #   resenje*osa_zavrtnja[3:]
    #   + vek_pocetak \
    #   - vek_kraj
    # ) == delta
    # zato sto su ose zavrtnja ciste translacije.
    # Takodje, u slucaju da podproblem ima dva resenja, trebaju oba da se
    # provere na isti nacin koji je prethodno naveden
    if isinstance(resenje, tuple):
        if np.isclose(
            np.linalg.norm(
                resenje[0]*osa_zavrtnja[3:] + vek_pocetak - vek_kraj
            ),
            delta
        ) and np.isclose(
            np.linalg.norm(
                resenje[1]*osa_zavrtnja[3:] + vek_pocetak - vek_kraj
            ),
            delta
        ):
            return resenje
        else:
            raise PardosGotorError(3)
    else:
        if np.isclose(
            np.linalg.norm(
                resenje*osa_zavrtnja[3:] + vek_pocetak - vek_kraj
            ),
            delta
        ):
            return resenje
        else:
            raise PardosGotorError(3)