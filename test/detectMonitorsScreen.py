import screeninfo

# Obtém informações sobre os monitores conectados
monitors = screeninfo.get_monitors()
# Imprime as informações de cada monitor
print(f"Lista:\n{monitors}\n\nLista:")
# Imprime as informações de cada monitor
for monitor in monitors:
    print(monitor)
print("")
# Imprime as informações de cada monitor
for i, monitor in enumerate(monitors, 1):
    print(f"Monitor {i}:")
    print(f"\t- Largura: {monitor.width}")
    print(f"\t- Altura: {monitor.height}")
    print(f"\t- Posição à esquerda: {monitor.x}")
    print(f"\t- Posição ao topo: {monitor.y}")
    print()