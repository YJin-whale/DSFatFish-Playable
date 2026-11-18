# -*- coding: utf-8 -*-
"""Fetch real public-domain / CC-BY astronomical source images for star textures.

Run:
  python fetch_star_sources.py

Downloads into assets/tex/raw/star/:
  sdo_304.jpg / sdo_171.jpg   NASA SDO/AIA full-disk Sun (public domain, NASA)
  eht_sgra.jpg                EHT Sagittarius A* first image (CC BY 4.0, EHT Collaboration)
Files already present are skipped (delete to re-download).
"""
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = 'FatFishPlayable-asset-fetch/1.0 (educational game; contact: local)'

CANDIDATES = [
    # SDO/AIA latest full-disk images (NASA, public domain)
    ('sdo_304.jpg', 'https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg'),
    ('sdo_171.jpg', 'https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg'),
]


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(req, timeout=timeout, context=ctx).read()


def commons_file_info(title):
    """Return (url, extmetadata dict) for a Wikimedia Commons file title."""
    api = ('https://commons.wikimedia.org/w/api.php?action=query&format=json'
           '&prop=imageinfo&iiprop=url|extmetadata|size&titles=' + urllib.parse.quote(title))
    raw = get(api)
    data = json.loads(raw.decode('utf-8'))
    pages = data.get('query', {}).get('pages', {})
    for _, page in pages.items():
        ii = page.get('imageinfo')
        if ii:
            return ii[0]['url'], ii[0].get('extmetadata', {})
    return None, {}


def try_commons():
    """Locate the EHT Sgr A* image on Commons via search API, then fetch it."""
    api = ('https://commons.wikimedia.org/w/api.php?action=query&format=json'
           '&list=search&srnamespace=6&srlimit=12&srsearch=' +
           urllib.parse.quote('Sagittarius A* EHT'))
    try:
        data = json.loads(get(api).decode('utf-8'))
    except Exception as e:
        print('  commons search failed:', repr(e))
        return None
    hits = [h['title'] for h in data.get('query', {}).get('search', [])]
    print('  commons search hits:', hits)
    for title in hits:
        low = title.lower()
        if 'sagittarius' in low and 'a' in low:
            try:
                url, meta = commons_file_info(title)
            except Exception as e:
                print('  imageinfo failed for', title, repr(e))
                continue
            if not url:
                continue
            return title, url, meta
    return None


def main():
    os.makedirs(HERE, exist_ok=True)
    ok, fail = [], []

    for name, url in CANDIDATES:
        path = os.path.join(HERE, name)
        if os.path.isfile(path) and os.path.getsize(path) > 10000:
            print('skip (exists):', name)
            ok.append(name)
            continue
        try:
            data = get(url)
            if len(data) < 10000:
                raise ValueError('too small: %d bytes' % len(data))
            with open(path, 'wb') as f:
                f.write(data)
            print('OK', name, len(data), 'bytes <-', url)
            ok.append(name)
        except Exception as e:
            print('FAIL', name, repr(e))
            fail.append(name)

    # EHT Sgr A*
    eht_path = os.path.join(HERE, 'eht_sgra.jpg')
    if os.path.isfile(eht_path) and os.path.getsize(eht_path) > 10000:
        print('skip (exists): eht_sgra.jpg')
        ok.append('eht_sgra.jpg')
    else:
        found = try_commons()
        if found:
            title, url, meta = found
            try:
                data = get(url)
                with open(eht_path, 'wb') as f:
                    f.write(data)
                info = {
                    'commons_title': title,
                    'url': url,
                    'license': meta.get('LicenseShortName', {}).get('value', ''),
                    'artist': meta.get('Artist', {}).get('value', ''),
                    'credit': meta.get('Credit', {}).get('value', ''),
                    'description': meta.get('ImageDescription', {}).get('value', ''),
                }
                with open(os.path.join(HERE, 'eht_sgra_source.json'), 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                print('OK eht_sgra.jpg', len(data), 'bytes <-', url)
                print('  license:', info['license'])
                ok.append('eht_sgra.jpg')
            except Exception as e:
                print('FAIL eht_sgra.jpg download', repr(e))
                fail.append('eht_sgra.jpg')
        else:
            print('FAIL eht_sgra.jpg (not found on commons)')
            fail.append('eht_sgra.jpg')

    print('\nOK:', ok)
    print('FAIL:', fail)
    return 0


if __name__ == '__main__':
    sys.exit(main())
