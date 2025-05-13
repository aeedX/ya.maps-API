import pygame
import requests
# 83.776860,53.346785

def main():
    ll = list(map(float, input().split(',')))

    pygame.init()
    pygame.display.set_caption('ya.maps')
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont(None, 36)

    theme_btn = font.render('theme', True, (255, 255, 255))
    reset_btn = font.render('reset', True, (255, 255, 255))

    txt = ''
    active = False

    theme = 0
    pt = ''
    z = 10
    update_map(ll, z, theme, pt)


    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active:
                        ll = search(txt)
                        pt = ll.copy()
                        update_map(ll, z, theme, pt)
                    else:
                        txt = ''
                    active = not active
                else:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            txt = txt[:-1]
                        else:
                            txt += event.unicode
                        break
                if event.key == pygame.K_PAGEUP and z < 21:
                    z += 1
                    update_map(ll, z, theme, pt)
                if event.key == pygame.K_PAGEDOWN and z > 0:
                    z -= 1
                    update_map(ll, z, theme, pt)
                moving_delta = 163.84 / 2 ** z
                if event.key == pygame.K_w and ll[1] + moving_delta < 85.05112878:
                    ll[1] += moving_delta
                    update_map(ll, z, theme, pt)
                if event.key == pygame.K_a and ll[0] - moving_delta > -180:
                    ll[0] -= moving_delta
                    update_map(ll, z, theme, pt)
                if event.key == pygame.K_s and ll[1] - moving_delta > -85.05112878:
                    ll[1] -= moving_delta
                    update_map(ll, z, theme, pt)
                if event.key == pygame.K_d and ll[0] + moving_delta < 180:
                    ll[0] += moving_delta
                    update_map(ll, z, theme, pt)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < 75 and event.pos[1] > 450:
                    theme = (theme + 1) % 2
                    update_map(ll, z, theme, pt)
                if 100 < event.pos[0] < 160 and event.pos[1] > 450:
                    pt = ''
                    update_map(ll, z, theme, pt)
        screen.blit(theme_btn, (0, 462))
        screen.blit(reset_btn, (100, 462))
        screen.blit(font.render(txt, True, (255, 255, 255)), (400, 462))
        screen.blit(pygame.image.load('map.png'), (0, 0))
        pygame.display.flip()


def update_map(ll, z, theme, pt):
    ll = ','.join(map(str, ll))
    response = requests.get(f'https://static-maps.yandex.ru/v1?ll={ll}&z={z}&theme={"dark" if theme else "light"}'
                            f'{f"&pt={','.join(map(str, pt))}" if pt else ""}&apikey=f3a0fe3a-b07e-4840-a1da-06f18b2ddf13')
    with open('map.png', 'wb') as f:
        f.write(response.content)


def search(txt):
    return list(map(float, requests.get(f'http://geocode-maps.yandex.ru/1.x?geocode={txt}&format=json&'
                                       f'apikey=8013b162-6b42-4997-9691-77b7074026e0').json()["response"][
        "GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos'].split()))


if __name__ == '__main__':
    main()
