import os
from pprint import pprint

import requests

ZONE = os.getenv("ZONE", "mortdogged.com")
DNS_RECORD = os.getenv("DNS_RECORD", "api.mortdogged.com")
AUTH = os.getenv("AUTH")

BASE_URL = "https://api.cloudflare.com/client/v4"


def main():
    ip = get_ip()
    print(f"Current IP is {ip}")

    zone_id = get_zone_id(ZONE, AUTH)
    print(f"Zoneid for {ZONE} is {zone_id}")

    dns_record_id = get_dns_record_id(zone_id, DNS_RECORD, AUTH)
    print(f"DNSrecordid for {DNS_RECORD} is {dns_record_id}")

    result = update_dns_record(ip, zone_id, dns_record_id, DNS_RECORD, AUTH)
    pprint(result)


def get_ip():
    return requests.get("https://checkip.amazonaws.com").text.strip()


def get_zone_id(zone, auth):
    return requests.get(
        f"{BASE_URL}/zones?name={zone}&status=active",
        headers={"Authorization": auth},
    ).json()["result"][0]["id"]


def get_dns_record_id(zone_id, dns_record, auth):
    return requests.get(
        f"{BASE_URL}/zones/{zone_id}/dns_records?" f"type=A&name={dns_record}",
        headers={"Authorization": auth},
    ).json()["result"][0]["id"]


def update_dns_record(ip, zone_id, dns_record_id, dns_record, auth):
    return requests.put(
        f"{BASE_URL}/zones/{zone_id}/dns_records/{dns_record_id}",
        headers={"Authorization": auth},
        json={
            "type": "A",
            "name": dns_record,
            "content": ip,
            "ttl": 1,
            "proxied": True,
        },
    ).json()


if __name__ == "__main__":
    main()
