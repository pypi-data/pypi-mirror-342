import subprocess
import re

def get_gpu_stats(samples=1):
    try:
        output = subprocess.check_output([
            "sudo", "powermetrics", "--samplers", "gpu_power", f"-n{samples}"
        ], stderr=subprocess.DEVNULL).decode()

        samples_data = output.split("*** Sampled system activity")
        parsed_samples = []

        for sample in samples_data:
            if "**** GPU usage ****" not in sample:
                continue

            gpu_data = {}

            freq_match = re.search(r"GPU HW active frequency:\s+(\d+)\s+MHz", sample)
            if freq_match:
                gpu_data["Active Frequency"] = f"{freq_match.group(1)} MHz"

            residency_match = re.search(r"GPU HW active residency:\s+([\d\.]+%)", sample)
            if residency_match:
                gpu_data["HW Active Residency"] = residency_match.group(1)

            idle_match = re.search(r"GPU idle residency:\s+([\d\.]+%)", sample)
            if idle_match:
                gpu_data["Idle Residency"] = idle_match.group(1)

            power_match = re.search(r"GPU Power:\s+(\d+)\s+mW", sample)
            if power_match:
                gpu_data["GPU Power"] = f"{power_match.group(1)} mW"

            parsed_samples.append(gpu_data)

        return parsed_samples

    except Exception as e:
        return [{"Error": str(e)}]
