# Attempting to create and save the diagram in a different way to ensure downloadability.
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create figure and axis for the ERD
fig, ax = plt.subplots(figsize=(10, 8))

# Function to create a table-like representation
def draw_table(x, y, title, fields):
    rect = mpatches.FancyBboxPatch((x, y), 3, 1.6, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="black", facecolor="#AED6F1")
    ax.add_patch(rect)
    plt.text(x + 1.5, y + 1.4, title, ha="center", va="top", fontsize=12, fontweight="bold")
    for i, field in enumerate(fields):
        plt.text(x + 0.1, y + 1.1 - i * 0.3, field, ha="left", va="center", fontsize=10)

# Draw each table for entities in the ERD
draw_table(1, 6, "Usuarios", [
    "ID_Usuario (PK)",
    "Enfoque",
    "Nivel",
    "Fecha_Ultima_Actualización"
])

draw_table(6, 6, "Objetivos_Diarios", [
    "ID_Objetivo (PK)",
    "ID_Usuario (FK)",
    "Categoría",
    "Tareas_Requeridas",
    "Dificultad"
])

draw_table(3.5, 2.5, "Progreso", [
    "ID_Progreso (PK)",
    "ID_Usuario (FK)",
    "Fecha",
    "Categoria",
    "Tareas_Completadas",
    "Porcentaje_Progreso"
])

# Draw relationship arrows
plt.arrow(3.4, 6.5, 2, 0, head_width=0.2, head_length=0.2, fc="black", ec="black")
plt.text(4.4, 6.7, "1:N", ha="center", fontsize=10)

plt.arrow(2.6, 6, 1.1, -2.6, head_width=0.2, head_length=0.2, fc="black", ec="black")
plt.text(3.1, 4, "1:N", ha="center", fontsize=10)

plt.arrow(7.4, 6, -1.2, -3, head_width=0.2, head_length=0.2, fc="black", ec="black")
plt.text(6.3, 4, "1:N", ha="center", fontsize=10)

# Set plot limits and remove axes
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.axis('off')

# Save the diagram as a PNG file
file_path = "/mnt/data/RiseNotes_ERD_Final.png"
plt.savefig(file_path, bbox_inches='tight')
plt.close(fig)

file_path
