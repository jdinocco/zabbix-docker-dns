# zabbix-docker-dns

## Running Docker

```
docker-compose up -d
```

## Usage
### Discover DNS Servers for Zabbix LLD
```
curl http://localhost:5000/dns_servers
```

Result
```
{
  "data": [
    {
      "{#DNS_SERVER}": "8.8.4.4"
    },
    {
      "{#DNS_SERVER}": "1.1.1.1"
    },
    {
      "{#DNS_SERVER}": "8.8.8.8"
    }
  ]
}
```

### DNS Query Time
```
curl -s "http://localhost:5000/dns_test?server=8.8.8.8&url=cisco.com"
```

Result
```
[
  {
    "answer": [
      {
        "class": "IN",
        "data": "72.163.4.185",
        "name": "cisco.com.",
        "ttl": 1391,
        "type": "A"
      }
    ],
    "query_time": 0,
    "rcvd": 54,
    "server": "8.8.8.8#53(8.8.8.8) (UDP)",
    "when": "Tue Feb 20 16:53:12 -03 2024",
    "when_epoch": 1708458792,
    "when_epoch_utc": null
  }
]
```

## Additional Notes
The container is only bind to the localhost where is running, the Zabbix agent o Proxy must be install and running on the host.
