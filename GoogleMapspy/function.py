from urllib.parse import unquote
import requests
import random
import json
import numpy as np
import math

# --- Constants for geographic calculations (from your original) ---
earth_radius = 6370.856
math_2pi = math.pi * 2
pis_per_degree = math_2pi / 360

# --- Geographic helper functions (from your original) ---
def lat_degree2km(dif_degree=.0001, radius=earth_radius):
    return radius * dif_degree * pis_per_degree

def lat_km2degree(dis_km=111, radius=earth_radius):
    return dis_km / radius / pis_per_degree

def lng_degree2km(dif_degree=.0001, center_lat=22):
    real_radius = earth_radius * math.cos(center_lat * pis_per_degree)
    return lat_degree2km(dif_degree, real_radius)

def lng_km2degree(dis_km=1, center_lat=22):
    real_radius = earth_radius * math.cos(center_lat * pis_per_degree)
    return lat_km2degree(dis_km, real_radius)

# --- User Agents (from your original) ---
agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20', # Removed extra quote
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1'
]

# --- Country Dictionaries (from your original) ---
google_country_dict = {'afghanistan': 'Afghanistan', 'åland islands': 'Åland Islands', 'albania': 'Albania',
                       'algeria': 'Algeria', 'american samoa': 'American Samoa', 'andorra': 'Andorra',
                       'angola': 'Angola', 'anguilla': 'Anguilla', 'antarctica': 'Antarctica',
                       'antigua and barbuda': 'Antigua and Barbuda', 'argentina': 'Argentina', 'armenia': 'Armenia',
                       'aruba': 'Aruba', 'australia': 'Australia', 'austria': 'Austria', 'azerbaijan': 'Azerbaijan',
                       'bahamas': 'The Bahamas', 'bahrain': 'Bahrain', 'bangladesh': 'Bangladesh',
                       'barbados': 'Barbados', 'belarus': 'Belarus', 'belgium': 'Belgium', 'belize': 'Belize',
                       'benin': 'Benin', 'bermuda': 'Bermuda', 'bhutan': 'Bhutan', 'bolivia': 'Bolivia',
                       'bonaire, sint eustatius and saba (netherlands)': 'Sint Eustatius',
                       'bosnia and herzegovina': 'Bosnia and Herzegovina', 'botswana': 'Botswana',
                       'bouvet island': 'Bouvet Island', 'brazil': 'Brazil',
                       'british indian ocean territory': 'British Indian Ocean Territory',
                       'brunei darussalam': 'Brunei', 'brunei': 'Brunei', 'bulgaria': 'Bulgaria',
                       'burkina faso': 'Burkina Faso', 'burundi': 'Burundi', 'cape verde': 'Cape Verde',
                       'cambodia': 'Cambodia', 'cameroon': 'Cameroon', 'canada': 'Canada',
                       'cayman islands': 'Cayman Islands', 'central african': 'Central African Republic',
                       'central african republic': 'Central African Republic', 'chad': 'Chad', 'chile': 'Chile',
                       'china': 'China', 'christmas island': 'Christmas Island', 'colombia': 'Colombia',
                       'comoros': 'Comoros', 'democratic republic of congo': 'Democratic Republic of the Congo',
                       'congo dr': 'Democratic Republic of the Congo', 'congo': 'Democratic Republic of the Congo',
                       'cook islands': 'Cook Islands', 'costa rica': 'Costa Rica', 'croatia': 'Croatia', 'cuba': 'Cuba',
                       'curaçao': 'Curaçao', 'cyprus': 'Cyprus', 'czech republic': 'Czechia', 'denmark': 'Denmark',
                       'djibouti': 'Djibouti', 'dominica': 'Dominica', 'dominican rep': 'Dominican Republic',
                       'dominican republic': 'Dominican Republic', 'ecuador': 'Ecuador', 'egypt': 'Egypt',
                       'el salvador': 'El Salvador', 'equatorial guinea': 'Equatorial Guinea', 'eritrea': 'Eritrea',
                       'estonia': 'Estonia', 'ethiopia': 'Ethiopia',
                       'falkland islands  [malvinas]': 'Falkland Islands (Islas Malvinas)',
                       'faroe islands (denmark)': 'Faroe Islands', 'fiji': 'Fiji', 'finland': 'Finland',
                       'france': 'France', 'french guiana (france)': 'French Guiana',
                       'french polynesia (france)': 'French Polynesia',
                       'french southern territories': 'French Southern and Antarctic Lands', 'gabon': 'Gabon',
                       'gambia': 'The Gambia', 'georgia': 'Georgia', 'germany': 'Germany', 'ghana': 'Ghana',
                       'gibraltar': 'Gibraltar', 'greece': 'Greece', 'greenland (denmark)': 'Greenland',
                       'grenada': 'Grenada', 'guadeloupe (france)': 'Guadeloupe',
                       'guam (united states of america)': 'Guam', 'guatemala': 'Guatemala',
                       'guernsey (united kingdom)': 'Guernsey', 'guinea': 'Guinea', 'guinea bissau': 'Guinea-Bissau',
                       'guyana': 'Guyana', 'haiti': 'Haiti',
                       'heard island and mcdonald islands': 'Heard Island and McDonald Islands',
                       'holy see': 'Vatican City', 'honduras': 'Honduras', 'hong kong': 'Hong Kong',
                       'hungary': 'Hungary', 'iceland': 'Iceland', 'india': 'India', 'indonesia': 'Indonesia',
                       'islamic republic of iran': 'Iran', 'iraq': 'Iraq', 'ireland': 'Ireland',
                       'isle of man (united kingdom)': 'Isle of Man', 'israel': 'Israel', 'italy': 'Italy',
                       'jamaica': 'Jamaica', 'japan': 'Japan', 'jersey (united kingdom)': 'Jersey', 'jordan': 'Jordan',
                       'kazakhstan': 'Kazakhstan', 'kenya': 'Kenya', 'kiribati': 'Kiribati',
                       'democratic peoples republic of korea': 'North Korea', 'republic of korea': 'South Korea',
                       'kuwait': 'Kuwait', 'kyrgyzstan': 'Kyrgyzstan', 'latvia': 'Latvia', 'lebanon': 'Lebanon',
                       'lesotho': 'Lesotho', 'liberia': 'Liberia', 'libya': 'Libya', 'liechtenstein': 'Liechtenstein',
                       'lithuania': 'Lithuania', 'luxembourg': 'Luxembourg', 'macao': 'Macao',
                       'macedonia': 'North Macedonia', 'macedonia (fyrom)': 'North Macedonia',
                       'madagascar': 'Madagascar', 'malawi': 'Malawi', 'malaysia': 'Malaysia', 'maldives': 'Maldives',
                       'mali': 'Mali', 'malta': 'Malta', 'marshall islands': 'Marshall Islands',
                       'martinique': 'Martinique', 'martinique (france)': 'Martinique', 'mauritania': 'Mauritania',
                       'mauritius': 'Mauritius', 'mayotte (france)': 'Mayotte', 'mexico': 'Mexico',
                       'republic of moldova': 'Moldova', 'monaco': 'Monaco', 'mongolia': 'Mongolia',
                       'montenegro': 'Montenegro', 'montserrat': 'Montserrat', 'morocco': 'Morocco',
                       'mozambique': 'Mozambique', 'myanmar/burma': 'Myanmar (Burma)', 'namibia': 'Namibia',
                       'nauru': 'Nauru', 'nepal': 'Nepal', 'netherlands': 'Netherlands',
                       'new caledonia (france)': 'New Caledonia', 'new zealand': 'New Zealand',
                       'nicaragua': 'Nicaragua', 'niger': 'Niger', 'nigeria': 'Nigeria', 'niue': 'Niue',
                       'norfolk island': 'Norfolk Island', 'northern mariana islands': 'Northern Mariana Islands',
                       'norway': 'Norway', 'oman': 'Oman', 'pakistan': 'Pakistan', 'palau': 'Palau',
                       'palestinian territories': 'Palestine', 'panama': 'Panama',
                       'papua new guinea': 'Papua New Guinea', 'paraguay': 'Paraguay', 'peru': 'Peru',
                       'philippines': 'Philippines', 'pitcairn': 'Pitcairn Islands', 'poland': 'Poland',
                       'portugal': 'Portugal', 'puerto rico': 'Puerto Rico',
                       'puerto rico (united states of america)': 'Puerto Rico', 'reunion (france)': 'Réunion',
                       'romania': 'Romania', 'russian federation': 'Russia', 'rwanda': 'Rwanda',
                       'saint helena, ascension and tristan da cunha': 'St Helena, Ascension and Tristan da Cunha',
                       'saint kitts and nevis': 'St Kitts & Nevis', 'saint lucia': 'St Lucia',
                       'saint martin (france)': 'St Martin', 'saint pierre and miquelon': 'St Pierre and Miquelon',
                       'saint vincent and the grenadines': 'St Vincent and the Grenadines', 'samoa': 'Samoa',
                       'san marino': 'San Marino', 'sao tome and principe': 'São Tomé and Príncipe',
                       'saudi arabia': 'Saudi Arabia', 'senegal': 'Senegal', 'serbia': 'Serbia',
                       'seychelles': 'Seychelles', 'sierra leone': 'Sierra Leone', 'singapore': 'Singapore',
                       'sint maarten': 'Sint Maarten', 'slovakia': 'Slovakia', 'slovenia': 'Slovenia',
                       'solomon islands': 'Solomon Islands', 'somalia': 'Somalia', 'south africa': 'South Africa',
                       'south georgia and the south sandwich islands': 'South Georgia and the South Sandwich Islands',
                       'south sudan': 'South Sudan', 'spain': 'Spain', 'sri lanka': 'Sri Lanka', 'sudan': 'Sudan',
                       'suriname': 'Suriname', 'svalbard and jan mayen': 'Svalbard and Jan Mayen',
                       'swaziland': 'Eswatini', 'sweden': 'Sweden', 'switzerland': 'Switzerland',
                       'syrian arab republic': 'Syria', 'taiwan': 'Taiwan', 'tajikistan': 'Tajikistan',
                       'united republic of tanzania': 'Tanzania', 'thailand': 'Thailand', 'timor-leste': 'Timor-Leste',
                       'togo': 'Togo', 'tokelau': 'Tokelau', 'tonga': 'Tonga',
                       'trinidad and tobago': 'Trinidad and Tobago', 'tunisia': 'Tunisia', 'turkey': 'Turkey',
                       'turkmenistan': 'Turkmenistan', 'turks and caicos islands': 'Turks and Caicos Islands',
                       'tuvalu': 'Tuvalu', 'uganda': 'Uganda', 'ukraine': 'Ukraine',
                       'united arab emirates': 'United Arab Emirates', 'united kingdom': 'United Kingdom',
                       'united states minor outlying islands': 'United States Minor Outlying Islands',
                       'united states of america': 'United States', 'uruguay': 'Uruguay', 'uzbekistan': 'Uzbekistan',
                       'vanuatu': 'Vanuatu', 'venezuela': 'Venezuela', 'vietnam': 'Vietnam',
                       'virgin islands (british)': 'British Virgin Islands',
                       'virgin islands (united states of america)': 'U.S. Virgin Islands',
                       'wallis and futuna': 'Wallis and Futuna', 'western sahara*': 'Western Sahara', 'yemen': 'Yemen',
                       'zambia': 'Zambia', 'zimbabwe': 'Zimbabwe', 'lao peoples democratic republic': 'Laos',
                       'cote divoire': "Côte d'Ivoire", 'kosovo': 'Kosovo'}

country_suffix_dict = {'af': 'Afghanistan', 'fk': 'land Islands', 'al': 'Albania', 'dz': 'Algeria',
                       'as': 'American Samoa', 'ad': 'Andorra', 'ao': 'Angola', 'ai': 'Anguilla', 'aq': 'Antarctica',
                       'ag': 'Antigua and Barbuda', 'ar': 'Argentina', 'am': 'Armenia', 'aw': 'Aruba',
                       'au': 'Australia', 'at': 'Austria', 'az': 'Azerbaijan', 'bs': 'Bahamas', 'bh': 'Bahrain',
                       'bd': 'Bangladesh', 'bb': 'Barbados', 'by': 'Belarus', 'be': 'Belgium', 'bz': 'Belize',
                       'bj': 'Benin', 'bm': 'Bermuda', 'bt': 'Bhutan', 'ga': 'Bolivia', 'ba': 'Bosnia and Herzegovina',
                       'bw': 'Botswana', 'bv': 'Bouvet Island', 'br': 'Brazil', 'io': 'British Indian Ocean Territory',
                       'bn': 'Brunei Darussalam', 'bg': 'Bulgaria', 'bf': 'Burkina Faso', 'bi': 'Burundi',
                       'cv': 'Cape Verde', 'kh': 'Cambodia', 'cm': 'Cameroon', 'ca': 'Canada', 'ky': 'Cayman Islands',
                       'cf': 'Central African Republic', 'td': 'Chad', 'cl': 'Chile', 'cn': 'China',
                       'cx': 'Christmas Island', 'cc': 'Cocos', 'co': 'Colombia', 'km': 'Comoros', 'cg': 'Congo',
                       'ck': 'Cook Islands', 'cr': 'Costa Rica', 'hr': 'Croatia', 'cu': 'Cuba', 'cy': 'Cyprus',
                       'cz': 'Czech Republic', 'dk': 'Denmark', 'dj': 'Djibouti', 'do': 'Dominica', 'ec': 'Ecuador',
                       'eg': 'Egypt', 'sv': 'El Salvador', 'cq': 'Equatorial Guinea', 'ee': 'Estonia', 'et': 'Ethiopia',
                       'fo': 'Faroe Islands (Denmark)', 'fj': 'Fiji', 'fi': 'Finland', 'fr': 'France',
                       'gf': 'French Guiana (France)', 'pf': 'French Polynesia (France)',
                       'tf': 'French Southern Territories', 'gm': 'Gambia', 'ge': 'Georgia', 'de': 'Germany',
                       'gh': 'Ghana', 'gi': 'Gibraltar', 'vi': 'Greece', 'gl': 'Grenada', 'gp': 'Guadeloupe (France)',
                       'gt': 'Guatemala', 'gn': 'Guinea', 'gw': 'Guinea Bissau', 'gy': 'Guyana', 'ht': 'Haiti',
                       'hm': 'Heard Island and McDonald Islands', 'va': 'Holy See', 'hn': 'Honduras', 'hk': 'Hong Kong',
                       'hu': 'Hungary', 'is': 'Iceland', 'in': 'India', 'id': 'Indonesia',
                       'ir': 'Islamic Republic of Iran', 'iq': 'Iraq', 'ie': 'Ireland', 'il': 'Israel', 'it': 'Italy',
                       'jm': 'Jamaica', 'jp': 'Japan', 'jo': 'Jordan', 'kz': 'Kazakhstan', 'ke': 'Kenya',
                       'ki': 'Kiribati', 'kp': 'Democratic Peoples Republic of Korea', 'kr': 'Republic of Korea',
                       'kw': 'Kuwait', 'kg': 'Kyrgyzstan', 'lv': 'Latvia', 'lb': 'Lebanon', 'ls': 'Lesotho',
                       'lr': 'Liberia', 'ly': 'Libya', 'li': 'Liechtenstein', 'lt': 'Lithuania', 'lu': 'Luxembourg',
                       'mo': 'Macao', 'mg': 'Madagascar', 'mw': 'Malawi', 'my': 'Malaysia', 'mv': 'Maldives',
                       'ml': 'Mali', 'mt': 'Malta', 'mh': 'Marshall Islands', 'mq': 'Martinique (France)',
                       'mr': 'Mauritania', 'mx': 'Mexico', 'fm': 'Micronesia', 'md': 'Republic of Moldova',
                       'mc': 'Monaco', 'mn': 'Mongolia', 'ms': 'Montserrat', 'ma': 'Morocco', 'mz': 'Mozambique',
                       'mm': 'Myanmar/Burma', 'na': 'Namibia', 'nr': 'Nauru', 'np': 'Nepal', 'nl': 'Netherlands',
                       'nc': 'New Caledonia (France)', 'nz': 'New Zealand', 'ni': 'Nicaragua', 'ne': 'Niger',
                       'ng': 'Nigeria', 'nu': 'Niue', 'nf': 'Norfolk Island', 'mp': 'Northern Mariana Islands',
                       'no': 'Norway', 'om': 'Oman', 'pk': 'Pakistan', 'pw': 'Palau', 'pa': 'Panama',
                       'pg': 'Papua New Guinea', 'py': 'Paraguay', 'pe': 'Peru', 'ph': 'Philippines', 'pn': 'Pitcairn',
                       'pl': 'Poland', 'pt': 'Portugal', 'qa': 'Qatar', 're': 'Reunion (France)', 'ro': 'Romania',
                       'ru': 'Russian Federation', 'rw': 'Rwanda', 'kn': 'Saint Kitts and Nevis', 'sh': 'Saint Lucia',
                       'pm': 'Saint Pierre and Miquelon', 'vc': 'Saint Vincent and the Grenadines', 'sm': 'San Marino',
                       'st': 'Sao Tome and Principe', 'sa': 'Saudi Arabia', 'sn': 'Senegal', 'sc': 'Seychelles',
                       'sl': 'Sierra Leone', 'sg': 'Singapore', 'sk': 'Slovakia', 'si': 'Slovenia',
                       'sb': 'Solomon Islands', 'so': 'Somalia', 'za': 'South Africa', 'ss': 'South Sudan',
                       'es': 'Spain', 'lk': 'Sri Lanka', 'sd': 'Sudan', 'sr': 'Suriname', 'sz': 'Swaziland',
                       'se': 'Sweden', 'ch': 'Switzerland', 'sy': 'Syrian Arab Republic', 'tw': 'Taiwan',
                       'tj': 'Tajikistan', 'tz': 'United Republic of Tanzania', 'th': 'Thailand', 'tl': 'Timor-Leste',
                       'tg': 'Togo', 'tk': 'Tokelau', 'to': 'Tonga', 'tt': 'Trinidad and Tobago', 'tn': 'Tunisia',
                       'tr': 'Turkey', 'tm': 'Turkmenistan', 'tc': 'Turks and Caicos Islands', 'tv': 'Tuvalu',
                       'ug': 'Uganda', 'ua': 'Ukraine', 'ae': 'United Arab Emirates', 'uk': 'United Kingdom',
                       'pr': 'United States Minor Outlying Islands', 'us': 'United States of America', 'uy': 'Uruguay',
                       'vu': 'Vanuatu', 've': 'Venezuela', 'vn': 'VietNam', 'vg': 'Virgin Islands (British)',
                       'wf': 'Wallis and Futuna', 'ws': 'Western Sahara*', 'ye': 'Yemen', 'zm': 'Zambia',
                       'zw': 'Zimbabwe', 'la': 'Lao Peoples Democratic Republic', 'ci': 'COTE DIVOIRE'}

# --- Data Extraction Function (from your original, with minor original pathing fixes) ---
def get_allcom(response):
    page_source = response.text
    result_list = list()
    try:
        # Original parsing logic
        big_dict = json.loads(page_source.replace('/*""*/', ''))
        d_str = big_dict.get('d', '').replace(")]}'", '').strip() # Added .get for safety
        if not d_str:
            return result_list
        
        d_list_outer = json.loads(d_str)
        if not (isinstance(d_list_outer, list) and len(d_list_outer) > 0 and 
                isinstance(d_list_outer[0], list) and len(d_list_outer[0]) > 1 and
                d_list_outer[0][1] is not None):
            return result_list

        company_list_container = d_list_outer[0][1] # This is the list of company wrappers
        if not company_list_container or not isinstance(company_list_container, list):
            return result_list # No companies, or unexpected structure

        for company_wrapper in company_list_container: # company_wrapper should be a list
            if not isinstance(company_wrapper, list) or len(company_wrapper) <= 14 : # Check for the data container
                continue # Skip if data not in expected place
            
            company_data = company_wrapper[14] # The actual data array
            if not isinstance(company_data, list):
                continue

            try:
                temp_dict = dict()
                # Accessing elements safely
                temp_dict['companyName'] = company_data[11] if len(company_data) > 11 and company_data[11] else None
                
                url_info = company_data[7] if len(company_data) > 7 and company_data[7] and isinstance(company_data[7], list) and company_data[7] else None
                temp_dict['url'] = url_info[0] if url_info else None
                if temp_dict['url']:
                    temp_dict['url'] = unquote(temp_dict['url'])

                temp_dict['address'] = company_data[39] if len(company_data) > 39 and company_data[39] else None
                if not temp_dict['address'] and len(company_data) > 18 and company_data[18]:
                    temp_dict['address'] = company_data[18]
                
                phone_val = None
                phone_info_178 = company_data[178] if len(company_data) > 178 and company_data[178] and isinstance(company_data[178], list) and company_data[178] else None
                if phone_info_178 and isinstance(phone_info_178[0], list) and phone_info_178[0]:
                    phone_val = phone_info_178[0][0]
                
                if not phone_val:
                    phone_info_3 = company_data[3] if len(company_data) > 3 and company_data[3] and isinstance(company_data[3], list) and company_data[3] else None
                    if phone_info_3:
                        phone_val = phone_info_3[0]
                temp_dict['phone'] = phone_val

                category_list = company_data[13] if len(company_data) > 13 and company_data[13] and isinstance(company_data[13], list) else None
                temp_dict['category'] = '>'.join(category_list) if category_list else None
                
                temp_dict['countryEn'] = None
                if temp_dict['address']:
                    addr_lower = temp_dict['address'].lower()
                    for google_country_val in google_country_dict.values():
                        if google_country_val.lower() in addr_lower:
                            temp_dict['countryEn'] = google_country_val
                            break
                
                if not temp_dict['countryEn']:
                    addr_info_183 = company_data[183] if len(company_data) > 183 and company_data[183] and isinstance(company_data[183], list) else None
                    if addr_info_183 and len(addr_info_183) > 1 and isinstance(addr_info_183[1], list) and addr_info_183[1] and addr_info_183[-1]: # Checking path to country code
                        country_code_key = addr_info_183[-1].lower() # Assuming last element is country code
                        if country_code_key in country_suffix_dict:
                             temp_dict['countryEn'] = country_suffix_dict[country_code_key]

                temp_dict['city'] = company_data[14] if len(company_data) > 14 and company_data[14] else None
                
                if temp_dict['companyName']: # Only add if company name exists
                    # yield temp_dict # If streaming was intended
                    result_list.append(temp_dict)
            except (IndexError, TypeError) as e_parse:
                # print(f"Error parsing specific company: {e_parse}, Data: {str(company_data)[:100]}")
                continue # Skip this company entry on error
    except json.JSONDecodeError:
        # print(f"JSON Decode Error. Response Preview: {page_source[:200]}")
        pass # Or handle as needed
    except Exception as e:
        # print(f"General error_in_get_allcom: {e}. Response Preview: {page_source[:200]}")
        pass # Or handle as needed
        
    return result_list


# --- Functions to calculate map parameters (from your original) ---
def get_1d(module=1, offset=0.01):
    a = []
    ori = 94618532.08008283
    a.append([2, ori])
    for i_zoom in range(2, 22): # Renamed i to i_zoom
        if i_zoom > 2:
            ori = (ori / 2)
        # else: ori is correct for i_zoom = 2
        if module == 1:
            for j_offset in np.arange(0, 1, offset): # Renamed j to j_offset
                if (i_zoom + j_offset) > 2 and (i_zoom + j_offset) <= 21:
                    a.append([(i_zoom + j_offset), ori - ori * j_offset / 2]) # Original formula
        elif module == 0:
            if [i_zoom, ori] not in a: # To avoid duplicate for i_zoom=2 if already added
                a.append([i_zoom, ori])
    return dict(a)

def get_23d(d2, d3, dis=5775.056889653493):
    # lat_range = [-85.05112877980659, 85.05112877980659] # Informational
    # lon_range = [-180, 180] # Informational

    lat = lat_km2degree(dis / 1000.0) # dis is in meters, convert to km
    lon = lng_km2degree(dis / 1000.0, d3)

    up_lat = d3 + lat
    down_lat = d3 - lat
    left_lon = d2 - lon
    right_lon = d2 + lon

    # Check if new coordinates are within typical map bounds (optional but good practice)
    up = (d2, up_lat) if -85.05112877980659 <= up_lat <= 85.05112877980659 else None
    down = (d2, down_lat) if -85.05112877980659 <= down_lat <= 85.05112877980659 else None
    # Longitude can wrap, so usually no strict check unless needed by the application's logic
    left = (left_lon, d3)
    right = (right_lon, d3)
    
    # Filter out None values if any coordinate went out of bounds and was set to None
    return [coord for coord in [up, down, left, right] if coord is not None]


# --- Main Company Scraping Function with PROXY SUPPORT ---
def get_com(d2_lon, d3_lat, proxies=None): # <<< MODIFIED: Added proxies parameter (defaults to None)
    """
    Crawls Google Maps for company data.
    d2_lon: Longitude
    d3_lat: Latitude
    proxies: Optional dictionary for requests proxies. e.g., {"http": "...", "https": "..."}
    """
    com_num = {}
    d1_dict = get_1d(0)

    for d1_multiple in d1_dict:
        d1 = d1_dict[d1_multiple]
        print('目前倍数%d：' % d1_multiple)
        
        # Original URL and pb string structure
        url_template = 'https://www.google.com/search?tbm=map&authuser=0&hl=en&pb=!4m12!1m3!1d{}!2d{}!3d{}'
        pb_fixed_part = ( # The pb part that doesn't change with pagination, but has one placeholder for page_id
            '!2m3!1f0!2f0!3f0!3m2!1i784!2i644!4f13.1!7i20{}!10b1!12m8!1m1!18b1!2m3!5m1!6e2!20e3!10b1!16b1'
            '!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240'
            '!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3'
            '!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0'
            '!22m5!1s5mKzXrHAJNSXr7wP5u-akAQ!4m1!2i5600!7e81!12e30!24m46!1m12!13m6!2b1!3b1!4b1!6i1!8b1!9b1'
            '!18m4!3b1!4b1!5b1!6b1!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m2!1e3!1e6!24b1'
            '!25b1!26b1!30m1!2b1!36b1!43b1!52b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!26m4!2m3'
            '!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i644!1m6!1m2!1i734!2i0!2m2!1i784!2i644!1m6!1m2'
            '!1i0!2i0!2m2!1i784!2i20!1m6!1m2!1i0!2i624!2m2!1i784!2i644!31b1!34m13!2b1!3b1!4b1!6b1!8m3!1b1'
            '!3b1!4b1!9b1!12b1!14b1!20b1!23b1!37m1!1e81!42b1!46m1!1e2!47m0!49m1!3b1!50m13!1m8!3m6!1u17!2m4'
            '!1m2!17m1!1e2!2z6Led56a7!4BIAE!2e2!3m2!1b1!3b0!59BQ2dBd0Fn!65m0&q=company&tch=1&ech=4'
            '&psi=5mKzXrHAJNSXr7wP5u-akAQ.1588814569168.1' # psi is likely a session/request token
        )
        
        page_offset = 0 # Renamed 'page' for clarity as it's an offset
        all_result_for_zoom = [] # Renamed 'all_result'
        
        while True:
            page_id_str = '!8i%d' % page_offset # Example: !8i0, !8i20, etc.
            headers = {'User-Agent': random.choice(agents)}
            
            # Construct the full URL
            current_base_url = url_template.format(d1, d2_lon, d3_lat)
            current_pb_part = pb_fixed_part.format(page_id_str) # Insert page_id into pb string
            full_url = current_base_url + current_pb_part
            
            try:
                # >>> MODIFIED: Pass proxies to requests.get()
                response = requests.get(full_url, headers=headers, proxies=proxies, timeout=15) # Added timeout
                response.raise_for_status() # Check for HTTP errors
                
                # Assuming get_allcom always returns a list (even if empty)
                # and doesn't raise exceptions that aren't caught internally.
                results_from_page = get_allcom(response)
                
                if not results_from_page: # No more results on this page
                    break
                
                all_result_for_zoom.extend(results_from_page)
                page_offset += 20 # Standard pagination step
            except requests.exceptions.RequestException as e:
                print(f"Request error for {full_url[:100]}...: {e}")
                break # Exit this while loop (for this zoom level) on request error
            except Exception as e_general:
                print(f"Unexpected error during request for {full_url[:100]}...: {e_general}")
                break # Exit this while loop on other errors


        print(f"For d1 (zoom key) {d1_multiple}, 1d value {d1:.2f}, found {len(all_result_for_zoom)} companies.")
        com_num[d1_multiple] = len(all_result_for_zoom)

    if not com_num: # No data collected at all
        print("No company data collected for any zoom level. Cannot proceed with this branch.")
        return

    # Original logic for choosing the next step
    # This part is sensitive to the keys and values in com_num (zoom levels 2-21)
    # The slice [12:19] assumes com_num.keys() are sorted and correspond to zoom levels.
    # get_1d(0) produces keys: 2, 3, ..., 21.
    # list(com_num.values())[12:19] would correspond to values for keys 14 through 20.
    # list(com_num.keys())[12:19] would correspond to keys 14 through 20.
    
    values_list = list(com_num.values())
    keys_list = list(com_num.keys()) # These are zoom levels e.g. 2, 3, ..., 21

    # Slicing directly like this from list(dict.values()) or list(dict.keys())
    # assumes Python 3.7+ where dict insertion order is preserved,
    # or that d1_dict was iterated in a specific sorted order for com_num population.
    # For robustness, it's better to filter keys and then get values.
    
    # Original slicing indices (12 to 18, since 19 is exclusive)
    # If keys_list is [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21] (20 elements)
    # Keys at index 12 to 18 are: 14,15,16,17,18,19,20
    
    target_keys_for_best_zoom = [k for k in keys_list if 14 <= k <= 20] # Example relevant zoom levels
    
    max_num_in_target = 0
    if target_keys_for_best_zoom:
        values_in_target = [com_num[k] for k in target_keys_for_best_zoom if k in com_num]
        if values_in_target:
            max_num_in_target = max(values_in_target)
    
    new_list_coords = []
    if max_num_in_target == 0:
        new_list_coords = get_23d(d2_lon, d3_lat) # Default distance
        print(f'没有最优倍数 (max_num_in_target is 0), 取默认值. Coords: {new_list_coords}')
    else:
        best_d1_multiples_for_max = [
            k for k in target_keys_for_best_zoom if k in com_num and com_num[k] == max_num_in_target
        ]
        if not best_d1_multiples_for_max: # Fallback if something went wrong
             best_d1_multiples_for_max = [k for k in keys_list if k in com_num and com_num[k] == max_num_in_target]


        if best_d1_multiples_for_max: # Should have at least one
            chosen_best_d1_multiple = best_d1_multiples_for_max[0] # Take the first one
            print(f'最优倍数为： {chosen_best_d1_multiple} (from {best_d1_multiples_for_max}) with {max_num_in_target} companies.')
            distance_for_step = d1_dict[chosen_best_d1_multiple] # This is the '1d' value
            new_list_coords = get_23d(d2_lon, d3_lat, dis=distance_for_step)
        else: # Should not happen if max_num_in_target > 0
             new_list_coords = get_23d(d2_lon, d3_lat) # Default distance
             print(f'逻辑错误: max_num > 0 但未找到 best_d1_multiple. 取默认值. Coords: {new_list_coords}')


    print(f'移动后的四个坐标 (for {d2_lon},{d3_lat}): {new_list_coords}')
    for i_coord in new_list_coords: # Renamed 'i' to 'i_coord'
        if i_coord: # i_coord is a tuple (lon, lat)
            # >>> MODIFIED: Pass proxies in recursive call
            get_com(i_coord[0], i_coord[1], proxies=proxies)


if __name__ == '__main__':
    # d = 20037508.3427892 # Original comment
    # 起始点
    d3_start_lat = 22.3527234
    d2_start_lon = 114.1277

    # Define your proxies here IF you want to hardcode for testing
    # For committed code, it's better to pass them from an external source or environment variables
    # Example proxy dictionary (replace with your actual proxy if testing)
    test_proxies = {
        "http": "http://kmzhpbnt-rotate:fmce7ro1djvc@p.webshare.io:80/",
        "https": "http://kmzhpbnt-rotate:fmce7ro1djvc@p.webshare.io:80/" # Or your HTTPS specific proxy
    }
    
    print(f"Starting crawler from lat: {d3_start_lat}, lon: {d2_start_lon}")
    
    # To run WITH proxies:
    # get_com(d2_start_lon, d3_start_lat, proxies=test_proxies)
    
    # To run WITHOUT proxies (original behavior):
    get_com(d2_start_lon, d3_start_lat, proxies=None) # Or simply get_com(d2_start_lon, d3_start_lat)
    # For your specific request to use the Webshare proxy:
    # get_com(d2_start_lon, d3_start_lat, proxies=test_proxies)


    print("Crawler finished.")
