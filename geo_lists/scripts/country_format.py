import os
import sys


PATH_SEPARATOR = '\\' if sys.platform == 'win32' else '/'
HOME_DIR: str = '/'.join(os.path.realpath(__file__).split(PATH_SEPARATOR)[:-2])

GEO_LIST = {
    'NONE', 'RFC1918',
    'AFGHANISTAN', 'ALAND_ISLANDS', 'ALBANIA', 'ALGERIA', 'AMERICAN_SAMOA', 'ANDORRA', 'ANGOLA', 'ANGUILLA',
    'ANTARCTICA', 'ANTIGUA_AND_BARBUDA', 'ARGENTINA', 'ARMENIA', 'ARUBA', 'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN',
    'BAHAMAS', 'BAHRAIN', 'BANGLADESH', 'BARBADOS', 'BELARUS', 'BELGIUM', 'BELIZE', 'BENIN', 'BERMUDA', 'BHUTAN',
    'BOLIVIA', 'BONAIRE', 'BOSNIA_AND_HERZEGOVINA', 'BOTSWANA', 'BOUVET_ISLAND', 'BRAZIL',
    'BRITISH_INDIAN_OCEAN_TERRITORY', 'BRITISH_VIRGIN_ISLANDS', 'BRUNEI_DARUSSALAM', 'BULGARIA', 'BURKINA_FASO',
    'BURUNDI', 'CABO_VERDE', 'CAMBODIA', 'CAMEROON', 'CANADA', 'CAYMAN_ISLANDS', 'CENTRAL_AFRICAN_REPUBLIC', 'CHAD',
    'CHILE', 'CHINA', 'CHRISTMAS_ISLAND', 'COCOS_ISLANDS', 'COLOMBIA', 'COMOROS', 'CONGO', 'COTE_D_IVOIRE', 'CURACAO',
    'COOK_ISLANDS', 'COSTA_RICA', 'CROATIA', 'CUBA', 'CYPRUS', 'CZECHIA', 'DENMARK', 'DJIBOUTI', 'DOMINICA',
    'DOMINICAN_REPUBLIC', 'ECUADOR', 'EGYPT', 'EL_SALVADOR', 'EQUATORIAL_GUINEA', 'ERITREA', 'ESTONIA', 'ESWATINI',
    'ETHIOPIA', 'FALKLAND_ISLANDS', 'FAROE_ISLANDS', 'FIJI', 'FINLAND', 'FRANCE', 'FRENCH_GUIANA', 'FRENCH_POLYNESIA',
    'FRENCH_SOUTHERN_TERRITORIES', 'GABON', 'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GIBRALTAR', 'GREECE', 'GREENLAND',
    'GRENADA', 'GUADELOUPE', 'GUAM', 'GUATEMALA', 'GUERNSEY', 'GUINEA', 'GUINEA_BISSAU', 'GUYANA', 'HAITI', 'HOLY_SEE',
    'HONDURAS', 'HONG_KONG', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 'IRAN', 'IRAQ', 'IRELAND', 'ISLE_OF_MAN',
    'ISRAEL', 'ITALY', 'JAMAICA', 'JAPAN', 'JERSEY', 'JORDAN', 'KAZAKHSTAN', 'KENYA', 'KIRIBATI', 'KUWAIT',
    'KYRGYZSTAN', 'LAOS', 'LATVIA', 'LEBANON', 'LESOTHO', 'LIBERIA', 'LIBYA', 'LIECHTENSTEIN', 'LITHUANIA',
    'LUXEMBOURG', 'MACAO', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 'MALDIVES', 'MALI', 'MALTA', 'MARSHALL_ISLANDS',
    'MARTINIQUE', 'MAURITANIA', 'MAURITIUS', 'MAYOTTE', 'MEXICO', 'MICRONESIA', 'MOLDOVA', 'MONACO', 'MONGOLIA',
    'MONTENEGRO', 'MONTSERRAT', 'MOROCCO', 'MOZAMBIQUE', 'MYANMAR', 'NAMIBIA', 'NAURU', 'NEPAL', 'NETHERLANDS',
    'NEW_CALEDONIA', 'NEW_ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA', 'NIUE', 'NORFOLK_ISLAND', 'NORTH_KOREA',
    'NORTH_MACEDONIA', 'NORTHERN_MARIANA_ISLANDS', 'NORWAY', 'OMAN', 'PAKISTAN', 'PALAU', 'PALESTINE', 'PANAMA',
    'PAPUA_NEW_GUINEA', 'PARAGUAY', 'PERU', 'PHILIPPINES', 'POLAND', 'PORTUGAL', 'PUERTO_RICO', 'QATAR', 'REUNION',
    'ROMANIA', 'RUSSIAN_FEDERATION', 'RWANDA', 'SAINT_BARTHELEMY', 'SAINT_HELENA', 'SAINT_KITTS_AND_NEVIS',
    'SAINT_LUCIA', 'SAINT_MARTIN_DUTCH', 'SAINT_MARTIN_FRENCH', 'SAINT_PIERRE_AND_MIQUELON',
    'SAINT_VINCENT_AND_THE_GRENADINES', 'SAMOA', 'SAN_MARINO', 'SAO_TOME_AND_PRINCIPE', 'SAUDI_ARABIA', 'SENEGAL',
    'SERBIA', 'SEYCHELLES', 'SIERRA_LEONE', 'SINGAPORE', 'SLOVAKIA', 'SLOVENIA', 'SOLOMON_ISLANDS', 'SOMALIA',
    'SOUTH_AFRICA', 'SOUTH_GEORGIA_AND_THE_SOUTH_SANDWICH_ISLANDS', 'SOUTH_KOREA', 'SOUTH_SUDAN', 'SPAIN', 'SRI_LANKA',
    'SUDAN', 'SURINAME', 'SWEDEN', 'SWITZERLAND', 'SYRIA', 'TAIWAN', 'TAJIKISTAN', 'TANZANIA', 'THAILAND',
    'TIMOR_LESTE', 'TOGO', 'TOKELAU', 'TONGA', 'TRINIDAD_AND_TOBAGO', 'TUNISIA', 'TURKEY', 'TURKMENISTAN',
    'TURKS_AND_CAICOS_ISLANDS', 'TUVALU', 'UGANDA', 'UKRAINE', 'UNITED_ARAB_EMIRATES', 'UNITED_KINGDOM',
    'UNITED_STATES', 'URUGUAY', 'US_MINOR_OUTLYING_ISLANDS', 'US_VIRGIN_ISLANDS', 'UZBEKISTAN', 'VANUATU', 'VENEZUELA',
    'VIETNAM', 'WALLIS_AND_FUTUNA', 'WESTERN_SAHARA', 'YEMEN', 'ZAMBIA', 'ZIMBABWE'
}

def find_invalid_names():

    invalid_names = set()

    with open(f'{HOME_DIR}/collection.geo') as f:

        for line in f:
            line = line.strip().split(',', 2)

            country_name = line[2].upper()

            if country_name not in GEO_LIST and country_name not in invalid_names:
                invalid_names.add(country_name.lower())

    return sorted(invalid_names)


if (__name__ == '__main__'):
    ret = find_invalid_names()

    print(ret)
