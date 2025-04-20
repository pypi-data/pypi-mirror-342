from flask import request
from geopy.geocoders import Nominatim
from user_agents import parse
import requests
import logging

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
        if location:
            # Split the address and get the last part (country)
            address_parts = location.address.split(',')
            country = address_parts[-1].strip() if address_parts else "Unknown"
            city = address_parts[0].strip() if address_parts else "Unknown"
            
            # Truncate country name if it's too long
            if len(country) > 100:
                country = country[:97] + "..."
        else:
            country = "Unknown"
            city = "Unknown"
    except Exception as e:
        logging.error(f"Error getting location info: {str(e)}")
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