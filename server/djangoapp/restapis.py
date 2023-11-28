import requests
import json
from .models import CarDealer, DealerReview
# import related models here
from requests.auth import HTTPBasicAuth
import sys
import logging
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


logger = logging.getLogger(__name__)




# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        except:
            print("An error occurred while making GET request. ")
    else:
        # No authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            print("An error occurred while making GET request. ")

    # Retrieving the response status code and content
    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)

    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(f"POST to {url}")
    try:
        print(json_payload)
        response = requests.post(url, params=kwargs, json=json_payload)
    except Exception as e:
        print("An error occurred while making POST request. ")
        print(e)
    status_code = response.status_code
    print(f"With status {status_code}")
    
    return response



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = post_request(url, {"params": {}}, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result.json()
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = post_request(url, {"params" : {"method" : "get", "dealerId" : dealerId}})
    if json_result:
        reviews = json_result.json()
        for review in reviews['data']:
            review_obj = DealerReview(dealership=review['dealership'], name=review['name'], purchase=review['purchase'],
                                      review=review['review'], purchase_date=review['purchase_date'], car_make=review['car_make'],
                                      car_model=review['car_model'], car_year=review['car_year'], id=review['review_id'])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerReview):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/7e5260a5-a847-48b0-a95d-26353aafac5b"
    api_key = "CJlCvXyL7cwPc0g8L1Fhjpiyy2IXXO6YY6z7TXBJELjy"
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1('2022-04-07', authenticator=authenticator)
    nlu.set_service_url(url)

    try:
        response = nlu.analyze(text=dealerReview, features=Features(sentiment=SentimentOptions())).get_result()
        sentiment_response = response['sentiment']['document']['label']
    except:
        sentiment_response = "neutral"
    
    return sentiment_response
