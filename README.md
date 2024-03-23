# NordVPN WireGuard Configuration Generator

The NordVPN WireGuard Configuration Generator is a Python script designed to streamline the process of generating optimized WireGuard configuration files for NordVPN servers. By leveraging the NordVPN API and advanced algorithms, this tool enables users to effortlessly connect to the most suitable servers based on factors such as server load, proximity to the user's location, and server performance.

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Usage](#usage)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Configuring WireGuard for NordVPN can be a time-consuming and complex task, especially when considering the vast array of available servers. The NordVPN WireGuard Configuration Generator aims to simplify this process by automatically generating optimized configuration files tailored to the user's preferences and location. By utilizing intelligent algorithms and the NordVPN API, this tool ensures a seamless and efficient VPN setup experience.

## Key Features

- **Automated Server Sorting**: The script intelligently sorts NordVPN servers based on server load and proximity to the user's location, ensuring optimal performance and reliability.

- **Intuitive Server Organization**: Servers are categorized by country and city, providing a clear and structured view of NordVPN's extensive network.

- **Best Server Selection**: The script identifies and saves the best server configuration for each city in every country, allowing users to quickly connect to the most optimal servers.

- **Location-Based Optimization**: By considering the user's location, the script prioritizes servers that are geographically closer, minimizing latency and improving connection speed.

- **Server Load Balancing**: The script takes into account the current load of each server, ensuring that users are connected to the least congested servers for a smooth browsing experience.

- **Configuration File Management**: Generated configuration files are meticulously organized and saved by country and city, making it easy to locate and manage specific server configurations.

## Usage

To use the NordVPN WireGuard Configuration Generator, follow these steps:

1. Obtain your NordVPN access token from the NordVPN dashboard.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Run the `main.py` script and provide your access token when prompted.
5. The script will generate optimized WireGuard configuration files based on your location and save them in an organized directory structure.

```bash
python main.py
```

## Installation

To install the NordVPN WireGuard Configuration Generator, clone this repository to your local machine:

```bash
git clone https://github.com/mustafachyi/NordVPN-WireGuard-Config-Generator.git
```

## Dependencies

The NordVPN WireGuard Configuration Generator relies on the following Python libraries:

- `requests`: For making HTTP requests to the NordVPN API.
- `logging`: For logging script activities and errors.
- `subprocess`: For interacting with system commands.
- `concurrent.futures`: For parallel execution of tasks.

Ensure that these dependencies are installed before running the script.

## Contributing

Contributions to the NordVPN WireGuard Configuration Generator are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please open an issue or submit a pull request. We appreciate your contributions in making this tool better.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

We hope that the NordVPN WireGuard Configuration Generator simplifies your VPN setup process and enhances your overall NordVPN experience. If you have any questions or need further assistance, please don't hesitate to reach out.
