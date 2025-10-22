import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

class PBC:
    @staticmethod
    def separation(dx, L):
        return dx - L * round(dx / L)

    @staticmethod
    def position(x, L):
        return x - L * np.floor(x / L)

class HardDisks:
    def __init__(self, N, Lx, Ly):
        self.N = N
        self.Lx = Lx
        self.Ly = Ly
        self.x = np.zeros(N)
        self.y = np.zeros(N)
        self.vx = np.zeros(N)
        self.vy = np.zeros(N)
        self.collisionTime = np.full(N, 1.0E10)
        self.partner = np.zeros(N, dtype=int)
        self.keSum = 0
        self.virialSum = 0
        self.nextCollider = 0
        self.nextPartner = 0
        self.timeToCollision = 0
        self.t = 0
        self.bigTime = 1.0E10
        self.temperature = 0
        self.numberOfCollisions = 0

    def initialize(self, configuration):
        self.resetAverages()
        if configuration == "regular":
            self.setRegularPositions()
        else:
            self.setRandomPositions()
        self.setVelocities()
        for i in range(self.N):
            self.collisionTime[i] = self.bigTime
        for i in range(self.N - 1):
            for j in range(i + 1, self.N):
                self.checkCollision(i, j)

    def resetAverages(self):
        self.t = 0
        self.virialSum = 0

    def setVelocities(self):
        vxSum = 0
        vySum = 0
        for i in range(self.N):
            self.vx[i] = random.random() - 0.5
            self.vy[i] = random.random() - 0.5
            vxSum += self.vx[i]
            vySum += self.vy[i]
        vxCM = vxSum / self.N
        vyCM = vySum / self.N
        v2Sum = 0
        for i in range(self.N):
            self.vx[i] -= vxCM
            self.vy[i] -= vyCM
            v2Sum += self.vx[i] * self.vx[i] + self.vy[i] * self.vy[i]
        self.temperature = 0.5 * v2Sum / self.N

    def setRandomPositions(self):
        for i in range(self.N):
            overlap = True
            while overlap:
                overlap = False
                self.x[i] = self.Lx * random.random()
                self.y[i] = self.Ly * random.random()
                j = 0
                while j < i and not overlap:
                    dx = PBC.separation(self.x[i] - self.x[j], self.Lx)
                    dy = PBC.separation(self.y[i] - self.y[j], self.Ly)
                    if dx * dx + dy * dy < 1.0:
                        overlap = True
                    j += 1

    def setRegularPositions(self):
        dnx = np.sqrt(self.N)
        nx = int(dnx)
        if dnx - nx > 0.00001:
            nx += 1
        ax = self.Lx / nx
        ay = self.Ly / nx
        i = 0
        iy = 0
        while i < self.N:
            for ix in range(nx):
                if i < self.N:
                    self.y[i] = ay * (iy + 0.5)
                    if iy % 2 == 0:
                        self.x[i] = ax * (ix + 0.25)
                    else:
                        self.x[i] = ax * (ix + 0.75)
                    i += 1
            iy += 1

    def checkCollision(self, i, j):
        dvx = self.vx[i] - self.vx[j]
        dvy = self.vy[i] - self.vy[j]
        v2 = dvx * dvx + dvy * dvy
        for xCell in range(-1, 2):
            for yCell in range(-1, 2):
                dx = self.x[i] - self.x[j] + xCell * self.Lx
                dy = self.y[i] - self.y[j] + yCell * self.Ly
                bij = dx * dvx + dy * dvy
                if bij < 0:
                    r2 = dx * dx + dy * dy
                    discriminant = bij * bij - v2 * (r2 - 1)
                    if discriminant > 0:
                        tij = (-bij - np.sqrt(discriminant)) / v2
                        if tij < self.collisionTime[i]:
                            self.collisionTime[i] = tij
                            self.partner[i] = j
                        if tij < self.collisionTime[j]:
                            self.collisionTime[j] = tij
                            self.partner[j] = i

    def step(self):
        self.minimumCollisionTime()
        self.move()
        self.t += self.timeToCollision
        self.contact()
        self.setDefaultCollisionTimes()
        self.newCollisionTimes()
        self.numberOfCollisions += 1

    def minimumCollisionTime(self):
        self.timeToCollision = self.bigTime
        for k in range(self.N):
            if self.collisionTime[k] < self.timeToCollision:
                self.timeToCollision = self.collisionTime[k]
                self.nextCollider = k
        self.nextPartner = self.partner[self.nextCollider]

    def move(self):
        for k in range(self.N):
            self.collisionTime[k] -= self.timeToCollision
            self.x[k] = PBC.position(self.x[k] + self.vx[k] * self.timeToCollision, self.Lx)
            self.y[k] = PBC.position(self.y[k] + self.vy[k] * self.timeToCollision, self.Ly)

    def contact(self):
        dx = PBC.separation(self.x[self.nextCollider] - self.x[self.nextPartner], self.Lx)
        dy = PBC.separation(self.y[self.nextCollider] - self.y[self.nextPartner], self.Ly)
        dvx = self.vx[self.nextCollider] - self.vx[self.nextPartner]
        dvy = self.vy[self.nextCollider] - self.vy[self.nextPartner]
        factor = dx * dvx + dy * dvy
        delvx = -factor * dx
        delvy = -factor * dy
        self.vx[self.nextCollider] += delvx
        self.vy[self.nextCollider] += delvy
        self.vx[self.nextPartner] -= delvx
        self.vy[self.nextPartner] -= delvy
        self.virialSum += delvx * dx + delvy * dy

    def setDefaultCollisionTimes(self):
        self.collisionTime[self.nextCollider] = self.bigTime
        self.collisionTime[self.nextPartner] = self.bigTime
        for k in range(self.N):
            if self.partner[k] == self.nextCollider:
                self.collisionTime[k] = self.bigTime
            elif self.partner[k] == self.nextPartner:
                self.collisionTime[k] = self.bigTime

    def newCollisionTimes(self):
        for k in range(self.N):
            if k != self.nextCollider and k != self.nextPartner:
                self.checkCollision(k, self.nextPartner)
                self.checkCollision(k, self.nextCollider)

    def pressure(self):
        if self.t == 0:
            return 1.0
        return 1 + self.virialSum / (2 * self.t * self.N * self.temperature)

    def draw(self, ax):
        if self.x is None:
            return
        ax.clear()
        ax.set_xlim(0, self.Lx)
        ax.set_ylim(0, self.Ly)
        for i in range(self.N):
            circle = Circle((self.x[i], self.y[i]), 0.5, color='r')
            ax.add_artist(circle)
        rect = Rectangle((0, 0), self.Lx, self.Ly, fill=False)
        ax.add_artist(rect)
