#!/usr/bin/python3
import sys
import urllib.request
import xml.etree.ElementTree as ET

def_ns = {
    'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
}


def get_urls_from_sitemap(sitemap_path, ns):
    file = urllib.request.urlopen(sitemap_path)
    xml = ET.fromstring(file.read())
    file.close()
    urls_list = xml.findall("xmlns:url/xmlns:loc", ns)
    if len(urls_list) < 1:
        return None
    output_urls = []
    for url in urls_list:
        output_urls.append(url.text)
    return output_urls


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must specify the parameters')
        exit()
    sitemap_file = sys.argv[1]
    urls = get_urls_from_sitemap(sitemap_file, def_ns)
    if urls is None:
        print('Sitemap is empty')
        exit()
    for url in urls:
        print(url)
