# macgputils

`macgputils` is a lightweight Python utility to fetch GPU statistics on macOS using the native `powermetrics` tool. It provides programmatic access to GPU power usage, frequency, active/idle time, and more.

## Features

- Read real-time GPU power consumption (in mW)
- Get GPU hardware active frequency
- Check GPU idle residency
- Sample multiple times to monitor changes over time
- Easy-to-use API: `macgputils.get_gpu_stats()`

## Installation

```bash
pip install macgputils
```

> If `powermetrics` is not already available, `macgputils` will prompt and help install it via Apple's developer tools.

## Usage

```python
import macgputils

# Get single sample
stats = macgputils.get_gpu_stats()
print(stats)

# Get multiple samples
for sample in macgputils.get_gpu_stats(samples=3):
    print(sample)
```

### Output Example

```python
{'Active Frequency': '389 MHz', 'HW Active Residency': '14.00%', 'Idle Residency': '86.00%', 'GPU Power': '33 mW'}
```

## API Reference

### `macgputils.get_gpu_stats(samples=1, interval=5)`

| Parameter | Description |
|----------|-------------|
| `samples` | Number of GPU usage samples to collect |
| `interval` | Time in seconds between each sample |

Returns:
- A dictionary if `samples=1`
- A list of dictionaries if `samples > 1`

---

## Requirements

- macOS
- Python 3.6+
- `powermetrics` (part of macOS; auto-installable via Xcode command line tools)

## License

MIT License

---

## Author

Developed by @aabhinavg1. Contributions are welcome — feel free to fork and submit pull requests!
