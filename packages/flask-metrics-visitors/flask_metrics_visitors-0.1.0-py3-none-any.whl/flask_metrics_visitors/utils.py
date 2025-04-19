from flask import request
from geopy.geocoders import Nominatim
from user_agents import parse
import requests

def get_visitor_info(request):
    """Get information about the visitor"""
    ip = request.remote_addr
    user_agent = parse(request.user_agent.string)
    
    # Get location information
    geolocator = Nominatim(user_agent="flask_metrics_visitors")
    try:
        # In production, you should use a proper IP geolocation service
        # This is just a simple example
        location = geolocator.geocode(ip)
        country = location.address.split(',')[-1].strip() if location else "Unknown"
        city = location.address.split(',')[0].strip() if location else "Unknown"
    except:
        country = "Unknown"
        city = "Unknown"
    
    return {
        'ip': ip,
        'country': country,
        'city': city,
        'browser': user_agent.browser.family,
        'os': user_agent.os.family,
        'device': user_agent.device.family
    } 