import requests
from requests import RequestException
import gzip, json, os
from apt import Cache


hi_url = 'https://udd.debian.org/how-can-i-help.json.gz'


def get_data(url):
    """ get the gz and store it to a temporary file"""
    try:
        req = requests.get(url, stream=True)
    except RequestException as e:
        print(e.reason)

    """ store the gz in a temorary file """
    with open('tmp/delete_me.gz', 'wb') as handle:
        for block in req.iter_content(1024):
            handle.write(block)

    """ extract the tmp gz to a list"""
    with gzip.open('tmp/delete_me.gz', 'r') as infile:
        for line in infile:
            data = json.loads(line.decode("utf-8"))
        #os.unlink('tmp/delete_me.gz')

    return data

def get_data_len(dict):
    return {key: len(value) for key, value in dict.items()}

def get_help_items():
    hi = get_data(hi_url)

    """ Get system installed packages  """
    cache = Cache()
    system_packages = []
    for pkg in cache:
        if cache[pkg.name].is_installed:
            system_packages.append(pkg.name)

    """ Filter the list of help items against the system installed packages list """
    hi_filtered = []
    for i in range(1, len(hi)):
        for key, value in hi[i].items():
            if key == "packages":
                for package in value:
                    if package in system_packages:
                        hi_filtered.append(hi[i])
            elif key == "package":
                if value in system_packages:
                    hi_filtered.append(hi[i])

    """ pripare data for render  """
    help_data = {
        "wnpp": [],
        "gift": [],
        "testing-autorm": [],
        "no-testing": [],
        "infra": [],
        "rfs": []
    }

    for item in hi_filtered:
        if item["type"] == "wnpp":
            # puts " - #{r['source']} - https://bugs.debian.org/#{r['wnppbug']} - #{wnpptype(r['wnpptype'])}"
            help_data["wnpp"].append(item)
        elif item["type"] == "gift":
            # puts " - #{r['package']} - https://bugs.debian.org/#{r['bug']} - #{r['title']}"
            help_data["gift"].append(item)
        elif item["type"] == "testing-autorm":
            puts
            help_data["testing-autorm"].append(item)
        elif item["type"] == "rfs":
            # puts " - #{r['source']} - https://bugs.debian.org/#{r['id']} - #{r['title']}"
            help_data["rfs"].append(item)
        elif item["type"] == "no-testing":
            # puts " - #{r['package']} - https://tracker.debian.org/pkg/#{r['id']}"
            help_data["no-testing"].append(item)
        elif item["type"] == "infra":
            help_data["infra"].append(item)

    return help_data
