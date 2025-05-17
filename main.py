import pygame
import requests
# 83.776860,53.346785

def main():
    ll = list(map(float, input().split(',')))

    pygame.init()
    pygame.display.set_caption('ya.maps')
    size = width, height = 600, 535
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont(None, 32)
    font2 = pygame.font.SysFont(None, 26)

    theme_btn = font.render('theme', True, (255, 255, 255))
    reset_btn = font.render('reset', True, (255, 255, 255))
    index_btn = font.render('index', True, (255, 255, 255))

    txt = ''
    active = False
    address = ''
    index = False

    params = {
        'll': ll,
        'theme': 0,
        'pt': '',
        'z': 10
    }
    update_map(params)
    rmb = False

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active:
                        res = search_org(ll, txt) if rmb else search(txt); rmb = False
                        if res:
                            params['ll'], address = res
                            params['pt'] = params['ll'].copy()
                            update_map(params)
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
                if event.key == pygame.K_PAGEUP and params['z'] < 21:
                    params['z'] += 1
                    update_map(params)
                if event.key == pygame.K_PAGEDOWN and params['z'] > 0:
                    params['z'] -= 1
                    update_map(params)
                moving_delta = 163.84 / 2 ** params['z']
                if event.key == pygame.K_w and params['ll'][1] + moving_delta < 85.05112878:
                    params['ll'][1] += moving_delta
                    update_map(params)
                if event.key == pygame.K_a and params['ll'][0] - moving_delta > -180:
                    params['ll'][0] -= moving_delta
                    update_map(params)
                if event.key == pygame.K_s and params['ll'][1] - moving_delta > -85.05112878:
                    params['ll'][1] -= moving_delta
                    update_map(params)
                if event.key == pygame.K_d and params['ll'][0] + moving_delta < 180:
                    params['ll'][0] += moving_delta
                    update_map(params)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] < 75 and event.pos[1] > 450:
                        params['theme'] = (params['theme'] + 1) % 2
                        update_map(params)
                    elif 80 < event.pos[0] < 140 and event.pos[1] > 450:
                        params['pt'] = ''
                        address = ''
                        update_map(params)
                    elif 150 < event.pos[0] < 210 and event.pos[1] > 450:
                        index = not index
                    else:
                        params['ll'] = [params['ll'][0] + (event.pos[0] - 600 / 2) * 0.00136 * 2 ** 10 / 2 ** params['z'],
                                        params['ll'][1] - (event.pos[1] - 450 / 2) * 0.00083 * 2 ** 10 / 2 ** params['z']]
                        res = search(','.join(map(str, params['ll'])))
                        if res:
                            params['ll'], address = res
                            params['pt'] = params['ll'].copy()
                            update_map(params)
                elif event.button == 3:
                    params['ll'] = [params['ll'][0] + (event.pos[0] - 600 / 2) * 0.00136 * 2 ** 10 / 2 ** params['z'],
                                    params['ll'][1] - (event.pos[1] - 450 / 2) * 0.00083 * 2 ** 10 / 2 ** params['z']]
                    update_map(params)
                    rmb = True
        screen.blit(theme_btn, (0, 462))
        screen.blit(reset_btn, (80, 462))
        screen.blit(index_btn, (150, 462))
        screen.blit(font2.render(txt, True, (255, 255, 255)), (240, 462))
        if address:
            screen.blit(font2.render(f'{address["formatted"]}{f", {address['postal_code']}" if index else ""}', True, (255, 255, 255)), (0, 500))
        screen.blit(pygame.image.load('map.png'), (0, 0))
        pygame.display.flip()


def update_map(p):
    ll = ','.join(map(str, p['ll']))
    response = requests.get(f'https://static-maps.yandex.ru/v1?ll={ll}&z={p["z"]}&theme={"dark" if p["theme"] else "light"}'
                            f'{f"&pt={','.join(map(str, p["pt"]))}" if p["pt"] else ""}&'
                            f'apikey=f3a0fe3a-b07e-4840-a1da-06f18b2ddf13')
    with open('map.png', 'wb') as f:
        f.write(response.content)


def search(txt):
    response =  requests.get(f'http://geocode-maps.yandex.ru/1.x?geocode={txt}&format=json&'
                                             f'apikey=8013b162-6b42-4997-9691-77b7074026e0').json()
    if response:
        print(txt)
        response = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return list(map(float, response['Point']['pos'].split())), response['metaDataProperty']['GeocoderMetaData']['Address']
    return None


def search_org(ll, txt):
    response =  requests.get(f'https://search-maps.yandex.ru/v1?ll={','.join(map(str, ll))}&text={txt}&results=1&format=json&'
                                             f'lang=ru&apikey=dda3ddba-c9ea-4ead-9010-f43fbc15c6e3').json()["features"]
    if response:
        response = response[0]["geometry"]['coordinates']
        return search(','.join(map(str, response)))


if __name__ == '__main__':
    main()
