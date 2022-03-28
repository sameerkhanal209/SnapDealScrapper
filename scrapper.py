from bs4 import BeautifulSoup
import requests
import html

def getProducts(page,query,sort):

    if page == 'index':
        loadn = f"https://www.snapdeal.com/products/{query}?sort={sort}"
    elif page == 'search':
        loadn = f"https://www.snapdeal.com/search?keyword={query}&sort={sort}"
    elif page == 'cat':
        loadn = f"https://www.snapdeal.com/products/{query}?sort={sort}"
    else:
        loadn = f"https://www.snapdeal.com/product/{query}"
    
    html_txt = requests.get(loadn).text
    soup = BeautifulSoup(html_txt, 'lxml')

    if(page == 'index' or page == 'search' or page == 'cat'):
        found_sections = soup.find_all('div', class_="product-tuple-listing")

        products = {}
        for num, product in enumerate(found_sections):
            image = product.picture.source['srcset']
            title = product.picture.source['title']
            price = product.find('span', class_="product-price").text.strip()

            oPrice = product.find('span', class_="product-desc-price").text.strip()
            link = product.find('a')['href'].replace('https://www.snapdeal.com','')
            #discount = product.find('div', class_="product-discount").span.text.strip()

            gotproduct = {
                'image': image,
                'title': title,
                'price': price,
                'oPrice': oPrice,
                'link': link
                }

            products[num] = gotproduct
            
        return products

    else:
        productDetail = {'offers':{}, 'specs':{}}
        
        p_title = soup.find('div', class_="comp-product-description").find('h1').text.strip()
        p_image = soup.find('ul', id="bx-slider-left-image-panel").find('li').find('img')['src']
        p_price = soup.find('span', class_="pdp-final-price").text.strip()
        p_oPrice = soup.find('div', class_="pdpCutPrice").text.strip()

        productDetail['p_title'] = p_title
        productDetail['p_image'] = p_image
        productDetail['p_price'] = p_price
        productDetail['p_oPrice'] = p_oPrice
        
        offers = soup.find_all('div', class_="genericOfferClass")

        for num, offer in enumerate(offers):
            offer.find('span', class_='static-tnc').decompose()
            gotOffer = offer.text.strip()
            productDetail['offers'][num] = gotOffer

        specs = soup.find_all('div', class_="spec-section")

        for num, spec in enumerate(specs):
            stitle = spec.find('span', class_="headTitle").text.strip()
            content = spec.find('div', class_="spec-body")

            gotSpecs = {'stitle':stitle, 'content':html.unescape(content)}
            productDetail['specs'][num] = gotSpecs

        return productDetail
    
def printProduct(product):
    print(f"Title: {product['title']}")
    print(f"Image: {product['image']}")
    print(f"Price: {product['price']}")
        
    print("-----")
    print(f"Original Price: {product['oPrice']}")
    print("-----")

    print('')

#getProducts('product','veirdo-green-half-sleeve-tshirt/639827458615',1)
