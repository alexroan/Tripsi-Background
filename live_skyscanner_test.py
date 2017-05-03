from skyscanner.skyscanner import Flights
import os

live_api_key = os.environ['SKYSCANNER_LIVE_KEY']
flights_service = Flights(live_api_key)
result = flights_service.get_result(
    country='UK',
    currency='GBP',
    locale='en-GB',
    originplace='CWL-sky',
    destinationplace='DUB-sky',
    outbounddate='2017-05-19',
    inbounddate='2017-05-21',
    adults=1,
	groupPricing=True,
	outbounddepartstarttime="16:00",
	outbounddepartendtime="23:30",
	inbounddepartstarttime="10:00",
	inbounddepartendtime="23:30").parsed
print(result)