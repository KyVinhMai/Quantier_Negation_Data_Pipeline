import requests
from stem import Signal
from stem.control import Controller

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
    return session

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="ManilaCebu15")
        controller.signal(Signal.NEWNYM)


if __name__ == "__main__":
    session = get_tor_session()
    print(session.get("http://httpbin.org/ip").text)

    print(requests.get("http://httpbin.org/ip").text)

    renew_connection()
    session = get_tor_session()
    print(session.get("http://httpbin.org/ip").text)