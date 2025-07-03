import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests

def get_truecaller_info(phone):
    headers = {
        "User-Agent": "Truecaller/11.75.5 (Android;10)",
    }
    params = {
        "number": phone,
        "countryCode": "IN"  # Change for other countries if needed
    }
    try:
        response = requests.get("https://search5-noneu.truecaller.com/v2/search", headers=headers, params=params)
        data = response.json()
        name = data.get("data", {}).get("name", "Unknown")
        city = data.get("data", {}).get("addresses", [{}])[0].get("city", "Unknown")
        return name, city
    except Exception as e:
        print("❌ Error contacting Truecaller API:", e)
        return "Unknown", "Unknown"

# Input number
number = input("Enter phone number with country code (e.g. +917012345678): ")

try:
    parsed = phonenumbers.parse(number)
    if not phonenumbers.is_valid_number(parsed):
        print("❌ Invalid number")
    else:
        region = geocoder.description_for_number(parsed, "en")
        service_provider = carrier.name_for_number(parsed, "en")
        time_zones = timezone.time_zones_for_number(parsed)

        name, city = get_truecaller_info(number)

        print("\n--- Phone Number Full Details ---")
        print(f"📞 Number         : {number}")
        print(f"👤 Name           : {name}")
        print(f"🌍 Region         : {region}")
        print(f"🏙️ City (API)     : {city}")
        print(f"📡 Carrier        : {service_provider}")
        print(f"🕒 Time Zone(s)   : {', '.join(time_zones)}")

except phonenumbers.NumberParseException:
    print("❌ Invalid input format.")
