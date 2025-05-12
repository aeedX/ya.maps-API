import pygame
import requests


def main():
    ll = list(map(float, input().split(',')))

    pygame.init()
    pygame.display.set_caption('ya.maps')
    size = width, height = 600, 450
    screen = pygame.display.set_mode(size)

    z = 10
    update_map(ll, z)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP and z < 21:
                    z += 1
                    update_map(ll, z)
                if event.key == pygame.K_PAGEDOWN and z > 0:
                    z -= 1
                    update_map(ll, z)
                moving_delta = 163.84 / 2 ** z
                if event.key == pygame.K_w and ll[1] + moving_delta < 85.05112878:
                    ll[1] += moving_delta
                    update_map(ll, z)
                if event.key == pygame.K_a and ll[0] - moving_delta > -180:
                    ll[0] -= moving_delta
                    update_map(ll, z)
                if event.key == pygame.K_s and ll[1] - moving_delta > -85.05112878:
                    ll[1] -= moving_delta
                    update_map(ll, z)
                if event.key == pygame.K_d and ll[0] + moving_delta < 180:
                    ll[0] += moving_delta
                    update_map(ll, z)
        screen.blit(pygame.image.load('map.png'), (0, 0))
        pygame.display.flip()


def update_map(ll, z):
    ll = ','.join(map(str, ll))
    response = requests.get(f'https://static-maps.yandex.ru/v1?ll={ll}&z={z}&apikey=f3a0fe3a-b07e-4840-a1da-06f18b2ddf13')
    with open('map.png', 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    main()
