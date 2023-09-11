import psutil
import os
import time

# Function to get CPU temperature (Raspberry Pi specific)
def get_cpu_temperature():
    try:
        res = os.popen("vcgencmd measure_temp").readline()
        temp = float(res.replace("temp=", "").replace("'C\n", ""))
        return temp
    except Exception as e:
        return None

# Function to get disk space usage
def get_disk_space():
    try:
        stat = os.statvfs("/")
        total_space = stat.f_frsize * stat.f_blocks
        free_space = stat.f_frsize * stat.f_bfree
        used_space = total_space - free_space
        return total_space, used_space
    except Exception as e:
        return None

while True:
    # CPU usage (per-core)
    cpu_usage_per_core = psutil.cpu_percent(interval=1, percpu=True)

    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    # Network utilization for eth0 (you can change the interface name if needed)
      network_interface = "eth0"

    # Read network interface speed from file
    with open(f'/sys/class/net/{network_interface}/speed') as speed_file:
        network_speed = int(speed_file.read().strip()) / 1000  # Convert to Mbps

    network_utilization = psutil.net_io_counters(pernic=True)[network_interface]
    sent_bytes = network_utilization.bytes_sent / (1024 * 1024)  # Convert to MB
    recv_bytes = network_utilization.bytes_recv / (1024 * 1024)  # Convert to MB

    # CPU temperature (Raspberry Pi specific)
    cpu_temperature = get_cpu_temperature()

    # Disk space usage
    total_space, used_space = get_disk_space()

    # Print live statistics
    os.system("clear")  # Clear the console for a cleaner display
    print("Per-Core CPU Usage:")
    for core, usage in enumerate(cpu_usage_per_core):
        print(f"Core {core}: {usage:.2f}%")
    print(f"Memory Usage: {memory_usage:.2f}%")
    print(f"Network Interface ({network_interface}) Speed: {network_speed:.2f} Mbps")
    print(f"Sent: {sent_bytes:.2f} MB | Received: {recv_bytes:.2f} MB")
    if cpu_temperature is not None:
        print(f"CPU Temperature: {cpu_temperature:.2f}°C")
    if total_space is not None:
        print(f"Total Disk Space: {total_space / (1024 * 1024 * 1024):.2f} GB")
        print(f"Used Disk Space: {used_space / (1024 * 1024 * 1024):.2f} GB")
    time.sleep(1)  # Wait for 1 second before refreshing
  
