from .Steifigkeitsmatrix import *
from .InputData import Input
import sympy as sp

import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D  # nötig für 3D-Plots
import matplotlib.patches as mpatches


class mainloop:
    def __init__(self):
        ##________ Subclasses __________##
        self.Inp = Input()
        self.ElemStem = ElemStema()
        ##_____ Class variables ___________##
        self.K_el_i_store = np.zeros((len(self.Inp.members), 14, 14))

        self.MY_el_i_store = np.zeros((len(self.Inp.members), 2, 1))
        self.VZ_el_i_store = np.zeros((len(self.Inp.members), 2, 1))

        self.MZ_el_i_store = np.zeros((len(self.Inp.members), 2, 1))
        self.VY_el_i_store = np.zeros((len(self.Inp.members), 2, 1))
        self.MX_el_i_store = np.zeros((len(self.Inp.members), 2, 1))

        self.MTP_el_i_store = np.zeros((len(self.Inp.members), 2, 1))
        self.MTS_el_i_store = np.zeros((len(self.Inp.members), 2, 1))
        self.N_el_i_store = np.zeros((len(self.Inp.members), 2, 1))

        ##_____ Class Functions____________##
        self.MainConvergence()

    def CalculateTransMat(self):
        print("Calculate Transmatrices")

        TransformationMatrices = np.zeros((len(self.Inp.members), 14, 14))
        na_memb = self.Inp.members["na"]
        ne_memb = self.Inp.members["ne"]
        for i in range(len(self.Inp.members["na"])):

            node_i = na_memb[i]  # Node number for node i of this member
            node_j = ne_memb[i]  # Node number for node j of this member

            # Index of DoF for this member
            ia = 2 * node_i - 2  # horizontal DoF at node i of this member
            ib = 2 * node_i - 1  # vertical DoF at node i of this member
            ja = 2 * node_j - 2  # horizontal DoF at node j of this member
            jb = 2 * node_j - 1  # vertical DoF at node j of this member

            # New positions = initial pos + cum deflection
            ix = self.Inp.nodes['x[m]'][node_i - 1]
            iy = self.Inp.nodes['y[m]'][node_i - 1]
            iz = self.Inp.nodes['z[m]'][node_i - 1]

            jx = self.Inp.nodes['x[m]'][node_j - 1]
            jy = self.Inp.nodes['y[m]'][node_j - 1]
            jz = self.Inp.nodes['z[m]'][node_j - 1]

            TM = self.ElemStem.TransformationMatrix([ix, iy, iz], [jx, jy, jz])

            TransformationMatrices[i, :, :] = TM
        print("Transmat")
        print(TransformationMatrices[0])
        return TransformationMatrices

    def BuildStructureStiffnessMatrix(self):
        """
        Standard construction of Primary and Structure stiffness matrix
        Construction of non-linear element stiffness matrix handled in a child function
        """
        Kp = np.zeros([self.Inp.nDoF, self.Inp.nDoF])  # Initialise the primary stiffness matrix
        self.member_length = []

        na_memb = self.Inp.members["na"]
        ne_memb = self.Inp.members["ne"]
        crosssec_members = self.Inp.members["cs"]

        for i in range(0, len(self.Inp.members["na"]), 1):
            node_i = na_memb[i]  # Node number for node i of this member
            node_j = ne_memb[i]  # Node number for node j of this member

            # New positions = initial pos + cum deflection
            ix = self.Inp.nodes['x[m]'][node_i - 1]
            iy = self.Inp.nodes['y[m]'][node_i - 1]
            iz = self.Inp.nodes['z[m]'][node_i - 1]

            jx = self.Inp.nodes['x[m]'][node_j - 1]
            jy = self.Inp.nodes['y[m]'][node_j - 1]
            jz = self.Inp.nodes['z[m]'][node_j - 1]

            dx = abs(ix - jx)
            dy = abs(iy - jy)
            dz = abs(iz - jz)

            length = np.sqrt(dx**2 + dy**2 + dz**2)
            self.member_length.append(length)

            num_cs = crosssec_members[i]
            mat_num_i = self.Inp.CrossSection.loc[self.Inp.CrossSection["No"] == num_cs, "material"].iloc[0]

            I_y_i = self.Inp.CrossSection.loc[self.Inp.CrossSection["No"] == num_cs, "Iy"].iloc[0]
            I_z_i = self.Inp.CrossSection.loc[self.Inp.CrossSection["No"] == num_cs, "Iz"].iloc[0]
            A_i = self.Inp.CrossSection.loc[self.Inp.CrossSection["No"] == num_cs, "A"].iloc[0]
            I_w_i = self.Inp.CrossSection.loc[self.Inp.CrossSection["No"] == num_cs, "Iw"].iloc[0]
            I_T_i = self.Inp.CrossSection.loc[self.Inp.CrossSection["No"] == num_cs, "It"].iloc[0]

            print("Material NUmber")
            print(mat_num_i)

            E_i = self.Inp.Material.loc[self.Inp.Material["No"] == mat_num_i, "E"].iloc[0]
            G_i = self.Inp.Material.loc[self.Inp.Material["No"] == mat_num_i, "G"].iloc[0]
            print("Material E_i")
            print(E_i)

            K_el_i = self.ElemStem.insert_elements(
                S=0,
                E=E_i,
                G=G_i,
                A=A_i,
                I_y=I_y_i,
                I_z=I_z_i,
                I_omega=I_w_i,
                I_T=I_T_i,
                cv=0,
                z1=0,
                cw=0,
                z2=0,
                c_thet=0,
                l=length,
            )

            K_el_i = np.matmul(self.TransMats[i].T, np.matmul(K_el_i, self.TransMats[i]))

            self.K_el_i_store[i] = K_el_i

            K_11 = K_el_i[0:7, 0:7]
            K_12 = K_el_i[0:7, 7:14]
            K_21 = K_el_i[7:14, 0:7]
            K_22 = K_el_i[7:14, 7:14]

            Kp[7 * (node_i - 1) : 7 * (node_i - 1) + 7, 7 * (node_i - 1) : 7 * (node_i - 1) + 7] += K_11

            Kp[7 * (node_i - 1) : 7 * (node_i - 1) + 7, 7 * (node_j - 1) : 7 * (node_j - 1) + 7] += K_12

            Kp[7 * (node_j - 1) : 7 * (node_j - 1) + 7, 7 * (node_i - 1) : 7 * (node_i - 1) + 7] += K_21

            Kp[7 * (node_j - 1) : 7 * (node_j - 1) + 7, 7 * (node_j - 1) : 7 * (node_j - 1) + 7] += K_22

        return Kp

    def RestraintData(self):
        """
        This functions implements the restraint data, which is loaded from the \n
        input file. \n
        There are 7 DOF's per node. \n
        Therefore the restrained DOF in the global stiffness matrix can be expressed by: \n
        GDOF = 7 * (node-1) + DOF \n
        """
        res_nodes = self.Inp.RestraintData["Node"]
        res_dof = self.Inp.RestraintData["Dof"]
        res_stif = self.Inp.RestraintData["Cp[MN/m]/[MNm/m]"]

        for i in range(len(res_dof)):
            glob_dof = 7 * (res_nodes[i] - 1) + res_dof[i]
            print("restrain ", glob_dof)
            self.GesMat[glob_dof, glob_dof] += res_stif[i]

    def LocalLoadVectorLine(self):
        """
        This function calculates the local loadvectors for each element \n
        and transforms them into the global coordinate system. \n
        Each local force vector is stored in a separate local force vector, \n
        which is taken into account, when the inner forces are calculated afterwards \n
        Members of the local load vector are: \n
            - Temperature loading  \n
            - Member forces \n
        """
        self.S_loc_elem_line = np.zeros((14, len(self.Inp.members)))
        S_glob_elem = np.zeros((14, len(self.Inp.members)))

        # Element Loading (line loads, single loads)

        res_mbr = self.Inp.ElementLoads["Member"]
        res_line_a = self.Inp.ElementLoads["qza"]
        res_line_b = self.Inp.ElementLoads["qze"]

        for i in range(0, len(res_mbr)):
            j = int(res_mbr[i] - 1)
            print("JJJ")
            print(j)
            print(res_mbr)
            TransMatj = self.TransMats[j]

            self.S_loc_elem_line[3, j] = +res_line_a[i] * self.member_length[j] / 2  # VZ
            self.S_loc_elem_line[10, j] = +res_line_a[i] * self.member_length[j] / 2

            self.S_loc_elem_line[4, j] = -res_line_a[i] * self.member_length[j] ** 2 / 12  # MY
            self.S_loc_elem_line[11, j] = +res_line_a[i] * self.member_length[j] ** 2 / 12

            S_loc = self.S_loc_elem_line[:, j]

            # global line loadings

            S_glob_elem[:, j] = np.matmul(np.transpose(TransMatj), S_loc)

        return S_glob_elem

    def LocalLoadVectorTemp(self):
        """
        This function calculates the local loadvectors for each element \n
        and transforms them into the global coordinate system. \n
        Each local force vector is stored in a separate local force vector, \n
        which is taken into account, when the inner forces are calculated afterwards \n
        Members of the local load vector are: \n
            - Temperature loading  \n
            - Member forces \n
        """
        self.S_loc_elem_temp = np.zeros((14, len(self.Inp.members)))
        S_glob_elem = np.zeros((14, len(self.Inp.members)))

        # Temperature Loading

        res_mbr = self.Inp.TemperatureForces["Member"]

        res_tem_dT = self.Inp.TemperatureForces["dT[K]"]
        res_tem_dTz = self.Inp.TemperatureForces["dTz[K]"]
        res_tem_dTy = self.Inp.TemperatureForces["dTy[K]"]

        for i in range(0, len(res_mbr)):
            j = int(res_mbr[i] - 1)
            TransMatj = self.TransMats[j]
            # Local temperature loadings
            self.S_loc_elem_temp[0, j] = -self.ElemStem.E * self.ElemStem.A * 1e-5 * res_tem_dT[i]  # N
            self.S_loc_elem_temp[7, j] = +self.ElemStem.E * self.ElemStem.A * 1e-5 * res_tem_dT[i]

            self.S_loc_elem_temp[2, j] = -self.ElemStem.E * self.ElemStem.I_z * 1e-5 * res_tem_dTy[i]  # MZ
            self.S_loc_elem_temp[9, j] = +self.ElemStem.E * self.ElemStem.I_z * 1e-5 * res_tem_dTy[i]

            self.S_loc_elem_temp[4, j] = -self.ElemStem.E * self.ElemStem.I_y * 1e-5 * res_tem_dTz[i]  # MY
            self.S_loc_elem_temp[11, j] = +self.ElemStem.E * self.ElemStem.I_y * 1e-5 * res_tem_dTz[i]

            S_loc = self.S_loc_elem_temp[:, j]

            # global temperature loadings

            S_glob_elem[:, j] = np.matmul(np.transpose(TransMatj), S_loc)

        return S_glob_elem

    def GlobalLoadVector(self):
        F_loc_temp = self.LocalLoadVectorTemp()
        F_loc_line = self.LocalLoadVectorLine()

        print("Local element temp")
        print(F_loc_temp)

        print("Local element line")
        print(F_loc_line)

        F_glob = np.zeros(self.Inp.nDoF)

        na_memb = self.Inp.members["na"]
        ne_memb = self.Inp.members["ne"]

        # Input of Member Forces
        for i in range(0, len(self.Inp.members)):
            node_i = na_memb[i]
            node_j = ne_memb[i]

            dof_Na = 7 * (node_i - 1)
            dof_Ne = 7 * (node_j - 1)

            dof_Vya = 7 * (node_i - 1) + 1
            dof_Vye = 7 * (node_j - 1) + 1

            dof_Vza = 7 * (node_i - 1) + 3
            dof_Vze = 7 * (node_j - 1) + 3

            dof_Mza = 7 * (node_i - 1) + 2
            dof_Mze = 7 * (node_j - 1) + 2

            dof_Mya = 7 * (node_i - 1) + 2
            dof_Mye = 7 * (node_j - 1) + 2

            F_glob[dof_Na] += F_loc_temp[0, i] + F_loc_line[0, i]
            F_glob[dof_Ne] += F_loc_temp[7, i] + F_loc_line[7, i]

            F_glob[dof_Vya] += F_loc_temp[1, i]
            F_glob[dof_Vye] += F_loc_temp[8, i]

            F_glob[dof_Vza] += F_loc_temp[3, i] + F_loc_line[3, i]
            F_glob[dof_Vze] += F_loc_temp[10, i] + F_loc_line[10, i]

            F_glob[dof_Mza] += F_loc_temp[2, i]
            F_glob[dof_Mze] += F_loc_temp[9, i]

            F_glob[dof_Mya] += F_loc_temp[4, i] + F_loc_line[4, i]
            F_glob[dof_Mye] += F_loc_temp[11, i] + F_loc_line[11, i]

        # Input of Nodal Forces
        res_nodes = self.Inp.NodalForces["Node"]
        res_dof = self.Inp.NodalForces["Dof"]
        res_forc = self.Inp.NodalForces["Value[MN/MNm]"]

        for i in range(0, len(res_nodes)):
            node_i = res_nodes[i]
            glob_index = (node_i - 1) * 7

            if res_dof[i] == "Fx" or res_dof[i] == "fx" or res_dof[i] == "FX":
                glob_index += 0
            elif res_dof[i] == "Fy" or res_dof[i] == "fy" or res_dof[i] == "FY":
                glob_index += 1
            elif res_dof[i] == "Fz" or res_dof[i] == "fz" or res_dof[i] == "FZ":
                glob_index += 3

            F_glob[glob_index] += res_forc[i]

        print("Force vector ", F_glob)
        print("Local force vectors ", self.S_loc_elem_temp)

        return F_glob

    def SolveDisplacement(self):
        u_glob = np.linalg.solve(self.GesMat, self.FGes)
        return u_glob

    def StoreLocalDisplacements(self):
        u_el = np.zeros([14, len(self.Inp.members["na"])])  # Initialise the primary stiffness matrix

        na_memb = self.Inp.members["na"]
        ne_memb = self.Inp.members["ne"]

        for i in range(0, len(self.Inp.members["na"]), 1):
            numa = 7 * (na_memb[i] - 1)
            nume = 7 * (ne_memb[i] - 1)

            u_el[0:7, i] = self.u_ges[numa : numa + 7]
            u_el[7:14, i] = self.u_ges[nume : nume + 7]

            # u_el[:,i] = np.matmul(self.TransMats[i],u_el[:,i])

        return u_el

    def CalculateLocalInnerForces(self):
        s_el = np.zeros([14, len(self.Inp.members["na"])])

        for i in range(0, len(self.Inp.members["na"]), 1):
            s_el[:, i] = np.matmul(self.K_el_i_store[i], self.u_el[:, i])
            self.MZ_el_i_store[i] = np.array([s_el[2, i] * (-1), s_el[9, i]]).reshape(2, 1)  # Left is *(-1)
            self.MY_el_i_store[i] = np.array([s_el[4, i] * (-1), s_el[11, i]]).reshape(2, 1)  # Left is *(-1)
            self.MX_el_i_store[i] = np.array([s_el[5, i] * (-1), s_el[12, i]]).reshape(2, 1)  # Left is *(-1)

            self.N_el_i_store[i] = np.array([s_el[0, i] * (-1), s_el[7, i]]).reshape(2, 1)  # Left is *(-1)
            self.VY_el_i_store[i] = np.array([s_el[1, i] * (-1), s_el[8, i]]).reshape(2, 1)  # Left is *(-1)
            self.VZ_el_i_store[i] = np.array([s_el[3, i] * (-1), s_el[10, i]]).reshape(2, 1)  # Left is *(-1)

            # Explicit transformation in local coordinates

            self.N_el_i_store[i] = (
                self.N_el_i_store[i] * self.TransMats[i][0, 0]
                + self.VY_el_i_store[i] * self.TransMats[i][0, 1]
                + self.VZ_el_i_store[i] * self.TransMats[i][0, 3]
                - np.array([-self.S_loc_elem_temp[0, i], self.S_loc_elem_temp[7, i]]).reshape(2, 1)  # Left is * (-1)
                # - np.array([-self.S_loc_elem_line[0, i], self.S_loc_elem_line[7, i]]).reshape(2, 1)   # Left is * (-1)
            )

            self.MY_el_i_store[i] = (
                self.MX_el_i_store[i] * self.TransMats[i][4, 5]
                + self.MY_el_i_store[i] * self.TransMats[i][4, 4]
                + self.MZ_el_i_store[i] * self.TransMats[i][4, 2]
                - np.array([-self.S_loc_elem_temp[4, i], self.S_loc_elem_temp[11, i]]).reshape(2, 1)  # Left is * (-1)
                # - np.array([-self.S_loc_elem_line[4, i], self.S_loc_elem_line[11, i]]).reshape(2, 1)   # Left is * (-1)
            )

        return s_el

    def MainConvergence(self):

        self.TransMats = self.CalculateTransMat()
        self.GesMat = self.BuildStructureStiffnessMatrix()

        self.RestraintData()

        self.FGes = self.GlobalLoadVector()

        self.u_ges = self.SolveDisplacement()

        self.u_el = self.StoreLocalDisplacements()

        self.s_el = self.CalculateLocalInnerForces()

    def plot_structure_3d(self, nodes, na_memb, ne_memb):
        """
        Plot the undeformed 3D structure.

        Parameters:
        nodes: dict with keys ['x[m]', 'y[m]', 'z[m]']
        na_memb, ne_memb: lists with node IDs for start and end of members
        """
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # Plot all members
        for i in range(len(na_memb)):
            node_i = na_memb[i]
            node_j = ne_memb[i]

            ix = nodes['x[m]'][node_i - 1]
            iy = nodes['y[m]'][node_i - 1]
            iz = nodes['z[m]'][node_i - 1]

            jx = nodes['x[m]'][node_j - 1]
            jy = nodes['y[m]'][node_j - 1]
            jz = nodes['z[m]'][node_j - 1]

            X = [ix, jx]
            Y = [iy, jy]
            Z = [iz, jz]

            ax.plot(X, Y, Z, color='black', lw=1.0)

        # Achsenbeschriftung und Titel
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.set_zlabel("Z [m]")
        ax.set_title("Unverformte Struktur")

        return fig, ax

    def calculate_orthogonal_unit_vector_cross_product(self, xi, zi, xj, zj):
        """
        Berechnet einen normierten orthogonalen Vektor zur Strukturlinie von (xi, zi) nach (xj, zj)
        mittels Kreuzprodukt.

        Parameter:
        - xi, zi: Koordinaten des Startknotens
        - xj, zj: Koordinaten des Endknotens

        Rückgabe:
        - unit_vector_pos: NumPy-Array des normierten orthogonalen Vektors für positives My
        - unit_vector_neg: NumPy-Array des normierten orthogonalen Vektors für negatives My
        """
        # Richtungsvektor in 3D (y-Komponente ist 0)
        v = np.array([xj - xi, 0, zj - zi])

        # Einheitsvektor entlang der y-Achse
        y_unit = np.array([0, 1, 0])

        # Kreuzprodukt berechnen
        perp_vector = np.cross(v, y_unit)  # Ergebnis ist ebenfalls ein 3D-Vektor

        # Extrahiere die x und z Komponenten
        perp_vector_2d = perp_vector[[0, 2]]

        # Normierung
        norm = np.linalg.norm(perp_vector_2d)
        if norm == 0:
            raise ValueError("Die Strukturlinie hat keine Länge. Start- und Endknoten sind identisch.")

        unit_vector = perp_vector_2d / norm

        # Für positives und negatives My
        unit_vector_pos = unit_vector
        unit_vector_neg = -unit_vector

        return unit_vector_pos, unit_vector_neg

    def plot_moment_my_2d(self, ax, xi, zi, my_local, unit_vector, scale=1):
        """
        Plot eines Biegemoments My in 2D (x-z-Ebene) orthogonal zur Strukturlinie.

        Parameter:
        ax : matplotlib.axes.Axes
            Die 2D-Achse zum Plotten
        xi, zi : float
            Startpunkt (globale Koordinaten in x und z)
        my_local : float
            Lokaler My-Wert
        unit_vector : array-like, shape (2,)
            Normalisierter orthogonaler Vektor für das Moment
        scale : float, optional
            Maßstabsfaktor für die Pfeillänge
        """
        if my_local == 0:
            return  # Kein Moment zu plotten

        # Kleine Verbindungslinie vom Knoten zum Start des Pfeils
        connection_length = 0.05 * scale  # Anpassbarer Wert

        conn_x = xi + connection_length * unit_vector[0] * my_local * scale
        conn_z = zi + connection_length * unit_vector[1] * my_local * scale

        if my_local >= 0:
            ax.plot([xi, conn_x], [zi, conn_z], color='blue', linewidth=1)
        if my_local < 0:
            ax.plot([xi, conn_x], [zi, conn_z], color='red', linewidth=1)

        # Berechnung des Vektors, skaliert durch Moment und Maßstabsfaktor
        vec = scale * my_local * unit_vector

        # Farbwahl basierend auf dem Vorzeichen des Moments
        color = 'blue' if my_local >= 0 else 'red'

        # Plotten des Pfeils
        # ax.arrow(conn_x, conn_z, vec[0], vec[1],
        #          head_width=0.05 * scale, head_length=0.1 * scale,
        #          fc=color, ec=color, length_includes_head=True)

        # Berechnung des Endpunkts für die Textplatzierung
        x_end = conn_x
        z_end = conn_z

        # Moment-Text
        moment_text = f"My = {my_local:.3f} MNm"

        # Textversatz für bessere Sichtbarkeit
        text_offset = 0  # 0.05 * scale
        ax.text(
            x_end + text_offset * unit_vector[0],
            z_end + text_offset * unit_vector[1],
            moment_text,
            color=color,
            fontsize=8,
        )

        return conn_x, conn_z

    def plot_all_My_2d(self, ax, nodes, na_memb, ne_memb, My_el_i_store, scale=0.4):
        """
        Plot My-Momente für alle Elemente an ihren Knoten in 2D (x-z-Ebene).

        Parameter:
        ax : matplotlib.axes.Axes
            Die 2D-Achse zum Plotten
        nodes : dict
            Dictionary mit Knotenkordinaten
        na_memb, ne_memb : Listen
            Listen von Knotennummern für die Elemente
        My_el_i_store : ndarray
            Array von My-Werten pro Element und Knoten
        scale : float, optional
            Maßstabsfaktor für die Pfeile
        """
        for i in range(len(na_memb)):
            node_i = na_memb[i]
            node_j = ne_memb[i]

            ix = nodes['x[m]'][node_i - 1]
            iz = nodes['z[m]'][node_i - 1]

            jx = nodes['x[m]'][node_j - 1]
            jz = nodes['z[m]'][node_j - 1]

            # Berechne die Einheitsvektoren für positives und negatives My mittels Kreuzprodukt
            try:
                unit_vector_pos, unit_vector_neg = self.calculate_orthogonal_unit_vector_cross_product(ix, iz, jx, jz)
                print(f"Element {i+1}: unit_vector_pos = {unit_vector_pos}, unit_vector_neg = {unit_vector_neg}")
            except ValueError as e:
                print(f"Fehler bei Mitglied {i+1}: {e}")
                continue

            # Lokales My an Knoten a / b
            My_a = My_el_i_store[i, 0, 0]  # [i,0] -> Knoten a
            My_b = My_el_i_store[i, 1, 0]  # [i,1] -> Knoten b

            try:
                # 1) Pfeil am Knoten a
                conn_ix, conn_iz = self.plot_moment_my_2d(ax, ix, iz, My_a, unit_vector_pos, scale=scale)
                # 2) Pfeil am Knoten b
                conn_jx, conn_jz = self.plot_moment_my_2d(ax, jx, jz, My_b, unit_vector_pos, scale=scale)
                ax.plot([conn_ix, conn_jx], [conn_iz, conn_jz], color='black', linewidth=1)
            except:
                pass

        # Hinzufügen einer Legende zur Unterscheidung
        red_patch = mpatches.Patch(color='blue', label='Positives My')
        blue_patch = mpatches.Patch(color='red', label='Negatives My')
        ax.legend(handles=[red_patch, blue_patch])

    def plot_normalforce_N_2d(self, ax, xi, zi, N_local, unit_vector, scale=1):
        """
        Plot eines Biegemoments My in 2D (x-z-Ebene) orthogonal zur Strukturlinie.

        Parameter:
        ax : matplotlib.axes.Axes
            Die 2D-Achse zum Plotten
        xi, zi : float
            Startpunkt (globale Koordinaten in x und z)
        N_local : float
            Lokaler N-Wert
        unit_vector : array-like, shape (2,)
            Normalisierter orthogonaler Vektor für das Moment
        scale : float, optional
            Maßstabsfaktor für die Pfeillänge
        """

        if N_local == 0:
            return  # Keine Kraft zu plotten

        # Kleine Verbindungslinie vom Knoten zum Start des Pfeils
        connection_length = 0.05 * scale  # Anpassbarer Wert

        conn_x = xi + connection_length * unit_vector[0] * N_local * scale
        conn_z = zi + connection_length * unit_vector[1] * N_local * scale

        if N_local >= 0:
            ax.plot([xi, conn_x], [zi, conn_z], color='blue', linewidth=1)
        if N_local < 0:
            ax.plot([xi, conn_x], [zi, conn_z], color='red', linewidth=1)

        # Berechnung des Vektors, skaliert durch Moment und Maßstabsfaktor
        vec = scale * N_local * unit_vector

        # Farbwahl basierend auf dem Vorzeichen des Moments
        color = 'blue' if N_local >= 0 else 'red'

        # Plotten des Pfeils
        # ax.arrow(conn_x, conn_z, vec[0], vec[1],
        #          head_width=0.05 * scale, head_length=0.1 * scale,
        #          fc=color, ec=color, length_includes_head=True)

        # Berechnung des Endpunkts für die Textplatzierung
        x_end = conn_x
        z_end = conn_z

        # Moment-Text
        moment_text = f"N = {N_local:.3f} MNm"

        # Textversatz für bessere Sichtbarkeit
        text_offset = 0  # 0.05 * scale
        ax.text(
            x_end + text_offset * unit_vector[0],
            z_end + text_offset * unit_vector[1],
            moment_text,
            color=color,
            fontsize=8,
        )

        return conn_x, conn_z

    def plot_all_N_2d(self, ax, nodes, na_memb, ne_memb, N_el_i_store, scale=0.4):
        """
        Plot N-Momente für alle Elemente an ihren Knoten in 2D (x-z-Ebene).

        Parameter:
        ax : matplotlib.axes.Axes
            Die 2D-Achse zum Plotten
        nodes : dict
            Dictionary mit Knotenkordinaten
        na_memb, ne_memb : Listen
            Listen von Knotennummern für die Elemente
        N_el_i_store : ndarray
            Array von N-Werten pro Element und Knoten
        scale : float, optional
            Maßstabsfaktor für die Pfeile
        """
        for i in range(len(na_memb)):
            node_i = na_memb[i]
            node_j = ne_memb[i]

            ix = nodes['x[m]'][node_i - 1]
            iz = nodes['z[m]'][node_i - 1]

            jx = nodes['x[m]'][node_j - 1]
            jz = nodes['z[m]'][node_j - 1]

            # Berechne die Einheitsvektoren für positives und negatives My mittels Kreuzprodukt
            try:
                unit_vector_pos, unit_vector_neg = self.calculate_orthogonal_unit_vector_cross_product(ix, iz, jx, jz)
                print(f"Element {i+1}: unit_vector_pos = {unit_vector_pos}, unit_vector_neg = {unit_vector_neg}")
            except ValueError as e:
                print(f"Fehler bei Mitglied {i+1}: {e}")
                continue

            # Lokales My an Knoten a / b
            N_a = N_el_i_store[i, 0, 0]  # [i,0] -> Knoten a
            N_b = N_el_i_store[i, 1, 0]  # [i,1] -> Knoten b

            try:
                # 1) Pfeil am Knoten a
                conn_ix, conn_iz = self.plot_normalforce_N_2d(ax, ix, iz, N_a, unit_vector_pos, scale=scale)
                # 2) Pfeil am Knoten b
                conn_jx, conn_jz = self.plot_normalforce_N_2d(ax, jx, jz, N_b, unit_vector_pos, scale=scale)
                ax.plot([conn_ix, conn_jx], [conn_iz, conn_jz], color='black', linewidth=1)
            except:
                pass

        # Hinzufügen einer Legende zur Unterscheidung
        red_patch = mpatches.Patch(color='blue', label='Positives N')
        blue_patch = mpatches.Patch(color='red', label='Negatives N')
        ax.legend(handles=[red_patch, blue_patch])

    def plot_structure_2d(self, nodes, na_memb, ne_memb):
        """
        Plot der unverformten 2D-Struktur in der x-z-Ebene.

        Parameter:
        nodes: dict mit den Schlüsseln ['x[m]', 'y[m]', 'z[m]']
        na_memb, ne_memb: Listen mit Knoten-IDs für Start und Ende der Elemente
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # Alle Elemente plotten
        for i in range(len(na_memb)):
            node_i = na_memb[i]
            node_j = ne_memb[i]

            ix = nodes['x[m]'][node_i - 1]
            iz = nodes['z[m]'][node_i - 1]

            jx = nodes['x[m]'][node_j - 1]
            jz = nodes['z[m]'][node_j - 1]

            X = [ix, jx]
            Z = [iz, jz]

            ax.plot(X, Z, color='black', lw=1.0)

        # Achsenbeschriftung und Titel
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Z [m]")
        ax.set_title("Unverformte Struktur (x-z-Ebene)")
        ax.grid(True)

        return fig, ax

    def plot_structure_with_moments_2d(self, scale=0.4):
        """
        Kombinierte Methode zum Plotten der Struktur und der Biegemomente My in 2D (x-z-Ebene).

        Parameter:
        scale : float, optional
            Skalierungsfaktor für die Momente
        """
        fig, ax = self.plot_structure_2d(self.Inp.nodes, self.Inp.members["na"], self.Inp.members["ne"])

        # Plot der Biegemomente My mittels Kreuzprodukt
        self.plot_all_My_2d(
            ax, self.Inp.nodes, self.Inp.members["na"], self.Inp.members["ne"], self.MY_el_i_store, scale=scale
        )

        # Achsenlimits automatisch anpassen und gleiches Seitenverhältnis
        ax.set_aspect('equal', adjustable='datalim')
        ax.relim()
        ax.autoscale_view()

        return fig, ax

    def plot_structure_with_normalforces_2d(self, scale=0.4):
        """
        Kombinierte Methode zum Plotten der Struktur und der Biegemomente My in 2D (x-z-Ebene).

        Parameter:
        scale : float, optional
            Skalierungsfaktor für die Momente
        """
        fig, ax = self.plot_structure_2d(self.Inp.nodes, self.Inp.members["na"], self.Inp.members["ne"])

        # Plot der Biegemomente My mittels Kreuzprodukt
        self.plot_all_N_2d(
            ax, self.Inp.nodes, self.Inp.members["na"], self.Inp.members["ne"], self.N_el_i_store, scale=scale
        )

        # Achsenlimits automatisch anpassen und gleiches Seitenverhältnis
        ax.set_aspect('equal', adjustable='datalim')
        ax.relim()
        ax.autoscale_view()

        return fig, ax


# # Beispielhafte Hauptfunktion
# if __name__ == "__main__":
#     import matplotlib.patches as mpatches

#     # 1) Erzeuge Instanz der Klasse 'mainloop'
#     Calc = mainloop()

#     # 2) Plot der Struktur mit Biegemomenten in 2D
#     fig, ax = Calc.plot_structure_with_moments_2d(scale=5)  # Angepasster Skalierungsfaktor
#     ax.invert_yaxis()
#     # 3) Speichern des Plots als EPS-Datei
#     plt.savefig("plots/ClampHinged_Inclination.eps", format='eps')

#     plt.show()
#     fig, ax = Calc.plot_structure_with_normalforces_2d(scale=5)
#     ax.invert_yaxis()

#     # 4) Anzeige des Plots
#     plt.show()
