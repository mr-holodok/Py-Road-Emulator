import pygame
from RoadEmulator import Road
from Car import Car, CarSignal, CarState
import random


def main():
    pygame.init()
   
    pygame.display.set_caption("Road emulation program")
    screen = pygame.display.set_mode((1280,800))
    background = pygame.Surface(screen.get_size())  # Create empty pygame surface
    background.fill((0,0,0))     # Fill the background white color (red,green,blue)
    background = background.convert()  # Convert Surface to make blitting faster
    running = True

    highway = list()
    i = 50
    while i < screen.get_size()[1] - 100: 
        highway.append(Road(i)) 
        i += 100

    FPS = 30
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 500)
    counter = 1
      
    while running:
        milliseconds = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT: 
                highway[counter].addCar(screen.get_size()[0])
                counter = random.randint(0, len(highway)-1)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                pygame.draw.circle(background, (255,255,0), (x,y), 20)
                for road in highway:
                    car = road.findCar((x, y))
                    if car:
                        car.receiveSignal(CarSignal.STOP_SIGNAL)
                        break
            if event.type == pygame.QUIT:
                running = False
        for road in highway:
            road.update()
        screen.blit(background, (0,0))
        background.fill((0,0,0))
        for road in highway:
            for car in road._cars:
                pygame.draw.rect(background, colorPick(car.getState()), (car.getCoords()[0].x, car.getCoords()[0].y, car._width, 10))
        pygame.display.flip()


def colorPick(carState):
    if carState == CarState.run:
        return (255,255,255)
    elif carState == CarState.crashDownBraking or carState == CarState.crashIntoBraking or\
            carState == CarState.crashedDown or carState == CarState.crashedInto:
        return (255,0,0)
    elif carState == CarState.accelerating:
        return (0,255,0)
    elif carState == CarState.stoppedWaiting or carState == CarState.stoppedImitation:
        return (128,128,128)
    elif carState == CarState.slowingDown:
        return (255,255,0)
    elif carState == CarState.braking:
        return (150,0,0)
    elif carState == CarState.slowRun:
        return (0,0,255)
    elif carState == CarState.out:
        return (0,0,0)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()


