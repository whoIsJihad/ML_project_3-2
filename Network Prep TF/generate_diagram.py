import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')

# Titles and layout
plt.title("Sensor vs Actuator in IoT", fontsize=16, fontweight='bold', pad=20)

# Draw Sensor box (Input)
sensor_box = patches.Rectangle((0.05, 0.3), 0.25, 0.4, fill=True, color='#add8e6', lw=2, ec='black')
ax.add_patch(sensor_box)
ax.text(0.175, 0.5, 'Sensor\n\nPhysical Environment\n↓\nDigital Signal', 
        ha='center', va='center', fontsize=11, fontweight='bold')

# Draw Processing Unit
proc_box = patches.Rectangle((0.4, 0.35), 0.2, 0.3, fill=True, color='#d3d3d3', lw=2, ec='black')
ax.add_patch(proc_box)
ax.text(0.5, 0.5, 'Microcontroller\n(Logic/Processing)', 
        ha='center', va='center', fontsize=10)

# Draw Actuator box (Output)
actuator_box = patches.Rectangle((0.7, 0.3), 0.25, 0.4, fill=True, color='#90ee90', lw=2, ec='black')
ax.add_patch(actuator_box)
ax.text(0.825, 0.5, 'Actuator\n\nDigital Control Signal\n↓\nPhysical Action', 
        ha='center', va='center', fontsize=11, fontweight='bold')

# Draw Arrows
ax.annotate('', xy=(0.4, 0.5), xytext=(0.3, 0.5), 
            arrowprops=dict(arrowstyle="->", lw=2, color='black'))
ax.text(0.35, 0.55, 'Data', ha='center', va='bottom', fontsize=9)

ax.annotate('', xy=(0.7, 0.5), xytext=(0.6, 0.5), 
            arrowprops=dict(arrowstyle="->", lw=2, color='black'))
ax.text(0.65, 0.55, 'Control', ha='center', va='bottom', fontsize=9)

# Save the figure
plt.tight_layout()
plt.savefig('sensor_actuator.png', dpi=300, bbox_inches='tight')
print("Saved sensor_actuator.png")
