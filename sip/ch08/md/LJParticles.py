import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class Verlet:
    def __init__(self, ode, dt):
        self.ode = ode
        self.dt = dt
        self.rate_counter = 0

    def get_rate_counter(self):
        return self.rate_counter

    def step(self):
        state = self.ode.get_state()
        rate = np.zeros_like(state)
        
        self.rate_counter = 1
        self.ode.get_rate(state, rate)
        
        for i in range(len(state)):
            state[i] += self.dt * rate[i]
        
        self.rate_counter = 2
        self.ode.get_rate(state, rate)
        
        for i in range(len(state)):
            state[i] += self.dt * rate[i]

class LJParticles:
    def __init__(self, nx, ny, Lx, Ly, initialKineticEnergy, dt, initialConfiguration):
        self.nx = nx
        self.ny = ny
        self.N = nx * ny
        self.Lx = Lx
        self.Ly = Ly
        self.rho = self.N / (self.Lx * self.Ly)
        self.initialKineticEnergy = initialKineticEnergy
        self.dt = dt
        self.initialConfiguration = initialConfiguration
        self.t = 0
        self.steps = 0
        self.totalPotentialEnergyAccumulator = 0
        self.totalKineticEnergyAccumulator = 0
        self.totalKineticEnergySquaredAccumulator = 0
        self.virialAccumulator = 0
        self.radius = 0.5
        self.state = np.zeros(1 + 4 * self.N)
        self.ax = np.zeros(self.N)
        self.ay = np.zeros(self.N)
        self.odeSolver = Verlet(self, self.dt)
        self.initialize()

    def initialize(self):
        self.t = 0
        self.rho = self.N / (self.Lx * self.Ly)
        self.resetAverages()
        if self.initialConfiguration == "triangular":
            self.setTriangularLattice()
        elif self.initialConfiguration == "rectangular":
            self.setRectangularLattice()
        else:
            self.setRandomPositions()
        self.setVelocities()
        self.computeAcceleration()

    def setRandomPositions(self):
        rMinimumSquared = 2.0**(1.0/3.0)
        for i in range(self.N):
            overlap = True
            while overlap:
                overlap = False
                self.state[4*i] = self.Lx * random.random()
                self.state[4*i+2] = self.Ly * random.random()
                j = 0
                while j < i and not overlap:
                    dx = self.pbcSeparation(self.state[4*i] - self.state[4*j], self.Lx)
                    dy = self.pbcSeparation(self.state[4*i+2] - self.state[4*j+2], self.Ly)
                    if dx*dx + dy*dy < rMinimumSquared:
                        overlap = True
                    j += 1

    def setRectangularLattice(self):
        dx = self.Lx / self.nx
        dy = self.Ly / self.ny
        for ix in range(self.nx):
            for iy in range(self.ny):
                i = ix + iy * self.nx
                self.state[4*i] = dx * (ix + 0.5)
                self.state[4*i+2] = dy * (iy + 0.5)

    def setTriangularLattice(self):
        dx = self.Lx / self.nx
        dy = self.Ly / self.ny
        for ix in range(self.nx):
            for iy in range(self.ny):
                i = ix + iy * self.nx
                self.state[4*i+2] = dy * (iy + 0.5)
                if iy % 2 == 0:
                    self.state[4*i] = dx * (ix + 0.25)
                else:
                    self.state[4*i] = dx * (ix + 0.75)

    def setVelocities(self):
        vxSum = 0.0
        vySum = 0.0
        for i in range(self.N):
            self.state[4*i+1] = random.random() - 0.5
            self.state[4*i+3] = random.random() - 0.5
            vxSum += self.state[4*i+1]
            vySum += self.state[4*i+3]
        
        vxcm = vxSum / self.N
        vycm = vySum / self.N
        for i in range(self.N):
            self.state[4*i+1] -= vxcm
            self.state[4*i+3] -= vycm
            
        v2sum = 0
        for i in range(self.N):
            v2sum += self.state[4*i+1]**2 + self.state[4*i+3]**2
            
        kineticEnergyPerParticle = 0.5 * v2sum / self.N
        rescale = np.sqrt(self.initialKineticEnergy / kineticEnergyPerParticle)
        
        for i in range(self.N):
            self.state[4*i+1] *= rescale
            self.state[4*i+3] *= rescale

    def getMeanTemperature(self):
        return self.totalKineticEnergyAccumulator / (self.N * self.steps)

    def getMeanEnergy(self):
        return self.totalKineticEnergyAccumulator / self.steps + self.totalPotentialEnergyAccumulator / self.steps

    def getMeanPressure(self):
        meanVirial = self.virialAccumulator / self.steps
        return 1.0 + 0.5 * meanVirial / (self.N * self.getMeanTemperature())

    def getHeatCapacity(self):
        meanTemperature = self.getMeanTemperature()
        meanKineticEnergySquared = self.totalKineticEnergySquaredAccumulator / self.steps
        meanKineticEnergy = self.totalKineticEnergyAccumulator / self.steps
        sigma2 = meanKineticEnergySquared - meanKineticEnergy**2
        denom = 1.0 - sigma2 / (self.N * meanTemperature**2)
        return self.N / denom

    def resetAverages(self):
        self.steps = 0
        self.virialAccumulator = 0
        self.totalPotentialEnergyAccumulator = 0
        self.totalKineticEnergyAccumulator = 0
        self.totalKineticEnergySquaredAccumulator = 0

    def computeAcceleration(self):
        self.ax.fill(0)
        self.ay.fill(0)
        self.totalPotentialEnergyAccumulator = 0
        self.virialAccumulator = 0
        for i in range(self.N - 1):
            for j in range(i + 1, self.N):
                dx = self.pbcSeparation(self.state[4*i] - self.state[4*j], self.Lx)
                dy = self.pbcSeparation(self.state[4*i+2] - self.state[4*j+2], self.Ly)
                r2 = dx*dx + dy*dy
                oneOverR2 = 1.0 / r2
                oneOverR6 = oneOverR2**3
                fOverR = 48.0 * oneOverR6 * (oneOverR6 - 0.5) * oneOverR2
                fx = fOverR * dx
                fy = fOverR * dy
                self.ax[i] += fx
                self.ay[i] += fy
                self.ax[j] -= fx
                self.ay[j] -= fy
                self.totalPotentialEnergyAccumulator += 4.0 * (oneOverR6**2 - oneOverR6)
                self.virialAccumulator += dx * fx + dy * fy

    def pbcSeparation(self, ds, L):
        if ds > 0:
            while ds > 0.5 * L:
                ds -= L
        else:
            while ds < -0.5 * L:
                ds += L
        return ds

    def pbcPosition(self, s, L):
        if s > 0:
            while s > L:
                s -= L
        else:
            while s < 0:
                s += L
        return s

    def get_rate(self, state, rate):
        if self.odeSolver.get_rate_counter() == 1:
            self.computeAcceleration()
        for i in range(self.N):
            rate[4*i] = state[4*i+1]
            rate[4*i+2] = state[4*i+3]
            rate[4*i+1] = self.ax[i]
            rate[4*i+3] = self.ay[i]
        rate[4*self.N] = 1

    def get_state(self):
        return self.state

    def step(self, xVelocityHistogram):
        self.odeSolver.step()
        totalKineticEnergy = 0
        for i in range(self.N):
            totalKineticEnergy += (self.state[4*i+1]**2 + self.state[4*i+3]**2)
            xVelocityHistogram.append(self.state[4*i+1])
            self.state[4*i] = self.pbcPosition(self.state[4*i], self.Lx)
            self.state[4*i+2] = self.pbcPosition(self.state[4*i+2], self.Ly)
        totalKineticEnergy *= 0.5
        self.steps += 1
        self.totalKineticEnergyAccumulator += totalKineticEnergy
        self.totalKineticEnergySquaredAccumulator += totalKineticEnergy**2
        self.t += self.dt

    def draw(self, ax):
        if self.state is None:
            return
        ax.clear()
        ax.set_xlim(0, self.Lx)
        ax.set_ylim(0, self.Ly)
        for i in range(self.N):
            circle = Circle((self.state[4*i], self.state[4*i+2]), self.radius, color='r')
            ax.add_artist(circle)
        rect = Rectangle((0, 0), self.Lx, self.Ly, fill=False)
        ax.add_artist(rect)
