#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os
import sys
import json
import logging

import requests
from django.core.management.base import BaseCommand

from snisi_core.models.Entities import Entity
from snisi_tools.sms import to_ascii

logger = logging.getLogger(__name__)

DHIS_URL = "https://mali.dhis2.org/dhis/api"
OU_URL = "/".join([DHIS_URL, "organisationUnits"])
MALI_DHIS_IS = "cKcuEmNzNF2"
try:
    u, p = os.environ['DHIS_AUTH'].split(":")
    DHIS_AUTH = (u, p)
except:
    logger.error("Error! Missing DHIS_AUTH (username:password) environ")
    sys.exit(1)
DHIS_CACHE = "dhis-cache"


def download_ou(ouId):
    url = "/".join([OU_URL, ouId])
    req = requests.get(url, auth=DHIS_AUTH)
    return req.json()


def retrieve_ou(ouId):
    fpath = os.path.join(DHIS_CACHE, "{}.json".format(ouId))
    # cache exists
    if os.path.exists(fpath):
        with open(fpath, 'r') as fp:
            return json.load(fp)
    # cache dont exist ; downloading
    jsd = download_ou(ouId)
    # write cache
    with open(fpath, 'w') as fp:
        json.dump(jsd, fp, indent=4)
    return jsd


def get_ou(ouId):
    jsd = retrieve_ou(ouId)
    return {"id": jsd.get("id"),
            "name": jsd.get("name"),
            "children": [c['id'] for c in jsd.get("children")]}


def norm(name):
    return to_ascii(name).strip().upper()


skip_ids = [
    'i0eHXErts7M',  # Taoudenit (RS) TODO
    'znoHlSTEiRW',  # Menaka (RS) TODO
    'gNa9tYxEh0u',  # Hopital de Kati
    'HTHC9LATu4u',  # Hopital de Sikasso
    'zH9fsIFBRpF',  # INRSP
    'ZPbkqXmex0C',  # Hopital Luxembourg ME
    'YYkGlPo1BYY',  # Hopital Gabriel Toure
    'XvPbAOeSZ0x',  # CNAM
    'SMtASCD8FpE',  # Laboratoire SEREFO
    'NLTFpKoK4d3',  # Laboratoire CICM
    'xcHYXfYi6Sw',  # Hopital Point G
    'mW8NixhED5c',  # IOTA
    'GOBjET424k8',  # CHU-CNOS
    'sWhh3BXrJb3',  # Hopital du Mali
    'uBVGK85vC9m',  # Hopital de Tombouctou
    'onZE5IlCOF0',  # Hopital de Segou
    'zNJiUxxh1jd',  # Hopital de Mopti
    'ygZh4kv9EaK',  # Hopital de Kayes
    'hfCE13oqU2S',  # Hopital de Gao

    'DU2hay1pcn7',  # Dépôt de Kalabancoro
    'qXJS85t5D32',  # Dépôt de Ouelessebougou
    'UNlDENm4Gv1',  # Dépôt de Fana
    'fwsJ9xzTqmu',  # Dépôt de Nara
    'GOJRGfHODIu',  # Dépôt de Kati
    'AC8FIu8WKFj',  # Dépôt de Kangaba
    'jpuFMcbM8KL',  # Dépôt de Banamba
    'sRnyvmAzLxF',  # Dépôt de Kolokani
    'f7psDrRwDTC',  # Dépôt de Koulikoro
    'szBVsZIjJoV',  # Dépôt de Dioila
    'a66IjTRoD1C',  # Dépôt de Kolondieba
    'FI1ZBIs7Mxj',  # Dépôt de Yanfolila
    'd0BXhQZ0FPQ',  # Dépôt de Niena
    'cICx86UuBw4',  # Dépôt de Bougouni
    'P4w263Panp2',  # Dépôt de Koutiala
    'TVTb6aZdq4H',  # Dépôt de Selingué
    'LgTEz7kiXST',  # Dépôt de Kadiolo
    'hGWVMIcLP0O',  # Dépôt de Kignan
    'ik0jI5Dm9AD',  # Dépôt de Sikasso
    'CG8XS0gYZa8',  # Dépôt de Yorosso
    'CPisqiNDl4N',  # Dépôt de Boukanem
    'BpHeTwsdh3e',  # PPM Korofina
    'ewux2U4TNzr',  # Pmi Niarela
    'fHQ1bHKVWkN',  # Magasin PPM Darsalam
    'SFVOxxJ77Uh',  # Magasin de Daoudabougou
    'RCqHCg0WPLk',  # Dépôt de Niono
    'JmH5upvikw4',  # Dépôt de San
    'bR3F4hGp96U',  # Dépôt de Markala
    'HtJqj7LnDr4',  # Dépôt de Tominian
    'tYMxAJMcuex',  # Dépôt de Macina
    'XwAEo0MobeC',  # Dépôt de Bla
    'JcPfc9UhMwa',  # Dépôt de Baraoueli
    'zSMheEYmoev',  # Dépôt de Segou
    'F9kLSMKYA7T',  # Dépôt de Tenenkou
    'gwukxXTrHci',  # Dépôt de Douentza
    'GzoFuWYtd4t',  # Dépôt de Djenné
    'vRf6niMeeog',  # Dépôt de Bandiagara
    'WoIFjJ1mYCv',  # Dépôt de Youwarou
    'VA9mhkKTmZS',  # Dépôt de Koro
    'GAadn8DkU6p',  # Dépôt de Bankass
    'tOVTEwvoapw',  # Dépôt de Mopti
    'BKqhlOUmJtc',  # Dépôt de Yélimané
    'TarXdnO1wdW',  # Dépôt de Nioro
    'DtmJB45pF6F',  # Dépôt de Oussibidiagna
    'JmELI4ZmNRc',  # Dépôt de Kita
    'ZpneSfijaBM',  # Dépôt Bafoulabé
    'RgQgrfq5Vya',  # Dépôt de Kayes
    'wdrZgV7topq',  # Dépôt de Kéniéba
    'kdwQSlFHjb0',  # Dépôt de Diéma


    # ZZZ
    'eRjImgzfcxV',  # ZZZ Faraba
    'i7B6NvBkM9L',  # Toukoro cscom non fonctionnel à supprimer
    'BRB9WrS0JUj',  # aire non fonctionnelle à supprimer N'Gabakoro
    'L5j50naBWTf',  # ZZZGuinso
    'aO7jMSSANol',  # ZZZTieguekourouni
    'YeaGUdWiCXl',  # ZZZMissirikoro
    'C7BhY0gkZ0g',  # ZZZSokourani-Missirikoro
    'xtJszl40GDV',  # ZZZMadinacoun
    'WuKu1KjXph8',  # ZZZKabalé
    'A1tfMbowBTT',  # A supprimer Dioulabougou - Niafunke
    'OllYwcy6EdV',  # A supprimer zzz Nampalari(Equipe M1)
    'TeAS6WUYGWG',  # ZZZ Nara
    'rAt46RLUuQ5',  # ZZZ Crsef Bla  à supprimer
    'Tgmnp89sc5g',  # ZZZ Mambri
    'HtMbNKMUJhR',  # ZZZ Kollé
    'DYcosKzLls3',  # ZZZ Segouna
    'dF8xoU0KE2p',  # ZZZ Baléa
    'd5Y3d4zpEWk',  # ZZZ à supprimer Bourem Foghass
    'Iz7HFiy33Ar',  # ZZZ à supprimer Amalaw-Law

    'jXclN52FA7u',  # TinEssako (DS - TOMB) TODO
    'mgxuQzMTgyp',  # Sefeto (DS - KAY) TODO
    'IFEHV5B8qPc',  # Sagabari (DS - KAY) TODO
    'Z4N53EblD4C',  # Mana (HA - Ouelessebougou) TODO
    'kJMIspyiQoG',  # Kafara (HA - Ouelessebougou) TODO
    'JCGJ4q3KlnB',  # Korokoro (HA - Fana) TODO
    'ypqM6owUS8b',  # Ouezzindou (HA - Kati) TODO
    'PcLJsZt6G6A',  # Djiguidala (HA - Kati) TODO
    'yjH2vJwqmez',  # Niamé (HA - Kati) TODO
    'qk6gGhDqosk',  # Dio Ba (HA - Kati) TODO
    'vHKTw7tjW6T',  # Koflatie (HA - Kangaba) TODO
    'QPPzKktjUjD',  # Faraba (HA - Kangaba) TODO || FARABA (ZJW25) Selingue??
    'KnzlZo9XCZO',  # Samaya (HA - Kangaba) TODO
    'wWpYxruNXlA',  # Baoufoulala (HA - Dioila) TODO
    'k8bDiC2YtMj',  # Dialakoroba (HA - Kolondieba) TODO
    'I2BgQPqDMFr',  # Fala II (HA - Kolondieba) TODO
    'Gbxb6NTY3GX',  # Beco (HA - Bougouni) TODO
    'uKfiKsVUvsz',  # Léléni (HA - Koutiala) TODO || LOULOUNI (Z3FB3) Kadiolo?
    'hTjBnRvsaEj',  # Madinakoun (HA - Selingue) TODO
    'WzGmp7eOXAU',  # Tieguecourouni (HA - Selingue) TODO
    'p3lesZ8YgBp',  # Solenkoro (HA - Selingue) TODO
    'QCfRzO8Tmp0',  # Diarani (HA - Selingue) TODO
    'IUFjWY6fKLg',  # Sanankoroba (HA - Selingue)
    'MTIfhx73VJx',  # Gouènè (HA - Kadiolo)
    'Npx9X5LpGpn',  # N'Golona (HA - Kadiolo)
    'mBtH57mAmRB',  # Fanidiama (HA - Kadiolo)
    'P1AC2NRtvjI',  # Torokoro (HA - Kadiolo)
    'zx9JGtmKAfn',  # N'goko (HA - Kadiolo)
    'zYl7wRVForu',  # Borogoba (HA - Kadiolo)
    'Pl8egMWC0kV',  # Hérémakono (HA - Sikasso)
    'ZCSc3fAzeFY',  # Banankoda (HA - Sikasso)
    'GGV99sDSY73',  # Tendio (HA - Yorosso)
    'vsiFFmbJhqB',  # Sanwa (HA - Yorosso)
    'NgJxmkCQpKz',  # N'Gorola (HA - Yorosso)
    'OjbXEpTAAvR',  # Alwalidji (HA - Diré)
    'PtJwF7xLCqc',  # Ebanguemalène (HA - Gourma-rharous)
    'HoOJfsKiXWW',  # Gareye (HA - Gourma-rharous)
    'mZla9EZeZLM',  # Dimamou (HA - Gourma-rharous)
    'uFasylmYYK2',  # Ouinerden (HA - Gourma-rharous)
    'wKdsYixsbid',  # Tatakarat (HA - Gourma-rharous)
    'Nl4Ve70qZ5f',  # Adiora (HA - Gourma-rharous)
    'M7jqEWGMpjD',  # Arsy Bella (HA - Gourma-rharous)
    'iegSHw6qzz8',  # Rharous (HA - Gourma-rharous)
    'OIOhkG3jJ5Q',  # Teberent (HA - Gourma-rharous)
    'EZKZ48zUl6n',  # Bougbéa (HA - Tombouctou)
    'TsCeTbk7cp1',  # M'Babou (HA - Tombouctou)
    'xdgYo1UH1fm',  # Oudeyka (HA - Tombouctou)
    'J8xXi9lA9U4',  # Dar Salam (HA - Tombouctou)
    'd5VtvRAt0xF',  # Gourou (HA - Tombouctou)
    'fSU0HhEbfFq',  # Beregoungou (HA - Tombouctou)
    'OxOz0ghjkw7',  # Nipkit Zriba (HA - Tombouctou)
    'tiB3ucqez5Z',  # Arnassaye (HA - Tombouctou)
    'TxGxeCRxWjd',  # Atoual (HA - Tombouctou)
    'SzY5csTnNMZ',  # Nibkitt El Iik (HA - Tombouctou)
    'OT5p0Oxfuxx',  # Doya (HA - Tombouctou)
    'K0s38trWboP',  # Kessoubiby (HA - Goundam)
    'UQeBPFKIIrr',  # Affernane (HA - Goundam)
    'rJfQZ9mICyT',  # Tondigame (HA - Goundam)
    'u1PNgJDT3H3',  # Yourmi (HA - Goundam)
    'wrX9eWtzcEy',  # Tamaskoye (HA - Goundam)
    'oLphnX86bpA',  # Aljounoub (HA - Goundam)
    'KhWBVz7UTY9',  # Zouéra (HA - Goundam)
    'svQxImenJT7',  # Fatakara (HA - Goundam)
    'bNspIWC50yu',  # Atta (HA - Goundam)
    'KOaP7htXkpp',  # Hangabera (HA - Goundam)
    'tdg0atdvb2N',  # Ibrika1 (HA - Goundam)
    'WoX9S15Qx4Z',  # Ediar (HA - Goundam)
    'hV1Z9q0nk88',  # Kessoukoreye (HA - Goundam)
    'OYgL48NYahy',  # Niambourgou (HA - Goundam)
    'UsGG4mfCChX',  # Aratène (HA - Goundam)
    'cBSYAMhAPfk',  # Hel Acheik (HA - Goundam)
    'L2pVkTZckUI',  # Kaneye (HA - Goundam)
    'HyPX5huhgEb',  # Toulabele (HA - Niafunké)
    'bAE5CuRbNM8',  # Namatié (HA - Niafunké)
    'kgLFcXzVHI7',  # Tondidarou (HA - Niafunké)
    'vTgj3d48sTG',  # Dari (HA - Niafunké)
    'RASFx5deEcY',  # Boudoubadi (HA - Niafunké)
    'ZVCObGTMmD4',  # Niafunke Central (HA - Niafunké)
    'hqZinLe5NIr',  # Tingora (HA - Niafunké)
    'efv6DFAJwRt',  # Kourou Bambara (HA - Niafunké)
    'pFu5kjcprJk',  # Waki (HA - Niafunké)
    'Mz2qhXgly5j',  # Telabit (HA - Tessalit)
    'WIHyUhNCxDR',  # Inhalid (HA - Tessalit)
    'ZAbOU8QDJIF',  # Boghassa (HA - Abeibara)
    'eBOPoBfhFxb',  # Tinzaouatene (HA - Abeibara)
    'oc8fA34FUcy',  # Intadeinit (HA - Kidal)
    'aJAiXIQ0wKs',  # Intibzaz (HA - Kidal)
    'Eq5PxdDIIsq',  # Tanainait (HA - Kidal)
    'PtF8mljE5Qb',  # Tassik (HA - Kidal)
    'O1imSUoJ9XO',  # Mamari Sibiri (HA - Niono)
    'xb0y4fV1blq',  # Fassoun (Ibatou) (HA - Niono)
    'UW7wowHJnQF',  # Thiadjol (HA - Niono)
    'HV8ZlDEIgoL',  # Siengo extension (HA - Niono)
    'GK7h0nPqDEA',  # Farakala (HA - Bla)
    'QvL6cbhKRxl',  # Tassona (HA - Bla)
    'pufA5MpHSvx',  # Soignebougou (HA - Segou)
    'OtPeVpFCdME',  # Hamdallaye  Sido (HA - Segou)
    'sqOgux6YquB',  # Pelegana Nord (HA - Segou)
    'fmwUHbTVSZe',  # Bougoufie Alamissa (HA - Segou)
    'JrisYA2rKSc',  # Gueni (HA - Segou)
    'xo09VA42cGN',  # Kita (HA - Tenenkou)
    'ozrJkjBaQzb',  # Petaka (HA - Douentza)
    'Sa6bVHe3j2y',  # Bourgouma (HA - Bandiagara)
    'JGgUrECRQGY',  # Kassa-Saou (HA - Koro)
    'JAxJISuplmU',  # Salsalbé (HA - Mopti)
    'Uoo46o9T1jg',  # Ngorodia (HA - Mopti)
    'C6SsFgYpmRX',  # Moupa (HA - Mopti)
    'AG7NhqIfsgC',  # Manako (HA - Mopti)
    'MDJogScevbf',  # Kotaka (HA - Mopti)
    'Vpb3VkjLMLY',  # Doko (HA - Mopti)
    'yL7Yu3jJpu7',  # Saraféré (HA - Mopti)
    'quxkhmKF0BA',  # Korampo (HA - Yelimane)
    'FCjBLM2PaVD',  # Komeoulou (HA - Yelimane)
    'HkPPCpCvxsA',  # Madina (HA - Kita)
    'aoJCdk1Z4Qp',  # Souranzan (HA - Kita)
    'iGz2wvuCiDm',  # Sibikily (HA - Kita)
    'xioqelbRN5x',  # Bankassi_Kita (HA - Kita)
    'WoV965mbJFO',  # Namala (HA _ Kita)
    'RcmXOeHKypy',  # Batimakana (HA - Kita)
    'kc2LxSHjkrD',  # Kouloun (HA - Kayes)
    'V6eiqzaODHh',  # Gounka (HA - Kayes)
    'ubH9cQGtiEI',  # Kalinioro (HA - Kayes)
    'JTxUVrs9woW',  # Sourangnédou (HA - Diema)
    'CHspNRWlxBs',  # Iminaguel (HA - Gao)
    'Qi7vbTKW4gn',  # Imenass (HA - Gao)
    'cbqoKy2m1Sp',  # Dorey (HA - Gao)
    'Hx9ogXb87Y2',  # Camp Firhoun (HA - Gao)
    'uBmiVqD3SAK',  # Doro (HA - Gao)
    'UpVeLv5zD0e',  # Bagoundje (HA - Gao)
    'YTTkMtH5kON',  # Gaina (HA - Gao)
    'S0piU7DdbaI',  # Gangano (HA - Bourem)
    'JuSlk4ABxIP',  # Hamankoira (HA - Bourem)
    'IOAwDXmGwUT',  # Hawa (HA - Bourem)
    'CgmYJqJrVdO',  # Fafa (HA - Ansongo)
    'dmjPeOVYJRq',  # Ansongo Central (HA - Ansongo)

]

custom_mapping = {
    'ddCBqPCb838': 'X922',  # Kalabancoro: KALABAN KORO
    'HLMyBv2ayJz': 'R279',  # Commune I: Commune1
    'RfbBHfPwL2y': 'HG51',  # Commune II: Commune2
    'HkdWN8JPsw5': 'GA67',  # Commune III: Commune3
    'PPlCb8soCGw': '7GK0',  # Commune IV: Commune4
    'GV6VqawGt5X': 'XRY9',  # Commune V: Commune5
    'FEW7Xo3AmMr': '5SS7',  # Commune VI: Commune6
    'pq9bZ5x438C': 'XN90',  # Baroueli: BARAOUELI
    'cZNXJ7srOVD': 'MKX2',  # Oussoubidiagna: OUSSOUBIDJANGNA

    'aPXxP8AstM0': 'Z4K70',  # Kalabancro Heremakono: KALABANCORO HERAMAKONO
    'LduQSNnuo6P': 'Z2PH2',  # Sirakoro Meguetana: SIRACORO-MEGUETANA
    'PUaeK9vW0fl': 'ZA620',  # Sanancoroba: SANANKOROBA
    'mqmWzISDo6b': 'ZNZC8',  # Kalabancoro: KALABAN-CORO
    'dOs9DVNiHzC': 'ZY862',  # N'Gouraba: NGOURABA
    'Jogh9zEzAv2': 'Z6Z26',  # Kalabancoro S Extension: KALABANCORO SUD EXTENSION
    'gPyny8gF8NG': 'ZF6F5',  # N'Tabacoro Att Bougou: ATT BOUGOU TABACORO
    'df6EWOMpZMi': 'ZHAH3',  # Faraba: FARABA-KATI
    'lXuIFGfmwWK': 'Z86R5',  # Safé-Bougoula: SAFE BOUGOULA
    'ovgvRPDtnms': 'ZX7G0',  # Tiaka Dialakoro: TIAKADOUGOU DIALACORO
    'rZU9Ow5JioJ': 'ZHFF8',  # Sanankorodjitoumou: SANANKORO-DJITOUMOU
    'uoQ3cXYXc7D': 'ZEPM8',  # Ouélessébougou: ASACOOUEL (OUELESSEBOUGOU CENTRAL)
    'kdn1Mvrc5fO': 'ZSY70',  # Beleco: BELEKO SOBA
    'Ke2T9CCvDo6': 'ZTXB9',  # Diele: DJELE
    'yzqYnxlA5eP': 'ZAD65',  # Markacoungo: MARCACOUNGO
    'pmumoWSY8pw': 'ZNKS0',  # Bougoukourala: BOUGOUCOURALA
    'JdtY3QWy58p': 'ZTJ65',  # Fana: FANA CENTRAL
    'CNZQFj1FBX4': 'ZAMC3',  # Mena: MENA-FANA
    'ZqxwocPyfR1': 'Z3G84',  # Alasso: ALLASSO
    'UGhYwd9Q7s4': 'Z6PZ8',  # Boudjiguire: BOUDJIGIRE
    'bUaUfQAlDAu': 'Z2XR2',  # Bineou-Niakate: BINEOU NIAKATE
    'tdTWRdbk9ee': 'ZDB37',  # N'Gai: NGAI
    'msbm16cLhKk': 'ZWWC9',  # Nioumamakana: NIOUMA MAKANA
    'SHhuBzf86ev': 'ZXBF9',  # Kati Coro: KATI-CORO
    'UvYNqy5cRcU': 'ZAAX1',  # Ngabakoro Droit: NGABACORO
    'E6DaFF5yQt2': 'Z4R83',  # Kati Koko: KATI COCO
    'bAeLdu3hwBZ': 'ZA4W4',  # Dialacorodji: DIALAKORODJI
    'xCaNny2P1od': 'ZDH60',  # Soninkegny: SONIKEGNY
    'v2V7MooMMwg': 'ZJCH1',  # Figuira Tomo: FIGUIRATOMO
    'MQo5DNDbPQF': 'ZBH22',  # Manicoura: MANINCOURA
    'URqrDYHlje3': 'ZS2B7',  # H.Kéniéba: KENIEBA-KANGABA
    'kzCYtUS37DB': 'Z7MA6',  # Banamba  Ouest: ASACO BAO (CSCOM BANAMBA OUEST)
    'kqdhIIY0aHF': 'ZA530',  # Ouleni: OULENY
    'FAdXweLlx2m': 'ZSXK7',  # Dampha: DAMPHA DIARISSO
    'SvDQHkKtGzy': 'ZS794',  # Banamba  Central: BANAMBA CENTRAL
    'N104efupM0g': 'ZTHR1',  # Madina  Sacko: MADINA SACKO
    'tp3OyxREW2c': 'ZPE61',  # Niogona: NIOKONA
    'vxKiWN7aCZL': 'Z8B59',  # Sonkegné: SONKENIE
    'mrCKDnUO4KW': 'ZAWD3',  # Segue: SEGUE-KOLOKANI
    'kCty72jdBwy': 'ZZ3B5',  # Sebekoro I: SEBECORO 1
    'JPgrRdD43TH': 'ZCS99',  # Koulikoroba: KOULIKORO-BA
    'cUHG7iXbz2h': 'ZZAJ9',  # N'Gouni: GOUNI
    'P7EbI0JudQD': 'ZA362',  # Kenenkoun: KENENKOU
    'mi78SnTxE3H': 'Z9JG7',  # N'Gara: NGARA
    'RJgXClkOL9l': 'ZF3B9',  # N'Golobougou: NGOLOBOUGOU
    'GPhDceIqQzn': 'ZZZK4',  # N'Tobougou: NTOBOUGOU
    'HBxSIOT1CkP': 'Z4FM1',  # Mena-Kolondièba: MENA
    'ciISoeK6hf0': 'ZS2S4',  # Farako: FARAKO-KOLONDIEBA
    'nStCCsexjjx': 'ZXDJ6',  # Foulabougoula: FLABOUGOULA
    'FoZ8SPnApbZ': 'ZJSG5',  # Gualala: GOUALALA
    'SjutMzVL5yx': 'Z82K1',  # Guelelenkoro: GUELELINKORO
    'H0nJqqGEv8a': 'ZKHT3',  # Koloni_Y: KOLONI
    'YT44CMxAusA': 'ZEH41',  # Mdiassa: MADINA DIASSA
    'kbTCApn80wX': 'ZYR56',  # Finkologanadougou: FINKOLO GANADOUGOU
    'YSs2mUrWbu9': 'Z9DN2',  # Sibiriifina: SIBIRIFINA
    'TjKsVaiDBGX': 'ZBXJ1',  # Koungoba: KOUNKOBA
    'DnY6wx2fRlp': 'ZZYH5',  # Kléssokoro: KLE-SOKORO
    'EifAUigqKKe': 'Z85P7',  # Dogo: DOGO-BOUGOUNI
    'OAvgk47Amzi': 'ZA550',  # Farangouaran: FARAGOUARAN
    'gFFDwwxbPMq': 'ZKFY4',  # Garalo 1: GARALO
    'sbgkRbBE605': 'ZY495',  # Garalo 2: GARALO II
    'V9DTS8eUOX6': 'ZD7X1',  # N'Golonianasso: NGOLONIANASSO
    'eeB8LZ5Uqb4': 'ZXN31',  # B- Zangasso: ZANGASSO
    'EWiUOMV1yFc': 'ZCDC2',  # Zanzoni: ZANSONI
    'HRqUlyKkTkE': 'ZHKX0',  # Medina Coura: MEDINA-COURA
    'vEDE0T5fnsf': 'ZJ5M4',  # N'Gountjina: NGOUNTJINA
    'izzGFr714tB': 'ZF9K1',  # N'Tosso: NTOSSO
    'RWBaPPVL7ag': 'Z2CW2',  # N'Tossoni: NTOSSONI
    'GJQlfqAQJ54': 'Z7GH0',  # N'Togonasso: NTOGONASSO
    'AataR5837c4': 'ZG7K3',  # M'Péssoba: MPESSOBA
    'GejKYUZkC38': 'Z9FC2',  # Hamdallaye: HAMDALAYE
    'W6fP8W7Neij': 'Z9KC7',  # Fonfana: FONFONA
    'IeL1BFJ1W4T': 'ZB9Z9',  # Konina: KONINA - KOUTIALA
    'H1v8w12Ho0y': 'ZSW43',  # Kouo: KOUWO
    'fTmBJhqRvA2': 'ZX7C1',  # Lofinè: LOFIGUE
    'WTITZrgqZUz': 'Z7AF7',  # Katélé: KATIELE
    'CQqmeRm5fha': 'ZBPM8',  # Nannérébougou: NANEREBOUGOU
    'jSsxZKm61Iq': 'ZKEA0',  # Kignan central: KIGNAN
    'bvDooyy58SI': 'ZRB44',  # Daoula Sonzana: DAOULA-SONZANA
    'AJI2PFfVrI6': 'ZXNH7',  # Medine: MEDINE SIKASSO
    'ZmlLGpwqege': 'Z8HM8',  # Sanoubougou 2: SANOUBOUGOU II
    'x1P3FdS7TS9': 'ZY5W9',  # Kouloukan: KOLOKOBA (???)
    'DiXFtqRNYD7': 'ZEN74',  # Centre Momo: MOMO
    'uVaCkp8JVyW': 'ZBDS9',  # Nongon: NONGO-SOUALA
    'xy4EmMOSoTJ': 'ZRH77',  # Mancourani: MANCOURANIE
    'atgf1VMYnVQ': 'ZS685',  # Sanoubougou 1: SANOUBOUGOU I
    's9AoErW5B5Q': 'Z8TM6',  # Zantiguila: ZANTIGUILA - SIKASSO
    'nsn5N3nLyzK': 'Z6KS4',  # Korobarrage: KORO-BARRAGE
    'svL9H10qVge': 'Z8S42',  # Hamdallaye: HAMDALLAYE SIKASSO
    'lVEIs1wV4xT': 'ZNSP2',  # Wayerma 2: WAYERMA II
    'GrW1S6h9BUq': 'ZWTZ7',  # Kiffosso I: KIFFOSSO
    'l2vbCofachW': 'ZPMX6',  # Ménamba I: MENAMBA
    'WXcznld7vMk': 'ZRHG4',  # Yorosso: YOROSSO CENTRAL
    'BzIcwtprOdI': 'Z24J0',  # Asacos: SOTUBA
    'HXt8sitI4rM': 'Z6F26',  # Asacko Nord: ASACONORD
    'z8y6BjJYkLM': 'ZCCM1',  # Asacofadi: ASACOFADJI
    'zuUZRv2ZAXV': 'Z25N8',  # Gomi: ASACONGOMI
    'lxAsbCT3bux': 'Z23B3',  # Pmi Missira: ASACOMI
    'Oor5kXdqfAG': 'ZSCX6',  # Asacola1: ASACOLA I
    'nJX91JtSI3L': 'ZA8H3',  # Asacolab5: ASACOLA B5
    'iBpaHfBc8wU': 'ZRK55',  # Asacola2: ASACOLA II
    'kbm7xfctXdo': 'ZPGJ5',  # Ascom: ASACOM
    'IstPqjnnbkX': 'ZGY73',  # Ascodar: ASACODAR
    'xnK1joKezig': 'Z8ZP0',  # Asacokoul-Point: ASACOKOULPOINT
    'N0ifQ9mv1rN': 'ZR2R4',  # Asacosab2: ASACOSAB II
    'CuYllztUQsz': 'Z5543',  # Asacosab1: ASACOSAB I
    'KcljkgqgcJR': 'ZGWS9',  # Ascom-Bacodji: ASCOMBACODJI
    'vNLygCa4Bdh': 'ZTX81',  # Pmi-Badala: ASACOBADA PMI
    'aDfasB8VPBY': 'ZZ4E3',  # Asacokalko: ASACOKAL ACI
    'VwcY0hYQDB6': 'ZDMC3',  # Asacosab3: ASACOSAB III
    'FZgyjtbkDeI': 'ZF827',  # Asacoma: ASACOMA I
    'SaycU2nOP0O': 'ZP726',  # Asaco-Sodia: ASACOSODIA
    'ADK521j7yHF': 'Z3J91',  # Asacomiss: ASACOMIS
    'lVpaVqLD7Nc': 'ZKSP3',  # Garbacoira: GARBAKOIRA
    'Bi5UKDUOWxg': 'ZMZK6',  # Dire: DIRE CENTRAL
    'GrZkEKc7Vgr': 'ZP2N5',  # Bourem Sidi Amar: BOUREM-SIDI-AMAR
    'oiHpm4bKwuv': 'ZZAE0',  # N'Daki: NDAKI
    'Nf5p1Txl5BB': 'ZHBK1',  # Koro Bella: KORO BELLAH
    'PvI2B0w7vtQ': 'ZGFD9',  # Tintadenit: TINTADENI
    'J8fJza0Z3Eo': 'ZPBE1',  # Bellefarandi: BELLAFARANDI
    'j483LXcYB5x': 'ZEY44',  # Zarho: ZORKO
    'hY5vmgashNN': 'Z9HA0',  # Hassidina: ASSIDI
    'UbcZenbrXT0': 'ZY932',  # Bourem Inaly: BOUREMINALY
    'UzFNfcCH3Jy': 'Z42Y8',  # Eryntédjeft: ERINTEDJEFT
    'sG8G2P76a2R': 'ZW5T0',  # Tin Telout: TIN - TELOUT
    'X3TgOVb0kSg': 'ZXDY3',  # Mekore: MIKORE
    'E3iaxoNe6ic': 'ZXFX2',  # Tin-Aicha: TIN AICHA
    'NjmIASs7F2w': 'ZDZZ5',  # Issa-Bery: ISSABERRY
    'GXjiZPFkDB6': 'ZTH67',  # Adarmalane: ADERMALANE
    'UInuZWMTrxD': 'ZDB57',  # Wako: OUONKO
    'Fr9rUbmijcU': 'ZNTN2',  # Garnati: GARNATY
    'cqcUI6lgYM3': 'ZXRX0',  # Timtaghène: TIMTAGHÈNE (INABAG)
    'YEtsSLvyYt6': 'ZS8B1',  # Tessalit_C: TESSALIT CSREF
    'jyloy66TDQ2': 'ZK7K2',  # Adjel-Hoc: ASSEKHAT (ADEL - HOC)
    'enaZpZPTrmt': 'ZRW53',  # Niono Extension: NIONO EXTENTION
    'dHQDDiXlFar': 'Z3KZ4',  # K2: NIONO K2
    'NNPks8Wzggo': 'Z7JS5',  # Mbewani: M'BEWANI
    'oOuf5ooIaT4': 'Z3PE3',  # Waky: WAKI
    'yzJoEpubG04': 'ZTBP8',  # M'Pesso Hameau: MPESSO HAMEAU
    'WM4QYhkLqbT': 'ZWWS6',  # N'Torosso: NTOROSSO
    'ygj5n6Z00Uf': 'ZZRT0',  # Koro: KORO-SAN
    'wJlTWf5TWnh': 'ZZB23',  # Niamana: NIAMANA BANKOUMA
    'LUTOo34drvr': 'ZJZT5',  # Somo - San: SOMO-SAN
    'CgwdGxXLuW5': 'ZN8H1',  # Csa Central: SAN CENTRAL
    'N0pqa5UOup8': 'ZKY52',  # N'Goa: NGOA
    'if5gjQXkMLu': 'Z28P5',  # Koila: KOILA BAMANA
    'Y7cJH7IGuYd': 'ZA2B0',  # Komola-Zanfina: KOMOLA - ZAFINA
    'fDMJnQLZvto': 'ZHA96',  # Cst: TOMINIAN CENTRAL
    'IxmKEFcuFYr': 'ZYCN6',  # N'Golokouna: NGOLOKOUNA
    'kP39YWFVVDz': 'Z2DT2',  # Souleye: SOULEY
    'xJP8oweER4R': 'ZRF50',  # Monimpe: MONIMPEBOUGOU
    'WOpsLpYM7hH': 'Z88M4',  # Boukiwere: BOKY WERE
    'W2Y8OzgXfrc': 'Z2KG8',  # Touhara: TOUARA
    'VSgwuTNImH5': 'ZZ594',  # Oulan: OULA
    'PkMU2e6nilz': 'ZPTA4',  # Niamana: NIAMANA - BLA
    'LttqSLp55zh': 'ZFBM1',  # Tallo: TALO BAMBANAN
    'UiH558P9RLO': 'ZPC43',  # Tériyabougou: TERYABOUGOU
    'q4zXTS3vfnl': 'ZN3H6',  # N'Djilla: NDJILLA
    'NrbqA6JfIH9': 'Z3DM3',  # Banido: BANINDO
    'umVxHaOkOuX': 'ZMA26',  # Somo - Baroueli: SOMO-BAROUELI
    'xTTrSNoHQtl': 'ZT7C1',  # M'Pebougou: MPEBOUGOU
    'tib6uEpLhbc': 'Z3RH0',  # N'Gassola: NGASSOLA
    'v4VxeqvuCMm': 'ZPTW9',  # Dougounikoro: DOUGOUNIKORO
    'ckqAb0zHZPi': 'ZA5T4',  # Sekoro: SÉCORO
    'UJtJiH3y8Ik': 'Z2X97',  # Zambougou-Cinzana: ZAMBOUGOU CINZANA
    'hKSmJPQpgDc': 'Z9542',  # Yollo: YOLO
    'ORwtLncTogi': 'Z9MS2',  # Cinzana Gare: CINZANA
    'GRaym4rri8e': 'ZHXP8',  # Tongo: TONGOU
    'cyiuw70qQWv': 'Z4JB9',  # Zambougou-Central: ZAMBOUGOU CENTRAL
    'nh3haGFPEwC': 'ZM7P0',  # Bananissaba Somon: BANANISSABA-SOMON
    'fxyVr2lwtnW': 'ZPEC8',  # Pelegana Sud: PELENGANA SUD
    'WCenW9Yl8Vj': 'ZTNH7',  # Segou Coura Baka: SEGOU - COURA
    'SyhQmYZ4011': 'Z43J1',  # N'Tombougou-DIGANI: NTOBOUGOU
    'w0YX5VsYpsP': 'ZFZJ8',  # Ouro Guiya: OURONGUIA
    'v7Wq5fQUSpI': 'ZKH98',  # Tenenkou: TENENKOU CENTRAL
    'NG2OtrLh0pA': 'ZPDK8',  # Walo: WALLO
    'OXqOZMlp2l7': 'ZZWA9',  # Senebamana: SENE BAMANA
    'lJEKPAdk83J': 'ZSWK8',  # Mopti Keba: MOPTI-KEBA
    'E9mUw1h1hKj': 'ZYSN0',  # Dianweli Maoundé: DIANWELY
    'Lijc7Y6k3KW': 'Z9RF9',  # Koubewel Koundia: KOUBEWEL
    'WRVNE6xpbXC': 'Z3XG4',  # Niangassaiou: NIAGASSADIOU
    'roBc3ryavUa': 'Z8E76',  # Central: DOUENTZA CENTRAL
    'MaIUrJA7BCN': 'Z2GG2',  # Dialoubé: DIALLOUBE
    'ojwssAz7IPc': 'ZDA48',  # N'Gouma: NGOUMA
    't3xKiuCnXwA': 'ZGG71',  # Nouh Bozo: NOUHBOZO
    'BRQwKv1PwcW': 'ZY486',  # Djigui Bombo: DJIGUIBOMBO
    'lSHsVUD0KA4': 'ZJ9W8',  # Kani-G: KANI-GOGOUNA
    'ajUMKIQCepL': 'Z3276',  # Iby: IBY-AMATO
    'ppqLLe8ksT3': 'ZSR97',  # Diankassagou: DIANGASSAGOU
    'tBCyLAVjUqI': 'ZMJE4',  # Tabi Tongo: TABITONGO
    'N3BoQtT231D': 'ZJEN7',  # Yendouma: YENDOUMA-SOGOL
    'lCQV0X4qkjn': 'ZRZN5',  # Kori-Maoudé: KORI-MAOUNDE
    'BXBGQpJrSrJ': 'ZTEC7',  # Bendjeli: BENDIELY
    'JGCTHcMYdub': 'Z88F6',  # Dogani-Béré: DOGANI - BERE
    'x149MuUom9a': 'ZAWK2',  # Youwarou-Central: YOUWAROU CENTRAL
    'I00hKXCGdKN': 'ZNMF0',  # Guidio-Sare: GUIDIO
    'PacAHa9kmwi': 'Z9TX4',  # Dinangourou: DINAGOUROU
    'tzRlwg6oq30': 'ZT2W3',  # Koporo Na: KOPORONA
    'CVVSsbVgeNj': 'ZEM75',  # Bamba-Koro: BAMBA
    'FfWDHi9Z93f': 'ZCNA2',  # Guinaolo: GUINAWALO
    'NRPYraZW9ee': 'ZDAK3',  # Diallassagou: DIALLASSAGOU (ASACODA)
    'MesXQXixjcd': 'ZJ321',  # Sokoura_B: SOKOURA (ASACOSO)
    'N9Dz0vnbjtK': 'Z28G7',  # Koulogo: KOULOGON
    'etUbESMvHR8': 'ZG728',  # Lessagou: LESSAGOU - HABE
    'w7AfSz4PJh8': 'ZKR30',  # Kani-Bonzon: KANI - BONZON
    'N0kJ0DHevuE': 'ZFW65',  # Niamnia: NIAMIA
    'TwBt3hbdkUL': 'ZTEG7',  # Ouenkoro: OUONKORO
    'dAYMc3Hofzl': 'ZF747',  # Tori: TORI (ASACOTO)
    'YewxtqpZ2Cz': 'ZT7G1',  # Soufroulaye: SOUFOUROULAYE
    'AZ97emYTCa4': 'ZACE3',  # Ascotam: ASCOTAMB
    'cxSbSuwYF8g': 'ZAC76',  # Sare Dina: SAREDINA
    'GuYJomSAGUT': 'Z7E27',  # Sévaré 3: SEVARE III
    'wviL572vcWR': 'ZKW74',  # Kontza: KONTZA PEULH
    'zNw1dJw10FV': 'Z3JR6',  # Sokoura: SOCOURA
    'cgX0AKVMpU3': 'ZP2G7',  # Tongorongon: TONGORONGO
    'aGRfXSFYxbv': 'ZKTE4',  # Sevare 2: SEVARE II
    'Kq5E5yM8rO6': 'ZAEH0',  # Sévéry: SEVERY PEULH
    'G7dJRUoqfQL': 'ZD2H9',  # Sare Mala: SAREMALA
    's5N8h8tRnW3': 'ZSCE9',  # Kersignane Diafounou: KERSIGNANE
    'MLxy0yeLB4Z': 'Z57T4',  # Niogomera: NOGOMERA
    'mrK6oHPIyvS': 'ZZAX6',  # Yaguine Banda: YAGUINE
    'f4epQEj9U1F': 'Z46H8',  # Hamdallaye: HAMDALLAYE YELIMANE
    'Z7OMSBpHZT5': 'ZKRY2',  # Badiougoula: BANDIOUGOULA
    'vRrC3aPsNKc': 'Z97N5',  # Diabaguela: DIABIGUE
    'MV464gVx2Mt': 'ZWY20',  # Banierekore: BANIERE KORE
    'mQM26CTb59j': 'Z7HS7',  # Diaye Coura: DIAYE KOURA
    'vnXc1XRCWBc': 'ZJ7Z9',  # Gadiaba Kadiel: GADIABA-KADIEL
    'FjsXW3H5oK9': 'ZCKF4',  # Fosse Karta: FOSSE KAARTA
    'd7lmjRT9vWc': 'ZB6X2',  # Diarah: DIARRAH
    'V7h6ZZ9Y0aj': 'ZW4G3',  # Frandalla: FRANDALAH
    'TRgC6DxWbmO': 'ZBF63',  # Dianwely Kounda: DIANWELY COUNDA
    'nreyqk3x503': 'ZZNX3',  # Djoufoya Tintokan: DJOUFOYA TINTOKA
    'T3RfBIUrfrT': 'ZG846',  # Sibindi: SIBINDY
    'XeAPFG66BRZ': 'Z8B88',  # Sawané: SAVANE
    'yZxYnXGHlUj': 'Z3T42',  # Oussibidiagna: OUSSOUBIDJANGNA CENTRAL
    'H0Hlh334TRs': 'ZHZA9',  # Modinkanou: MODINCANOU
    'osGiyOdP8Cn': 'ZEKR2',  # Trentimou: TRANTIMOU
    'UIywVdeG85t': 'ZMF90',  # Kourounikoto: KOUROUNINKOTO
    'DHcxJB3jWBr': 'ZCKC5',  # Darsalam_Kita: DARSALAM-KITA
    'wMB9WxlOML4': 'Z3FK2',  # Saint Felix: SAINT-FELIX
    'HCpQ8zK09cZ': 'ZMHZ1',  # Kobri: KOBRY
    'sKIgFHeteix': 'Z5YR1',  # Nafadjicoro: NAFADJI-CORO
    'FDf5HwqY1ZE': 'ZJ6M3',  # Selinkegny: SELINKEGNI
    'w12XNvAd4Cu': 'ZXKG0',  # Madinakouta: MADINACOUTA
    'ZZFPBTYvOTQ': 'ZYFW2',  # Diokely: DIOKELI
    'LEfz3A2Ek4p': 'ZZ3P2',  # Bafoulabé: BAFOULABE CENTRAL
    'DNi7RSxvrxq': 'ZTDG8',  # Niakalensiriya: NIAKALESIRAYA
    'ktuDkZyvQwo': 'ZCPB0',  # Liberte: KAYES LIBERTE
    'jKf44I42Lzq': 'Z2JK8',  # Bankassi: BANGASSI
    'rAkWHAfLIxz': 'ZZYW2',  # Khasso: KAYES - KHASSO
    'Virn66NiIrk': 'ZGJJ4',  # Same Ouolof: SAME - KAYES
    'nbyRVNIGMMl': 'Z7BG6',  # Lany-Tounka: LANY TOUNKA
    'ztnw0xHdLCU': 'ZCWN1',  # Dialané: DIALLANE
    'kFWstwO6LBu': 'ZBH90',  # Ambidedikore: AMBIDEDI-KORE
    'Wed3WnwymSo': 'ZWXH7',  # Ambidedi-Poste: AMBIDEDI POSTE
    'c3JmLG5zq1g': 'ZBM85',  # Tafassirga: TAFACIRGA
    'zk4Udf1i2Fx': 'ZY545',  # Tichy: TICHY LEYA
    'iSyDnHLI9sf': 'Z9AN5',  # Dialakasso: DIALA KHASSO
    'GPjZbH5DQI9': 'ZFX44',  # Gory-Gopela: GORI - GOPELA
    'quVNjXjemJS': 'ZXF49',  # Boutinguisse: BOUNTINGUISSE
    'eeTKsuDsRq2': 'ZA2H9',  # Logo-Saboussiré: LOGOSABOUCIRE
    'g1VULYikS5k': 'ZA2N8',  # Marena-Gadiaga: MARENA GADIAGA
    'VaCkzictPhR': 'Z99Y0',  # Marena-Diombougou: MARENA DIOMBOUGOU
    'Xiycf17YZNP': 'ZGZA9',  # Lafiabougou: KAYES LAFIABOUGOU
    't6eXi17kdeS': 'Z2DK4',  # Baye-Kéniéba: BAYE KENIEBA
    'Y1mFfPanvTc': 'ZY5M0',  # Guene-Gore: GUENEGORE
    'yrzlLDBktlZ': 'ZHWA2',  # Guenoubatan: GUENOUBANTAN
    'M0k0suUULSY': 'ZRKE2',  # Guindessou: GUINDINSOU
    'yAUa5PUjBTp': 'ZBAH4',  # Dialafara: DIALAFARA-KENIEBA
    'gZzBKtMntyK': 'ZM963',  # Sanougou: SANOUKOU
    'm3FvBNsxAWq': 'ZW4B4',  # Lattakaf: LATAKAFF
    'fVwMLm5F1NB': 'ZMB84',  # Dianguonté Camara: DIANGOUNTE CAMARA
    'yNxXkVYcDrC': 'ZCG42',  # Gomitradougou: GUOMITRADOUGOU
    'NE83oDX6GMP': 'ZK9X7',  # Forgo: FORGHO
    'n0Z1CUatgLJ': 'ZXDD8',  # Tin Aouker: TIN-AOUKER
    'WlBzzSLMfiT': 'Z3PA3',  # Tamakoutat: TAMKOUTAT
    'YDWXBWLX79I': 'Z2WH5',  # Magnadoué: MAGNADOE
    'YfOve9Co23w': 'Z6TP6',  # Bagnandji: BAGNADJI
    'C36xw283g93': 'Z5HT7',  # Diebock: DJEBOCK
    'UkNIG1bIcHq': 'ZYBN7',  # Marsi: MARSY
    'SQl3vSV9rpz': 'ZJ3G7',  # Boulgoundje: BOULGOUNDIE
    'rs4M1IAIHu9': 'Z9P45',  # Imilach: IMILACHE
    'KagRZ4pyI1U': 'ZTXN6',  # Tinsako: TINSAKOU
    'HgO41Wyt2DC': 'ZRRC5',  # Bamba Bourem: BAMBA
    'GGWxzCBpPns': 'Z67N5',  # Abakoria: ABAKOIRA
    'rPHK7FzXPuk': 'Z7H83',  # Ouatagouna: OUATTAGOUNA
    'mfPmL5jINqJ': 'ZS7S9',  # Herba: HERBA - KOUSOUM
    'OzDIkYMKnks': 'ZJWS8',  # Bazigourma: BAZI GOURMA
    'XQi1nOH9UEm': 'ZDTY1',  # Kaygoutane: KAIDJOUROUTANE
    'cFK1D0SI4qi': 'Z9T80',  # Tinhamma: TIN-HAMMA
    'GY4RihfB6Sl': 'ZZ278',  # Bazihaoussa: BAZI HAOUSSA


}

mapping = {}


def update(dhis, snisi):
    global mapping

    mapping[dhis['id']] = snisi.slug


def get_match(snisi_children, dhis):
    for child in snisi_children:
        if norm(child.name) == norm(dhis['name']):
            return child
    if dhis['id'] in custom_mapping.keys():
        return Entity.get_or_none(custom_mapping[dhis['id']])
    return None


def get_children(dhis):
    return [child for child in dhis['children'] if child not in skip_ids]


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("started SNISI-DHIS matcher")

        # root level
        root_dhis = get_ou(MALI_DHIS_IS)
        root_snisi = Entity.get_or_none("mali")
        update(root_dhis, root_snisi)

        logger.info("matched root level {d}:{s}".format(
                    d=root_dhis['id'],
                    s=root_snisi.slug))

        # region level
        snisi_regions = root_snisi.get_health_regions()
        for region_dhis_id in get_children(root_dhis):
            region_dhis = get_ou(region_dhis_id)

            logger.debug("# RS {}".format(region_dhis['name']))

            # DEBUG TODO
            if region_dhis['name'] in ("Koulikoro", "Sikasso",
                                       "Bamako", "Tombouctou",
                                       "Kidal", "Ségou", "Mopti", "Kayes"):
                continue

            region_snisi = get_match(snisi_regions, region_dhis)
            if region_snisi is None:
                from pprint import pprint as pp ; pp(region_dhis)
                raise
            logger.info("matched region level {d}:{s}".format(
                        d=region_dhis['id'],
                        s=region_snisi.slug))

            # district level
            snisi_districts = region_snisi.get_health_districts()
            for district_dhis_id in get_children(region_dhis):
                district_dhis = get_ou(district_dhis_id)

                logger.debug("## DS  {}".format(district_dhis['name']))

                district_snisi = get_match(snisi_districts, district_dhis)
                if district_snisi is None:
                    from pprint import pprint as pp ; pp(district_dhis)
                    raise
                logger.info("matched district level {d}:{s}".format(
                            d=district_dhis['id'],
                            s=district_snisi.slug))

                # health area level
                snisi_areas = region_snisi.get_health_areas()
                for area_dhis_id in get_children(district_dhis):
                    area_dhis = get_ou(area_dhis_id)

                    logger.debug("### HA  {}".format(area_dhis['name']))

                    area_snisi = get_match(snisi_areas, area_dhis)
                    if area_snisi is None:
                        from pprint import pprint as pp ; pp(area_dhis)
                        raise Exception("SNISI HA is None")
                    logger.info("matched area level {d}:{s}".format(
                                d=area_dhis['id'],
                                s=area_snisi.slug))

        logger.info("done matching.")
