from enum import Enum


class Car(object):
    """class that holds car's characteristics and states, and changes this values when needed"""

    def __init__(self, startX: int, startY: int, speed: int, out :int):
        self._width = 20
        self._startCoord = CarPoint(startX, startY)
        self._backCoord = CarPoint(startX + self._width, startY)
        self._startSpeed = speed
        self._currentSpeed = speed
        self._state = CarState.run
        self._outDist = out
        self._speedCoef = 5
        self._accelCoef = 30

        self._waitingTime = None
        self._negAcceleratingSpeed = None
        self._crashedDownTime = None
        self._posAcceleratingSpeed = None
        self._stoppedTime = None
        self._brakeAcceleratingSpeed = None
        self._crashDownAccel = None
        self._crashIntoAccel = None
        self._crashedIntoTime = None
        self._crashedDownTime = None


    def move(self, car):

        if self._state == CarState.stoppedWaiting:
            if self._waitingTime == None: self._waitingTime = 30
            else: 
                self._waitingTime -= 1
                if self._waitingTime == 0:
                    self._waitingTime = None
                    self._state = CarState.accelerating

        elif self._state == CarState.run:
            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width
            if car:
                signal = self._checkDistance(car)
                if signal == CarSignal.SLOW_DOWN_SIGNAL:
                    self._state = CarState.slowingDown
                    return signal

        elif self._state == CarState.slowingDown:
            if self._negAcceleratingSpeed == None:
                self._negAcceleratingSpeed = self._calcAccelerateSpeed(car._currentSpeed)/self._accelCoef
            
            if car == None: self._state = CarState.accelerating
            elif self._currentSpeed + self._negAcceleratingSpeed > car._currentSpeed:
                self._currentSpeed += self._negAcceleratingSpeed
            elif self._currentSpeed + self._negAcceleratingSpeed <= car._currentSpeed:
                self._currentSpeed = car._currentSpeed
                self._negAcceleratingSpeed = None
                self._state = CarState.slowRun
            if self._currentSpeed == 0:
                self._state = CarState.stoppedWaiting
                self._negAcceleratingSpeed = None

            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width

            signal = self._checkDistance(car)
            if signal == CarSignal.CRASHED_INTO_SIGNAL:
                self._state = CarState.crashIntoBraking
                self._negAcceleratingSpeed = None
                return signal
            elif not signal:
                self._state = CarState.accelerating
                self._negAcceleratingSpeed = None

        elif self._state == CarState.crashedDown:
            if self._crashedDownTime == None: self._crashedDownTime = 40
            else: 
                self._crashedDownTime -= 1
                if self._crashedDownTime == 0:
                    self._crashedDownTime = None
                    self._state = CarState.accelerating

                signal = self._checkDistance(car if car else None)
                if signal == CarSignal.CRASHED_INTO_SIGNAL:
                    return CarSignal.BUMP_SIGNAL

        elif self._state == CarState.accelerating:
            if self._posAcceleratingSpeed == None:
                self._posAcceleratingSpeed = self._calcAccelerateSpeed(self._startSpeed)/self._accelCoef

            if self._currentSpeed + self._posAcceleratingSpeed < self._startSpeed:
                self._currentSpeed += self._posAcceleratingSpeed
            elif self._currentSpeed + self._posAcceleratingSpeed >= self._startSpeed:
                self._currentSpeed = self._startSpeed
                self._posAcceleratingSpeed = None
                self._state = CarState.run

            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width

            signal = self._checkDistance(car if car else None)
            if signal == CarSignal.SLOW_DOWN_SIGNAL:
                self._state = CarState.slowingDown
                self._posAcceleratingSpeed = None
                return signal

        elif self._state == CarState.stoppedImitation:
            if self._stoppedTime == None: self._stoppedTime = 30
            else: 
                self._stoppedTime -= 1
                if self._stoppedTime == 0:
                    self._stoppedTime = None
                    self._state = CarState.accelerating

        elif self._state == CarState.braking:
            if self._brakeAcceleratingSpeed == None:
                self._brakeAcceleratingSpeed = self._calcAccelerateSpeed(0)/self._accelCoef

            if self._currentSpeed + self._brakeAcceleratingSpeed > 0:
                self._currentSpeed += self._brakeAcceleratingSpeed
            elif self._currentSpeed + self._brakeAcceleratingSpeed <= 0:
                self._currentSpeed = 0
                self._brakeAcceleratingSpeed = None
                self._state = CarState.stoppedImitation

            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width

        elif self._state == CarState.crashedInto:
            if self._crashedIntoTime == None: self._crashedIntoTime = 50
            else: 
                self._crashedIntoTime -= 1
                if self._crashedIntoTime == 0:
                    self._crashedIntoTime = None
                    self._state = CarState.accelerating

                signal = self._checkDistance(car if car else None)
                if signal == CarSignal.CRASHED_INTO_SIGNAL:
                    return CarSignal.BUMP_SIGNAL

        elif self._state == CarState.slowRun:
            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width

            signal = self._checkDistance(car)
            if signal == CarSignal.CRASHED_INTO_SIGNAL:
                self._state = CarState.crashIntoBraking
                return signal
            if not signal:
                self._state = CarState.accelerating

        elif self._state == CarState.crashDownBraking:
            if self._crashDownAccel == None:
                self._crashDownAccel = (self._calcAccelerateSpeed(0) * 2) / self._accelCoef

            if self._currentSpeed + self._crashDownAccel > 0:
                self._currentSpeed += self._crashDownAccel
            elif self._currentSpeed + self._crashDownAccel <= 0:
                self._currentSpeed = 0
                self._crashDownAccel = None
                self._state = CarState.crashedDown

            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width

            signal = self._checkDistance(car if car else None)
            if signal == CarSignal.CRASHED_INTO_SIGNAL:
                return CarSignal.BUMP_SIGNAL

        elif self._state == CarState.crashIntoBraking:
            if self._crashIntoAccel == None:
                self._crashIntoAccel = (self._calcAccelerateSpeed(0) * 2) / self._accelCoef

            if self._currentSpeed + self._crashIntoAccel > 0:
                self._currentSpeed += self._crashIntoAccel
            elif self._currentSpeed + self._crashIntoAccel <= 0:
                self._currentSpeed = 0
                self._crashIntoAccel = None
                self._state = CarState.crashedInto

            self._startCoord.x += self._toMetersPerSecond(self._currentSpeed)/self._speedCoef
            self._backCoord.x = self._startCoord.x - self._width

            signal = self._checkDistance(car if car else None)
            if signal == CarSignal.CRASHED_INTO_SIGNAL:
                return CarSignal.BUMP_SIGNAL

        if self._startCoord.x > self._outDist:
            self._state = CarState.out
        return None


    def _checkDistance(self, firstCar):
        if not firstCar: return None
        if firstCar._backCoord.x - self._startCoord.x <= 0:
            return CarSignal.CRASHED_INTO_SIGNAL
        elif firstCar._backCoord.x - self._startCoord.x <= 3 * self._width:
            return CarSignal.SLOW_DOWN_SIGNAL
        return None


    def receiveSignal(self, signal):
        if signal == CarSignal.CRASHED_INTO_SIGNAL:
            if self._state not in (CarState.crashedInto, CarState.crashedDown):
                self._state = CarState.crashDownBraking
                self._waitingTime = None
                self._negAcceleratingSpeed = None
                self._crashedDownTime = None
                self._posAcceleratingSpeed = None
                self._stoppedTime = None
                self._brakeAcceleratingSpeed = None
                self._crashDownAccel = None
                self._crashIntoAccel = None
                self._crashedIntoTime = None
                self._crashedDownTime = None
            elif self._state == CarState.crashedInto:
                self._state = CarState.crashedDown
                self._crashedIntoTime = None
            self._startCoord.x += 5
            self._backCoord.x = self._startCoord.x - self._width
        elif signal == CarSignal.SLOW_DOWN_SIGNAL and self._state == CarState.slowRun:
            self._state = CarState.slowingDown
        elif signal == CarSignal.STOP_SIGNAL:
            self._state = CarState.braking
            self._waitingTime = None
            self._negAcceleratingSpeed = None
            self._crashedDownTime = None
            self._posAcceleratingSpeed = None
            self._stoppedTime = None
            self._brakeAcceleratingSpeed = None
            self._crashDownAccel = None
            self._crashIntoAccel = None
            self._crashedIntoTime = None
            self._crashedDownTime = None


    def bumpUp(self, coordX):
        self._startCoord.x = coordX + self._width + 4
        self._backCoord.x = self._startCoord.x - self._width
        if self._state == CarState.crashedInto:
            self._state = CarState.crashedDown


    def _toMetersPerSecond(self, speed: int):
        return speed * 1000 / 3600


    def _calcAccelerateSpeed(self, speed: int):
        s = self._calcStopDist()
        a = (speed * speed - self._currentSpeed * self._currentSpeed) / (2 * s)
        return a if a < 20 else 20


    def _calcStopDist(self):
        if self._currentSpeed == 0:
            return self._width * 3
        return (self._currentSpeed * self._currentSpeed) / (254 * 0.7)


    def getCoords(self):
        return self._startCoord, self._backCoord


    def getState(self):
        return self._state



class CarPoint():
    """class that represent point"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y



class CarState(Enum):
    """Enumeration for car states"""

    # next car - car in front of the current car
    # back car - car behind the current car

    stoppedWaiting = 1      # car waits until next car will run
    run = 2                 # car runs with constant current speed
    slowingDown = 3         # car slows down and current speed decreases
    accelerating = 4        # car speeds up and current speed increases until it will be equal to start speed
    crashedDown = 5         # car crashed by back car and waits some period of time
    out = 6                 # car is out of road; it will be deleted
    stoppedImitation = 7    # imitation of forced braking; car waits for some time 
    braking = 8             # car brakes because of next car
    crashedInto = 9         # car crashed into next car and waits some period of time
    slowRun = 10            # car runs slowly because of next car
    crashDownBraking = 11  # car crashed down by back car and now is braking
    crashIntoBraking = 12  # car crashed into next car and now is braking



class CarSignal(Enum):
    """Enumeration for car signals to communicate between cars"""

    CRASHED_INTO_SIGNAL = 1
    SLOW_DOWN_SIGNAL = 2
    STOP_SIGNAL = 3
    BUMP_SIGNAL = 4