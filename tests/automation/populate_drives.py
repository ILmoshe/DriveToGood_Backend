"""A file for populating our db with drives via csv file"""

CURRENT_VERSION = "ver2.json"

from typing import Optional
from enum import Enum
import json
from random import choice
import datetime

from pydantic import BaseModel
from random_object_id import generate
from app.core.helpers.util import random_room

CITY_LIST = [
    {
        "city": "Jerusalem",
        "lat": "31.7833",
        "lng": "35.2167",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "primary",
        "population": "919438",
        "population_proper": "919438"
    },
    {
        "city": "Tel Aviv-Yafo",
        "lat": "32.0800",
        "lng": "34.7800",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "admin",
        "population": "451523",
        "population_proper": "451523"
    },
    {
        "city": "Haifa",
        "lat": "32.8000",
        "lng": "34.9833",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "admin",
        "population": "281087",
        "population_proper": "281087"
    },
    {
        "city": "Rishon LeẔiyyon",
        "lat": "31.9500",
        "lng": "34.8000",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "249860",
        "population_proper": "249860"
    },
    {
        "city": "Petaẖ Tiqwa",
        "lat": "32.0833",
        "lng": "34.8833",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "236169",
        "population_proper": "236169"
    },
    {
        "city": "Ashdod",
        "lat": "31.7978",
        "lng": "34.6503",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "220174",
        "population_proper": "220174"
    },
    {
        "city": "Netanya",
        "lat": "32.3328",
        "lng": "34.8600",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "217244",
        "population_proper": "217244"
    },
    {
        "city": "Beersheba",
        "lat": "31.2589",
        "lng": "34.7978",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "admin",
        "population": "209000",
        "population_proper": "209000"
    },
    {
        "city": "Bené Beraq",
        "lat": "32.0807",
        "lng": "34.8338",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "193774",
        "population_proper": "193774"
    },
    {
        "city": "Holon",
        "lat": "32.0167",
        "lng": "34.7667",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "188834",
        "population_proper": "188834"
    },
    {
        "city": "Ramat Gan",
        "lat": "32.0700",
        "lng": "34.8235",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "152596",
        "population_proper": "152596"
    },
    {
        "city": "Ashqelon",
        "lat": "31.6658",
        "lng": "34.5664",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "134454",
        "population_proper": "134454"
    },
    {
        "city": "Reẖovot",
        "lat": "31.8914",
        "lng": "34.8078",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "132671",
        "population_proper": "132671"
    },
    {
        "city": "Bat Yam",
        "lat": "32.0231",
        "lng": "34.7503",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "128800",
        "population_proper": "128800"
    },
    {
        "city": "Bet Shemesh",
        "lat": "31.7514",
        "lng": "34.9886",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Jerusalem",
        "capital": "",
        "population": "114371",
        "population_proper": "114371"
    },
    {
        "city": "Kefar Sava",
        "lat": "32.1858",
        "lng": "34.9077",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "100800",
        "population_proper": "100800"
    },
    {
        "city": "Herẕliyya",
        "lat": "32.1556",
        "lng": "34.8422",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "93989",
        "population_proper": "93989"
    },
    {
        "city": "Hadera",
        "lat": "32.4500",
        "lng": "34.9167",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "",
        "population": "91707",
        "population_proper": "91707"
    },
    {
        "city": "Modi‘in Makkabbim Re‘ut",
        "lat": "31.9339",
        "lng": "34.9856",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "90013",
        "population_proper": "90013"
    },
    {
        "city": "Nazareth",
        "lat": "32.7021",
        "lng": "35.2978",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "admin",
        "population": "83400",
        "population_proper": "83400"
    },
    {
        "city": "Lod",
        "lat": "31.9500",
        "lng": "34.9000",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "75700",
        "population_proper": "75700"
    },
    {
        "city": "Ramla",
        "lat": "31.9318",
        "lng": "34.8736",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "admin",
        "population": "75500",
        "population_proper": "75500"
    },
    {
        "city": "Ra‘ananna",
        "lat": "32.1833",
        "lng": "34.8667",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "74000",
        "population_proper": "74000"
    },
    {
        "city": "Rahat",
        "lat": "31.3925",
        "lng": "34.7544",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "64462",
        "population_proper": "64462"
    },
    {
        "city": "Nahariyya",
        "lat": "33.0036",
        "lng": "35.0925",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "60000",
        "population_proper": "60000"
    },
    {
        "city": "Givatayim",
        "lat": "32.0697",
        "lng": "34.8117",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "59518",
        "population_proper": "59518"
    },
    {
        "city": "Hod HaSharon",
        "lat": "32.1500",
        "lng": "34.8833",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "56659",
        "population_proper": "56659"
    },
    {
        "city": "Rosh Ha‘Ayin",
        "lat": "32.0833",
        "lng": "34.9500",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "56300",
        "population_proper": "56300"
    },
    {
        "city": "Qiryat Ata",
        "lat": "32.8000",
        "lng": "35.1000",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "",
        "population": "55464",
        "population_proper": "55464"
    },
    {
        "city": "Umm el Faḥm",
        "lat": "32.5158",
        "lng": "35.1525",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "",
        "population": "55300",
        "population_proper": "55300"
    },
    {
        "city": "Qiryat Gat",
        "lat": "31.6061",
        "lng": "34.7717",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "55000",
        "population_proper": "55000"
    },
    {
        "city": "Eilat",
        "lat": "29.5500",
        "lng": "34.9500",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "51935",
        "population_proper": "51935"
    },
    {
        "city": "Nes Ẕiyyona",
        "lat": "31.9333",
        "lng": "34.8000",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "50200",
        "population_proper": "50200"
    },
    {
        "city": "‘Akko",
        "lat": "32.9261",
        "lng": "35.0839",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "47675",
        "population_proper": "47675"
    },
    {
        "city": "El‘ad",
        "lat": "32.0523",
        "lng": "34.9512",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "46896",
        "population_proper": "46896"
    },
    {
        "city": "Ramat HaSharon",
        "lat": "32.1461",
        "lng": "34.8394",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "46700",
        "population_proper": "46700"
    },
    {
        "city": "Karmiel",
        "lat": "32.9000",
        "lng": "35.2833",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "45300",
        "population_proper": "45300"
    },
    {
        "city": "Afula",
        "lat": "32.6078",
        "lng": "35.2897",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "44930",
        "population_proper": "44930"
    },
    {
        "city": "Tiberias",
        "lat": "32.7897",
        "lng": "35.5247",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "44200",
        "population_proper": "44200"
    },
    {
        "city": "Eṭ Ṭaiyiba",
        "lat": "32.2667",
        "lng": "35.0000",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "43100",
        "population_proper": "43100"
    },
    {
        "city": "Qiryat Yam",
        "lat": "32.8331",
        "lng": "35.0664",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "",
        "population": "40700",
        "population_proper": "40700"
    },
    {
        "city": "Qiryat Moẕqin",
        "lat": "32.8381",
        "lng": "35.0794",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "",
        "population": "40160",
        "population_proper": "40160"
    },
    {
        "city": "Qiryat Bialik",
        "lat": "32.8331",
        "lng": "35.0664",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Haifa",
        "capital": "",
        "population": "39900",
        "population_proper": "39900"
    },
    {
        "city": "Qiryat Ono",
        "lat": "32.0636",
        "lng": "34.8553",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "37791",
        "population_proper": "37791"
    },
    {
        "city": "Or Yehuda",
        "lat": "32.0333",
        "lng": "34.8500",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Tel Aviv",
        "capital": "",
        "population": "36706",
        "population_proper": "36706"
    },
    {
        "city": "Ma‘alot Tarshīḥā",
        "lat": "33.0167",
        "lng": "35.2708",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "36000",
        "population_proper": "36000"
    },
    {
        "city": "Ẕefat",
        "lat": "32.9658",
        "lng": "35.4983",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "35700",
        "population_proper": "35700"
    },
    {
        "city": "Dimona",
        "lat": "31.0700",
        "lng": "35.0300",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "34135",
        "population_proper": "34135"
    },
    {
        "city": "Tamra",
        "lat": "32.8511",
        "lng": "35.2071",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "34000",
        "population_proper": "34000"
    },
    {
        "city": "Netivot",
        "lat": "31.4167",
        "lng": "34.5833",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Southern",
        "capital": "",
        "population": "31314",
        "population_proper": "31314"
    },
    {
        "city": "Sakhnīn",
        "lat": "32.8667",
        "lng": "35.3000",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "",
        "population": "31100",
        "population_proper": "31100"
    },
    {
        "city": "Yehud",
        "lat": "32.0333",
        "lng": "34.8833",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Central",
        "capital": "",
        "population": "29146",
        "population_proper": "29146"
    },
    {
        "city": "Al Buţayḩah",
        "lat": "32.9087",
        "lng": "35.6320",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "minor",
        "population": "",
        "population_proper": ""
    },
    {
        "city": "Al Khushnīyah",
        "lat": "32.9994",
        "lng": "35.8108",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "minor",
        "population": "",
        "population_proper": ""
    },
    {
        "city": "Fīq",
        "lat": "32.7793",
        "lng": "35.7003",
        "country": "Israel",
        "iso2": "IL",
        "admin_name": "Northern",
        "capital": "minor",
        "population": "",
        "population_proper": ""
    }
]


class DriveType(str, Enum):
    transporting_patient = "transporting_patient"
    hospital = "hospital"
    food_distribution = "food_distribution"
    roadside_assistance = "roadside_assistance"
    transportation_of_medical_equipment = "transportation_of_medical_equipment"


class Status(str, Enum):
    pending = "pending"
    occupied = "occupied"
    completed = "completed"


class LocationDD(BaseModel):
    """It is not working with INDEXED idk why"""
    type: str = "Point"
    coordinates: list[float, float]


BODY = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor "
                           "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
                           "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
                           "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla "
                           "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia "
                           "deserunt mollit anim id est laborum."""


def populate_drives(file_name: str, quantity: int = 20):
    data = []
    with open(file_name, mode='w', encoding="utf-8") as f:
        for _ in range(quantity):
            id = str(generate())
            id_user = str(generate())

            ver = choice(list(DriveType))

            city = choice(CITY_LIST)
            lat = float(city["lat"])
            lng = float(city["lng"])

            dst_city = choice(CITY_LIST)
            dst_lat = float(dst_city["lat"])
            dst_lng = float(dst_city["lng"])

            status = choice(list(Status))
            room_id = random_room()

            row = {"_id": id, "id_user": id_user, "ver": ver,
                   "location": {"type": "Point", "coordinates": [lng, lat]},
                   "destination": {"type": "Point", "coordinates": [dst_lng, dst_lat]},
                   "body": BODY,
                   "status": status,
                   "header": "short ride carry some bull shit", "room_id": room_id,
                   "date": datetime.datetime.now()}
            data.append(row)

        json.dump(data, f, ensure_ascii=False, indent=4, default=str)


populate_drives(rf"C:\Users\AKA_8700K\Desktop\drive pop\{CURRENT_VERSION}", 30)
