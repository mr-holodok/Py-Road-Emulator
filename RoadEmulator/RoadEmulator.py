from Car import Car, CarState, CarSignal, CarPoint
import random


class Road:
    
    def __init__(self, y):
        self._cars = list()
        self._Y = y

    def update(self):
        i = 0
        while i < len(self._cars):
            result = self._cars[i].move(None if i == 0 else self._cars[i-1])

            if self._cars[i].getState() == CarState.out:
                del self._cars[i]
                i -= 1
            elif result == CarSignal.CRASHED_INTO_SIGNAL:
                self._cars[i-1].receiveSignal(result)
                self._cars[i-1].move(None)
            elif result == CarSignal.SLOW_DOWN_SIGNAL and i + 1 < len(self._cars):
                self._cars[i+1].receiveSignal(result)
            elif result == CarSignal.BUMP_SIGNAL and i > 0:
                self._cars[i-1].bumpUp(self._cars[i]._startCoord.x)
            i += 1


    def addCar(self, outDist):
        self._cars.append(Car(20, self._Y, random.randint(50, 100), outDist))


    def findCar(self, posXY):
        if posXY[1] < self._Y - 10 or posXY[1] > self._Y + 10:
            return None
        for car in self._cars:
            if posXY[0] >= car._startCoord.x - 20 and posXY[0] <= car._startCoord.x + 20:
                return car
                
        