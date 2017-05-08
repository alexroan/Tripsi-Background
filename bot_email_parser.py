from lxml import etree

class BotEmailParser:

	def __init__(self, filename):
		self.filename = filename

	def parse_currency(self, currency):
		if currency == 'GBP':
			return '£'
		elif currency == 'EUR':
			return '€'
		elif currency == 'USD' or currency == 'AUD':
			return '$'
		else:
			return None

	def construct_email(self, origin, currency, advenchas, api_key_16):
		currency_symbol = self.parse_currency(currency)

		parser = etree.HTMLParser()
		tree = etree.parse(self.filename, parser)
		#main-title
		find = etree.XPath("//h1[@id = 'main-title']")
		main_title = find(tree)[0]
		main_title.text = "Deals From %s" % origin

		#details of each offer
		count = 1
		for advencha in advenchas:
			if count == 4:
				break
			xp = "//strong[@id = 'location-%s-title']" % str(count)
			find = etree.XPath(xp)
			location_title = find(tree)[0]
			location_title.text = advencha.return_place
			xp = "//p[@id = 'location-%s-text']" % str(count)
			find = etree.XPath(xp)
			location_text = find(tree)[0]
			#TODO display the dates of the advencha
			location_text.text = "%s to %s" % (str(advencha.departure_date).split('T')[0], str(advencha.return_date).split('T')[0])
			xp = "//a[@id = 'location-%s-button']" % str(count)
			find = etree.XPath(xp)
			location_button = find(tree)[0]
			url = "http://partners.api.skyscanner.net/apiservices/referral/v1.0/GB/%s/en-GB/%s/%s/%s/%s?apiKey=%s" % (currency, advencha.departure_iata, advencha.return_iata, str(advencha.departure_date.split('T')[0]), str(advencha.return_date.split('T')[0]), api_key_16)
			location_button.attrib['href'] = url
			location_button.text = "%s%s" % (currency_symbol, str(advencha.price))
			count = count + 1
		
		return etree.tostring(tree, encoding="ascii", pretty_print=True, method="html")

