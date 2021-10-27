import os
from pprint import pprint

import requests

ZONE = os.getenv("ZONE", "mortdogged.com")
DNS_RECORD = os.getenv("DNS_RECORD", "api.mortdogged.com")
AUTH = os.getenv("AUTH")

BASE_URL = "https://api.cloudflare.com/client/v4"


# try python3.5 syntax for raspberry
def main():
    ip = get_ip()
    print("Current IP is {}".format(ip))

    zone_id = get_zone_id(ZONE, AUTH)
    print("Zoneid for {} is {}".format(ZONE, zone_id))

    dns_record_id = get_dns_record_id(zone_id, DNS_RECORD, AUTH)
    print("DNSrecordid for {} is {}".format(DNS_RECORD, dns_record_id))

    result = update_dns_record(ip, zone_id, dns_record_id, DNS_RECORD, AUTH)
    pprint(result)


def get_ip():
    return requests.get("https://checkip.amazonaws.com").text.strip()


def get_zone_id(zone, auth):
    return requests.get(
        "{}/zones?name={}&status=active".format(BASE_URL, zone),
        headers={"Authorization": auth},
    ).json()["result"][0]["id"]


def get_dns_record_id(zone_id, dns_record, auth):
    return requests.get(
        "{}/zones/{}/dns_records?type=A&name={}".format(BASE_URL, zone_id, dns_record),
        headers={"Authorization": auth},
    ).json()["result"][0]["id"]


def update_dns_record(ip, zone_id, dns_record_id, dns_record, auth):
    return requests.put(
        "{}/zones/{}/dns_records/{}".format(BASE_URL, zone_id, dns_record_id),
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
