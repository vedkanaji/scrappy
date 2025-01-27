from bs4 import BeautifulSoup

def clean_product_details_list(columns):
    cleaned_list = []
    
    for item in columns:
        # Remove Unicode control characters and extra whitespace
        cleaned_item = item.replace('\u200f', '').replace('\u200e', '')
        cleaned_item = ' '.join(cleaned_item.split())
        cleaned_list.append(cleaned_item)
    
    return cleaned_list

def find_product_table_data(html):
    soup = BeautifulSoup(html, "html.parser")
    product_data = soup.find('div', id='prodDetails')
    if product_data is None:
        return []
    table = product_data.find('table')
    columns = clean_product_details_list(columns)
    return columns


def find_product_rating(html):
    soup = BeautifulSoup(html, "html.parser")
    average_rating = soup.find(id='averageCustomerReviews').find_all("span", class_='a-size-base')[0].text.strip()
    average_rating = "".join([x for x in f"{average_rating}".strip() if x.isdigit() or x == '.'])
    average_rating = float(average_rating)
    rating_data = soup.find(id='acrCustomerReviewText').text
    rating_count = int(''.join([x for x in rating_data if x.isdigit()]))
    rating_count
    return {
        'average': average_rating,
        'count': rating_count,
    }

def extract_amazon_product_data(html):
    soup = BeautifulSoup(html, "html.parser")
    productTitle = soup.find('span', id='productTitle')
    productTitleText = f"{productTitle.text}".strip()
    productPrice = soup.find_all('span', class_='a-price-whole')[0]
    productPrice = f"{productPrice.text}".strip()
    productPriceText = "".join([x for x in productPrice if x.isdigit() or x == '.'])
    productPriceNum = float(productPriceText)
    try:
        productDescription = soup.find('div', id='productDescription').text
    except:
        productDescription = ''
    featureBullets = soup.find('div', id='feature-bullets').text
    asin = ''
    elements_with_attribute = soup.find_all(lambda tag: tag.has_attr('data-csa-c-asin'))
    asins = [x.attrs.get('data-csa-c-asin') for x in elements_with_attribute if x]
    asins = list(set([x for x in asins if x != ""]))
    metadata_items = find_product_table_data(html)
    for data in metadata_items:
        if data.startswith("ASIN") is None:
            continue
        else:
            asin = data.startswith("ASIN")
            break
    return {
        'asin': asins,
        'title': productTitleText,
        'price_raw': productPrice,
        'price_text': productPriceText,
        'price': productPriceNum,
        'metadata': metadata_items,
        'description': productDescription,
        'feature_bullets': featureBullets,
        'rating': find_product_rating(html)
    }