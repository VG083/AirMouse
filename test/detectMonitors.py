import pygame

pygame.init()

# Cria uma janela de teste para obter as dimensões da tela
test_window = pygame.display.set_mode((1, 1))

# Obtém informações sobre o display
display_info = pygame.display.Info()

# Obtém o número de monitores
num_monitors = pygame.display.get_num_displays()

# Lista para armazenar os dicionários com as dimensões de cada monitor
monitors_list = []

# Obtém as dimensões de cada monitor e adiciona um dicionário na lista
for i in range(num_monitors):
    monitor_info = pygame.display.list_modes()[i]
    monitor_dict = {"Monitor": i+1, "Dimensões": monitor_info}
    monitors_list.append(monitor_dict)

# Fecha a janela de teste
pygame.quit()

# Imprime a lista de monitores com suas dimensões
print()
print(monitors_list)
print()

# Imprime cada monitor e suas dimensões de forma organizada
for monitor in monitors_list:
    print(f"Monitor {monitor['Monitor']}:")
    print(f"\t- Largura: {monitor['Dimensões'][0]}")
    print(f"\t- Altura: {monitor['Dimensões'][1]}")
