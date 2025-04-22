"""Upravljanje Niryo One manipulatorom"""

"""
*** BIBLIOTEKE ***
"""
from mehanika_robota.roboti import niryo_one as n_one
from mehanika_robota.mehanika import mat_prostor as mp
from mehanika_robota.mehanika import kinematika as kin
from mehanika_robota.mehanika import trajektorija as traj
import numpy as np
import pyniryo as pn
import os
import logging
from pathlib import Path
from msvcrt import getch

np.set_printoptions(14, suppress=None, floatmode='unique')

"""
*** KONSTANTE ***
"""
NIRYO_ONE_ETHERNET_IP = "169.254.200.200"


"""
*** FUNKCIJE ***
""" 
def gasenje_robota(robot: pn.NiryoRobot, izuzetak: Exception = None) -> None:
    """Procedura sigurnog gasenja robota

    Parametri
    ---------
    robot : pn.NiryoRobot
        Robot koji treba ugasiti
    izuzetak : Exception, opcionalno
        Ukoliko je nastala greska, pribeleziti izuzetak koji je nastao
        (automatska vrednost je None)
        
    Primeri
    -------
        >>> robot = pn.NiryoRobot("169.254.200.200")
        >>> gasenje_robota(robot)
        print("Robot je uspesno ugasen")
        >>> robot = pn.NiryoRobot("169.254.200.200")
        >>> gasenje_robota(robot, ValueError)
        print(
            "Doslo je do neocekivane greske, proverite greske.log za detalje"
        )
    """
    
    if izuzetak is not None:
        logging.error(
            f"{robot.get_hardware_status()}\n"
            f"-----------------------------------------------------------------\n"
            f"Pozicija zglobova = {robot.get_joints()}\n"
            f"-----------------------------------------------------------------\n"
            f"{izuzetak}\n\n"
        )
            
    robot.set_learning_mode(True)
    robot.close_connection()
    
    if izuzetak is not None:
        print(
            "Doslo je do neocekivane greske, proverite greske.log za vise "
            "detalja"
        )
    else:
        print("Robot je uspesno ugasen")


def main():
    # Log podesavanje
    logging.basicConfig(
        filename    = Path(__file__).parent / "greske.log",
        level       = logging.ERROR,
        format      = "%(asctime)s %(message)s",
        datefmt     = "Date: %d-%m-%Y   Time: %H:%M:%S"
    )

    # Povezivanje standardnom adresom robota za Ethernet TCP/IP komunikaciju
    try:
        robot = pn.NiryoRobot(NIRYO_ONE_ETHERNET_IP)
    except Exception as izuzetak:
        logging.error(f"{izuzetak}\n\n")
        print(
            "Nije moguce povezati se sa Niryo One robotom, videti greske.log "
            "za vise detalja"
        )
        return 
    
    try:
        # Kalibracija
        robot.calibrate(pn.CalibrateMode.AUTO)
        print("Pritisnite taster [d] da potvrdite rucnu kalibraciju: ")
        
        while getch().decode() != 'd':
            pass
        
        robot.calibrate(pn.CalibrateMode.MANUAL)
        print("Rucna kalibracija je uspesna!")

        # Matrica ciji ce redovi kasnije postati koordinate zglobova pri
        # odredjivanju prostoru zadataka, tj. ravni crtanja
        Teta_ravan = np.zeros((3, 6), dtype=float)
        
        i = 1
        while i <= 3:

            match i:
                case 1: kal_poz = "O"
                case 2: kal_poz = "x"
                case 3: kal_poz = "y"

            print(
                f"Priblizite Niryo One {i}. tacki prostoru zadataka u "
                + f"'{kal_poz}'"
                + f" kalibracionu poziciju i pritisnite taster [d]: "
            )

            while getch().decode() != 'd':
                pass
        
            Teta_ravan[i - 1] = robot.get_joints()
            
            i += 1

        # 3D matrica tacaka ravni sa SE(3) konfiguracijama kao i-ti element
        T_ravan_tacke = np.array(
            [n_one.dir_kin(Teta_ravan[i]) for i in range(Teta_ravan.shape[0])],
            dtype=float
        )

        # Matrica cije su kolone tacke ravni
        P_ravan = np.array(
            [T_ravan_tacke[i, :3, 3] for i in range(T_ravan_tacke.shape[0])],
            dtype=float
        ).T
        
        # Sastavlja SE(3) matricu gde se Oxy poklapa sa kalibracionim tackama,
        # z osa je vektorski proizvod prvih dveju ortova i matrica SO(3) je
        # projektovana na grupu SO(3) kako bi se smanjile numericke greske
        # Ekvivalentno ssa T_{s, ravan}
        T_ravan = mp.SE3_sastavi(
            mp.proj_grupa([
                mp.vek_norm(P_ravan[1] - P_ravan[0]),
                mp.vek_norm(P_ravan[2] - P_ravan[0]),
                mp.vek_norm(np.cross(
                    P_ravan[1] - P_ravan[0],
                    P_ravan[2] - P_ravan[0]
                ))
            ], 'SO3'),
            T_ravan_tacke[0, :3, 3]
        )

        # Matrica cije su kolone tacke kretanja u {s} koordinatnom sistemu.
        # Tacke redom odgavaraju narednim pozicijama:
        # 1. Iznad pocetne pozicije na ravni,
        # 2. pocetna pozicija na ravni,
        # 3. krajnja pozicija na ravni,
        # 4. iznad krajnje pozicije na ravni 
        P_traj = (T_ravan @ np.array(
            [[3e-2, 3e-2, 6e-2, 6e-2],
             [   0,    0,    0,    0],
             [1e-2,    0,    0, 1e-2],
             [   0,    0,    0,    0]], # homogene koordinate
            dtype=float
        ))[:3]

        robot.wait(1)

        e_omg = 1e-3
        e_v   = 0.5e-3

        print(T_ravan)
        print(P_ravan)

        return
    
        robot.set_arm_max_velocity(100)
        robot.move_joints(n_one.inv_kin(
            mp.SE3_sastavi(T_ravan[:3, :3], P_traj[:, 0]),
            e_omg,
            e_v
        )[0])

        robot.set_arm_max_velocity(10)

        traj_SE3 = traj.pravolin_traj(
            n_one.inv_kin(
                mp.SE3_sastavi(T_ravan[:3, :3], P_traj[:, 1]),
                e_omg,
                e_v
            )[0],
            n_one.inv_kin(
                mp.SE3_sastavi(T_ravan[:3, :3], P_traj[:, 2]),
                e_omg,
                e_v
            )[0],
            {"n": 50}
        )
        
        traj_joints = [
            n_one.inv_kin(traj_SE3[i], e_omg, e_v)[0]
            for i in range(len(traj_SE3))
        ]

        robot.execute_trajectory_from_poses_and_joints(traj_joints, ['joint'])

        robot.move_joints(n_one.inv_kin(
           mp.SE3_sastavi(T_ravan[:3, :3], P_traj[:, 3]),
            e_omg,
            e_v
        )[0])

        robot.set_arm_max_velocity(100)
        robot.move_to_home_pose()

    except Exception as izuzetak:
        # gasenje_robota(robot, izuzetak)
        robot.close_connection()
        raise izuzetak
    else:
        print("Program je uspesno zavrsen")
        gasenje_robota(robot)

if __name__ == "__main__":
    # Cisti terminal na COMMAND.COM i cmd.exe CLI
    os.system("cls")

    main()