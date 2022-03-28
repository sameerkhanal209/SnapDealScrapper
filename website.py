from flask import Flask, render_template, request
import scrapper as scrapper
import html

website = 'WeFashion'

def display():
    app = Flask(__name__)

    @app.route('/')
    def index():
        
        products = scrapper.getProducts('index','mens-footwear-special-shoes','plrty')

        data = {'title':website, 'page':'Latest Products', 'products': products, 'pt':'index'}
        return render_template('index.html', data=data)
    
    @app.route('/search', methods = ['GET'])
    def searchpd():

        query = request.args.get('q')
        order = request.args.get('o')
        
        txt = ''
        if order == 'rec':
            txt = 'Fresh Arrived'
        elif order == 'plth':
            txt = 'Low Priced'
        elif order == 'phtl':
            txt = 'High Priced'
        elif order == 'dhtl':
            txt == 'Discounted'
        else:
            txt = "Popular"
            
        products = scrapper.getProducts('search',query,order)

        data = {'title':website, 'page':'Search results for '+str(query)+ ' - ' +str(txt), 'products': products, 'pt':'search', 'purl':'/search?q='+str(query)}
        return render_template('index.html', data=data)

    @app.route('/cat/<query>/<order>')
    def listpd(query,order):

        if order == 'rec':
            txt = 'Fresh Arrived'
        elif order == 'plth':
            txt = 'Low Priced'
        elif order == 'phtl':
            txt = 'High Priced'
        elif order == 'dhtl':
            txt == 'Discounted'
        else:
            txt = "Popular"

        products = scrapper.getProducts('cat',query,order)

        data = {'title':website, 'page':str(txt)+' '+str(query)+' You might like', 'products': products, 'pt':'cat', 'purl':'/cat/'+str(query)}
        return render_template('index.html', data=data)
    
    @app.route('/product/<query>/<rc>')
    def getpd(query,rc):

        query = query + '/' + rc
        #products = scrapper.getProducts('product','mens-footwear-special-shoes',1)
        products = scrapper.getProducts('product',query,1)

        data = {'title':website, 'page':products['p_title'], 'products': products, 'pt':'product', 'query': query}
        return render_template('product.html', data=data, html=html)
    
    app.run()
