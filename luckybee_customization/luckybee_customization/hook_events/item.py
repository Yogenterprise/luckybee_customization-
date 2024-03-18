import json
import datetime
import keepa
import frappe
from frappe import _
import re
from frappe.utils import today



def update_item(doc, event):
	accesskey = '4i9vbmksc3d9o67p6fd3s9aitdaaer17c604f3qrh93auu67fnh6pfucqvqltmjm'
	api = keepa.Keepa(accesskey)
	ASIN = [row.custom_asin for row in doc.items if row.custom_asin]
	if ASIN:
		try:
			products = api.query(ASIN, stats=30, rating=True, update=0, domain="IN", history=1)
			for i in range(len(ASIN)):
				item = frappe.get_doc("Item", {"custom_asin_no": ASIN[i]})
				if item:
					item.custom_amzon_item_name = products[i]["title"]
					item.title = products[i]["title"]

					if products[i]["imagesCSV"]:
						item.image = "https://images-na.ssl-images-amazon.com/images/I/" + products[i]["imagesCSV"].split(',')[0]
					item.manufacturer = products[i]["manufacturer"]
					if products[i]['listedSince']:
						epoch_time = (products[i]["listedSince"]+ 21564000) * 60000
						listed_since_date = datetime.datetime.utcfromtimestamp(epoch_time / 1000)
						item.listed_since = listed_since_date.strftime("%Y-%m-%d")
					sales_ranks = products[i]["salesRanks"]
					sales_rank_reference = products[i]["salesRankReference"]
					if sales_ranks and sales_rank_reference:
						if str(sales_rank_reference) in sales_ranks:
							sales_rank_history = sales_ranks[str(sales_rank_reference)]
							item.sales_rank = str(sales_rank_history[-1])
					item.sales_rank_ref = products[i]['salesRankReference']
					item.amazon_url = f'https://www.amazon.in/dp/{ASIN[i]}'
					if len(products[i]['csv']) > 0:
						if len(products[i]['csv']) >= 17:
							if products[i]['csv'][17]:
								item.reviews_count = products[i]['csv'][17][-1]
						if len(products[i]['csv']) >= 16:
							if products[i]['csv'][16]:
								item.reviews_rating = str(products[i]['csv'][16][-1]/10)
					item.parent_asin = products[i]["parentAsin"]
					category_tree = []
					category_tree_dict = {}
					if products[i].get('categoryTree'):
						category_tree = [i.get("name") for i in products[i].get('categoryTree')]
						category_tree_dict = {i["catId"]:i["name"] for i in products[i]['categoryTree']}

					if category_tree:
						item.category_sub = category_tree[-1]
						item.categories_tree = ", ".join(category_tree)
					if category_tree_dict:
						item.category_root = category_tree_dict.get(products[0].get('rootCategory'))
					
					# item.ean =  re.findall('[0-9]+', json.dumps(products[i]['eanList'][0]))[0] if products[i]['eanList'] is not None else ''
					item.ean =  products[i]['eanList'][0] if products[i]['eanList'] else ''

					item.upc = json.dumps(products[i]['upcList'])
					item.launchpad = products[i]['launchpad']  # currently a data field, should be checkbox
					item.partnumber = products[i]['partNumber']
					frequently_bought_together = products[i]['frequentlyBoughtTogether']
					if isinstance(frequently_bought_together, (list, tuple)):
						item.freq_brought_together = ", ".join(frequently_bought_together)
					else:
						item.freq_brought_together = ""
					variations = products[i]['variations']
					if variations:
						v = [row.get('asin') for row in variations]
						if v:
							item.variation_asins = ", ".join(v)
					asin_attributes = [row.get('attributes') for row in variations if row.get('asin')==ASIN[i] and row.get('attributes')]
					if asin_attributes:
						attr_dict = [row for row in asin_attributes[0]]
						if attr_dict:
							item.variation_attributes = f"{attr_dict[0].get('dimension')}: {attr_dict[0].get('value')}"
					item.product_group = products[i]['productGroup']
					item.number_of_items = products[i]['numberOfItems']
					item.package_height = str(products[i]['packageHeight']/10)
					item.package_length = str(products[i]['packageLength']/10)
					item.package_width = str(products[i]['packageWidth']/10)
					item.package_weight = products[i]['packageWeight']
					item.package_quantity = products[i]['packageQuantity']
					pkg_dimension = str(products[i]['packageLength']/10 * products[i]['packageWidth']/10 * products[i]['packageHeight']/10)
					if products[i]['packageHeight']/10 > 0 and products[i]['packageLength']/10 > 0 and products[i]['packageWidth']/10 > 0:
						item.package_dimention = f"{item.package_length} x {item.package_width} x {item.package_height} cm (= {pkg_dimension}) cm\u00b3"
					item.model = products[i]['model']
					item.length_length = str(products[i]['itemLength']/10)
					item.length_breadth = str(products[i]['itemWidth']/10)
					item.length_height = str(products[i]['itemHeight']/10)
					item.length_weight = products[i]['itemWeight']
					item_dimension = str(products[i]['itemLength']/10 * products[i]['itemWidth']/10 * products[i]['itemHeight']/10)
					if products[i]['itemLength']/10 > 0 and products[i]['itemWidth']/10 > 0 and products[i]['itemHeight']/10 > 0:
						item.length_dimension = f"{item.length_length} x {item.length_breadth} x {item.length_height} cm (= {item_dimension} cm\u00b3)"
					item.size = products[i]['size']
					item.color = products[i]['color']
					item.desc_feature = products[i]["description"]
					if products[0]['features'] and len(products[0]['features']) >= 5:
						item.desc_feature_1 = products[0]['features'][0]
						item.desc_feature_2 = products[0]['features'][1]
						item.desc_feature_3 = products[0]['features'][2]
						item.desc_feature_4 = products[0]['features'][3]
						item.desc_feature_5 = products[0]['features'][4]
					stats_parsed = products[i].get("stats_parsed")
					if stats_parsed:
						current = stats_parsed.get("current")
						avg30 = stats_parsed.get("avg30")
						avg90 = stats_parsed.get("avg90")
						avg180 = stats_parsed.get("avg180")
						lowest = stats_parsed.get("min")
						highest = stats_parsed.get("max")

						if current:
							item.current_price = current.get("SALES")
							item.last_price = current.get("LISTPRICE")
							item.new_current = current.get("NEW")
						if avg30:
							item.custom_sales_30days = avg30.get("SALES")
							item.list_price_30days = avg30.get("LISTPRICE")
							item.new_30days = avg30.get("NEW")
						if avg90:
							item.custom_sales_90days = avg90.get("SALES")
							item.list_price_90days = avg90.get("LISTPRICE")
							item.new_90days = avg90.get("NEW")
						if avg180:
							item.custom_sales_180days = stats_parsed.get("avg180").get("SALES")
							item.list_price_180days = stats_parsed.get("avg180").get("LISTPRICE")
							item.new_180days = stats_parsed.get("avg180").get("NEW")
						if lowest:
							new_lowest = lowest.get("NEW")
							if new_lowest and len(new_lowest)==2:
								item.new_lowest = new_lowest[1]
							lowest_listprice = lowest.get("LISTPRICE")
							if lowest_listprice and len(lowest_listprice)==2:
								item.list_price_lowest = lowest_listprice[1]
						if highest:
							new_highest = lowest.get("NEW")
							if new_highest and len(new_highest)==2:
								item.new_highest = new_highest[1]
							highest_listprice = highest.get("LISTPRICE")
							if highest_listprice and len(highest_listprice)==2:
								item.list_price_highest = highest_listprice[1]

					item.save()
					# frappe.db.set_value("Item", item.name, "title", products[i]['title'])

		except Exception as e:
			frappe.throw(_("Found invalid ASIN"))
	

def sync_keepa_item(doc, event):
	accesskey = '4i9vbmksc3d9o67p6fd3s9aitdaaer17c604f3qrh93auu67fnh6pfucqvqltmjm'
	api = keepa.Keepa(accesskey)
	if doc.custom_asin_no:
		ASIN = [doc.custom_asin_no]
		if ASIN:
			try:
				products = api.query(ASIN, stats=30, rating=True, update=0, domain="IN", history=1)
			except Exception as e:
				frappe.throw(_(f"Invalid ASIN: {doc.custom_asin_no}"))
			else:
				for i in range(len(ASIN)):
					if products[i]["imagesCSV"]:
						doc.image = "https://images-na.ssl-images-amazon.com/images/I/" + products[i]["imagesCSV"].split(',')[0]
					doc.manufacturer = products[i]["manufacturer"]
					if products[i]['listedSince']:
						epoch_time = (products[i]["listedSince"]+ 21564000) * 60000
						listed_since_date = datetime.datetime.utcfromtimestamp(epoch_time / 1000)
						doc.listed_since = listed_since_date.strftime("%Y-%m-%d")
					sales_ranks = products[i]["salesRanks"]
					sales_rank_reference = products[i]["salesRankReference"]
					if sales_ranks and sales_rank_reference:
						if str(sales_rank_reference) in sales_ranks:
							sales_rank_history = sales_ranks[str(sales_rank_reference)]
							doc.sales_rank = str(sales_rank_history[-1])
					doc.sales_rank_ref = products[i]['salesRankReference']
					doc.amazon_url = f'https://www.amazon.in/dp/{doc.custom_asin_no}'
					if len(products[i]['csv']) > 0:
						if len(products[i]['csv']) >= 17:
							if products[i]['csv'][17]:
								doc.reviews_count = products[i]['csv'][17][-1]
						if len(products[i]['csv']) >= 16:
							if products[i]['csv'][16]:
								doc.reviews_rating = str(products[i]['csv'][16][-1]/10)
					doc.parent_asin = products[i]["parentAsin"]
					category_tree = []
					category_tree_dict = {}
					if products[i].get('categoryTree'):
						category_tree = [i.get("name") for i in products[i].get('categoryTree')]
						category_tree_dict = {i["catId"]:i["name"] for i in products[i]['categoryTree']}

					if category_tree:
						doc.category_sub = category_tree[-1]
						doc.categories_tree = ", ".join(category_tree)
					if category_tree_dict:
						doc.category_root = category_tree_dict.get(products[0].get('rootCategory'))
					
					# doc.ean =  re.findall('[0-9]+', json.dumps(products[i]['eanList'][0]))[0] if products[i]['eanList'] is not None else ''
					doc.ean =  products[i]['eanList'][0] if products[i]['eanList'] else ''

					doc.upc = json.dumps(products[i]['upcList'])
					doc.launchpad = products[i]['launchpad']  # currently a data field, should be checkbox
					doc.partnumber = products[i]['partNumber']
					frequently_bought_together = products[i]['frequentlyBoughtTogether']
					if isinstance(frequently_bought_together, (list, tuple)):
						doc.freq_brought_together = ", ".join(frequently_bought_together)
					else:
						doc.freq_brought_together = ""
					variations = products[i]['variations']
					asin_attributes = []
					if variations:
						v = [row.get('asin') for row in variations]
						if v:
							doc.variation_asins = ", ".join(v)
						asin_attributes = [row.get('attributes') for row in variations if row.get('asin')==doc.custom_asin_no and row.get('attributes')]
					if asin_attributes:
						attr_dict = [row for row in asin_attributes[0]]
						if attr_dict:
							doc.variation_attributes = f"{attr_dict[0].get('dimension')}: {attr_dict[0].get('value')}"
					doc.product_group = products[i]['productGroup']
					doc.number_of_items = products[i]['numberOfItems']
					doc.package_height = str(products[i]['packageHeight']/10)
					doc.package_length = str(products[i]['packageLength']/10)
					doc.package_width = str(products[i]['packageWidth']/10)
					doc.package_weight = products[i]['packageWeight']
					doc.package_quantity = products[i]['packageQuantity']
					pkg_dimension = str(products[i]['packageLength']/10 * products[i]['packageWidth']/10 * products[i]['packageHeight']/10)
					if products[i]['packageHeight']/10 > 0 and products[i]['packageLength']/10 > 0 and products[i]['packageWidth']/10 > 0:
						doc.package_dimention = f"{doc.package_length} x {doc.package_width} x {doc.package_height} cm (= {pkg_dimension}) cm\u00b3"
					doc.model = products[i]['model']
					doc.length_length = str(products[i]['itemLength']/10)
					doc.length_breadth = str(products[i]['itemWidth']/10)
					doc.length_height = str(products[i]['itemHeight']/10)
					doc.length_weight = products[i]['itemWeight']
					item_dimension = str(products[i]['itemLength']/10 * products[i]['itemWidth']/10 * products[i]['itemHeight']/10)
					if products[i]['itemLength']/10 > 0 and products[i]['itemWidth']/10 > 0 and products[i]['itemHeight']/10 > 0:
						doc.length_dimension = f"{doc.length_length} x {doc.length_breadth} x {doc.length_height} cm (= {item_dimension} cm\u00b3)"
					doc.size = products[i]['size']
					doc.color = products[i]['color']
					doc.desc_feature = products[i]["description"]
					doc.title = products[i]["title"]
					doc.custom_amzon_item_name = products[i]["title"]
					if products[0]['features'] and len(products[0]['features']) >= 5:
						doc.desc_feature_1 = products[0]['features'][0]
						doc.desc_feature_2 = products[0]['features'][1]
						doc.desc_feature_3 = products[0]['features'][2]
						doc.desc_feature_4 = products[0]['features'][3]
						doc.desc_feature_5 = products[0]['features'][4]
					stats_parsed = products[i].get("stats_parsed")
					if stats_parsed:
						current = stats_parsed.get("current")
						avg30 = stats_parsed.get("avg30")
						avg90 = stats_parsed.get("avg90")
						avg180 = stats_parsed.get("avg180")
						lowest = stats_parsed.get("min")
						highest = stats_parsed.get("max")
						if current:
							doc.current_price = current.get("SALES")
							doc.last_price = current.get("LISTPRICE")
							doc.new_current = current.get("NEW")
						if avg30:
							doc.custom_sales_30days = avg30.get("SALES")
							doc.list_price_30days = avg30.get("LISTPRICE")
							doc.new_30days = avg30.get("NEW")
						if avg90:
							doc.custom_sales_90days = avg90.get("SALES")
							doc.list_price_90days = avg90.get("LISTPRICE")
							doc.new_90days = avg90.get("NEW")
						if avg180:
							doc.custom_sales_180days = stats_parsed.get("avg180").get("SALES")
							doc.list_price_180days = stats_parsed.get("avg180").get("LISTPRICE")
							doc.new_180days = stats_parsed.get("avg180").get("NEW")
						if lowest:
							new_lowest = lowest.get("NEW")
							if new_lowest and len(new_lowest)==2:
								doc.new_lowest = new_lowest[1]
							lowest_listprice = lowest.get("LISTPRICE")
							if lowest_listprice and len(lowest_listprice)==2:
								doc.list_price_lowest = lowest_listprice[1]
						if highest:
							new_highest = lowest.get("NEW")
							if new_highest and len(new_highest)==2:
								doc.new_highest = new_highest[1]
							highest_listprice = highest.get("LISTPRICE")
							if highest_listprice and len(highest_listprice)==2:
								doc.list_price_highest = highest_listprice[1]

				frappe.msgprint(_("Item(s) has been synced with keepa"))


def create_selling_price(doc, event):
	for item in doc.items:
		if item.rate > 0:
			item_price_exists = frappe.db.get_all("Item Price", {"item_code": item.item_code, "selling": 1, "price_list": "Standard Selling"})
			if not item_price_exists:
				item_master = frappe.get_doc("Item", item.item_code)
				item_price = frappe.new_doc("Item Price")
				item_price.item_code = item.item_code
				item_price.price_list = "Standard Selling"
				item_price.selling = 1
				item_price.item_name = item_master.item_name
				item_price.uom = item_master.stock_uom
				item_price.valid_from = today()
				item_price.currency = frappe.db.get_value("Company", doc.company, "default_currency")
				selling_rate = item.rate + ( 0.05 * item.rate)  # Calculate selling rate with a 5% margin
				item_price.price_list_rate = round(selling_rate, 9) # Format the selling rate to end with 9
				item_price.save()


def create_item_price(doc, event):
	if frappe.db.exists("Item", {"name": doc.name}):
		if doc.custom_mrp != frappe.db.get_value("Item", doc.name, "custom_mrp"):
			item_price = frappe.new_doc("Item Price")
			item_price.item_code = doc.item_code
			item_price.price_list = "Standard Selling"
			item_price.selling = 1
			item_price.item_name = doc.item_name
			item_price.uom = doc.stock_uom
			item_price.valid_from = today()
			item_price.price_list_rate = float(doc.custom_mrp) -  (0.05 * float(doc.custom_mrp))  # Calculate selling rate with a 5% margin
			item_price.save()