import os, requests, logging, subprocess, json, time
from concurrent.futures import ThreadPoolExecutor
from math import radians, cos, sin, asin, sqrt
from operator import itemgetter

logging.basicConfig(level=logging.INFO)

def get_key(token):
    try:
        return json.loads(subprocess.check_output(["curl", "-s", "-u", f"token:{token}", "https://api.nordvpn.com/v1/users/services/credentials"]).decode('utf-8')).get('nordlynx_private_key')
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

def get_servers():
    try:
        return requests.get("https://api.nordvpn.com/v1/servers?limit=7000&filters[servers_technologies][identifier]=wireguard_udp").json()
    except Exception as err:
        logging.error(f'Error occurred: {err}')
        raise

def find_key(server):
    for tech in server['technologies']:
        if tech['identifier'] == 'wireguard_udp':
            for data in tech.get('metadata', []):
                if data.get('name') == 'public_key':
                    return data.get('value')

def format_name(name):
    return name.replace(' ', '_')

def generate_config(key, server):
    public_key = find_key(server)
    if public_key:
        country_name = format_name(server['locations'][0]['country']['name'])
        city_name = format_name(server['locations'][0]['country'].get('city', {}).get('name', 'Unknown'))
        server_name = format_name(f"{server['name'].replace('#', '')}_{city_name}")
        config = f"""
[Interface]
PrivateKey = {key}
Address = 10.5.0.2/16
DNS = 103.86.96.100

[Peer]
PublicKey = {public_key}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = {server['station']}:51820
PersistentKeepalive = 25
"""
        return country_name, city_name, server_name, config
    else:
        logging.info(f"No WireGuard public key found for {server['name']} in {server.get('city', {}).get('name', 'Unknown')}. Skipping.")

def save_config(key, server, path=None):
    try:
        if 'locations' in server:
            country_folder, city_folder, server_name, config = generate_config(key, server)
            if config:
                if path is None:
                    country_path = os.path.join('configs', country_folder)
                    os.makedirs(country_path, exist_ok=True)
                    city_path = os.path.join(country_path, city_folder)
                    os.makedirs(city_path, exist_ok=True)
                    filename = f"{server_name}.conf"
                    path = os.path.join(city_path, filename)
                with open(path, "w") as f:
                    f.write(config)
                    logging.info(f"WireGuard configuration for {server_name} saved to {path}")
                return path
    except Exception as e:
        logging.error(f"Error occurred while saving config: {e}")

def calculate_distance(ulat, ulon, slat, slon):
    ulon, ulat, slon, slat = map(radians, [ulon, ulat, slon, slat])
    dlon = slon - ulon
    dlat = slat - ulat
    a = sin(dlat/2)**2 + cos(ulat) * cos(slat) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * 6371

def sort_servers(servers, ulat, ulon):
    for server in servers:
        slat = server['locations'][0]['latitude']
        slon = server['locations'][0]['longitude']
        server['distance'] = calculate_distance(ulat, ulon, slat, slon)
    return sorted(servers, key=lambda k: (k['load'], k['distance']))

def get_location():
    try:
        location = requests.get('https://ipinfo.io/json').json()['loc'].split(',')
        return float(location[0]), float(location[1])
    except Exception as err:
        logging.error(f'Error occurred: {err}')
        raise

def main():
    token = input("Enter your access token: ")
    key = get_key(token)
    start_time = time.time()
    if key:
        servers = get_servers()
        if servers:
            ulat, ulon = get_location()
            sorted_servers = sort_servers(servers, ulat, ulon)
            with ThreadPoolExecutor() as executor:
                paths = list(set(executor.map(save_config, [key]*len(sorted_servers), sorted_servers)))
                paths = [path for path in paths if path is not None]

            servers_by_location = {}
            for server in sorted_servers:
                country = server['locations'][0]['country']['name']
                city = server['locations'][0]['country']['city']['name']
                if country not in servers_by_location:
                    servers_by_location[country] = {}
                if city not in servers_by_location[country]:
                    servers_by_location[country][city] = {"distance": int(server['distance']), "servers": []}
                server_info = (server['name'], f"load: {server['load']}")
                servers_by_location[country][city]["servers"].append(server_info)

            for country in servers_by_location:
                for city in servers_by_location[country]:
                    servers_by_location[country][city]["servers"].sort(key=itemgetter(1))

            if not os.path.exists('best_configs'):
                os.makedirs('best_configs')
            for country, cities in servers_by_location.items():
                safe_country_name = country.replace(' ', '_')
                for city, data in cities.items():
                    best_server = data["servers"][0]
                    best_server_info = next(server for server in servers if server['name'] == best_server[0])
                    safe_city_name = city.replace(' ', '_')
                    save_config(key, best_server_info, os.path.join('best_configs', f'{safe_country_name}_{safe_city_name}.conf'))

            servers_by_location = dict(sorted(servers_by_location.items()))

            with open('servers.json', 'w') as f:
                f.write('{\n')
                last_country_index = len(servers_by_location) - 1
                for index, (country, cities) in enumerate(servers_by_location.items()):
                    f.write(f'  "{country}": {{\n')
                    last_city_index = len(cities) - 1
                    for city_index, (city, data) in enumerate(cities.items()):
                        f.write(f'    "{city}": {{\n')
                        f.write(f'      "distance": {data["distance"]},\n')
                        f.write(f'      "servers": [\n')
                        last_server_index = len(data["servers"]) - 1
                        for server_index, server in enumerate(data["servers"]):
                            f.write(f'        ["{server[0]}", {server[1]}]')
                            if server_index < last_server_index:
                                f.write(',\n')
                            else:
                                f.write('\n')
                        f.write(f'      ]\n')
                        f.write(f'    }}')
                        if city_index < last_city_index:
                            f.write(',\n')
                        else:
                            f.write('\n')
                    f.write(f'  }}')
                    if index < last_country_index:
                        f.write(',\n')
                    else:
                        f.write('\n')
                f.write('}\n')

        else:
            print("Failed to retrieve server information.")
    else:
        print("Failed to retrieve Nordlynx Private Key.")
    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Process completed in {elapsed_time} seconds")

if __name__ == "__main__":
    main()
