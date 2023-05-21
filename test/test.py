import pyautogui
import screeninfo

# Obtém informações sobre os monitores conectados
monitors = screeninfo.get_monitors()

for i, monitor in enumerate(monitors, 1):
    print(f"Monitor {i}:")
    print(f"\t- Largura: {monitor.width}")
    print(f"\t- Altura: {monitor.height}")
    print(f"\t- Posição à esquerda: {monitor.x}")
    print(f"\t- Posição ao topo: {monitor.y}")
    print()

# Imprime as informações de cada monitor
for monitor in monitors:
    print(monitor)
print("")
print(f"{pyautogui.position()}")