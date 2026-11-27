import json
import re

# Load v2 dataset
with open('data_centres_india_v2.json', 'r', encoding='utf-8') as f:
    v2_data = json.load(f)

# Tracker domains that must strictly be [T]
TRACKER_DOMAINS = [
    'peeringdb.com', 'datacentermap.com', 'baxtel.com', 
    'datacenters.com', 'wikipedia.org', 'globaldcwiki.com'
]

# Primary domains
PRIMARY_DOMAINS = [
    'yotta.com', 'princetondg.com', 'services.global.ntt', 'ctrls.com',
    'adaniconnex.com', 'adani.com', 'sttgdc.in', 'sttgdc.com', 'sttelemediagdc.in',
    'digitalconnexion.com', 'sifytechnologies.com', 'coltdatacentres.net',
    'capitaland.com', 'equinix.com', 'nxtra.in', 'webwerks.in',
    'ironmountain.com', 'ril.com', 'news.microsoft.com', 'aws.amazon.com',
    'press.aboutamazon.com', 'tcs.com', 'larsentoubro.com',
    'environmentclearance.nic.in', 'investodisha.gov.in', 'ap.gov.in',
    'wbidc.com', 'bseindia.com', 'nseindia.com', 'tiaonline.org', 'uptimeinstitute.com'
]

# Secondary domains
SECONDARY_DOMAINS = [
    'datacenterdynamics.com', 'w.media', 'thehindu.com', 'economictimes.indiatimes.com',
    'business-standard.com', 'livemint.com', 'reuters.com', 'newindianexpress.com',
    'businessworld.in', 'indiatimes.com', 'odishatv.in', 'aninews.in',
    'thenewsminute.com', 'deccanchronicle.com', 'mingtiandi.com', 'cushmanwakefield.com',
    'jll.co.in', 'cbre.co.in', 'colliers.com', 'businesstoday.in', 'entrepreneur.com',
    'tradebrains.in', 'biltraxmedia.com'
]

print("Script template ready.")
