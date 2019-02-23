# -*- coding: utf-8 -*-
# scrapy crawl trabajandoTodo -o trabajandoTodo.csv -t csv -a CSV_DELIMITER="\t"
import scrapy
import re


class AnalisisHorizontalSpider(scrapy.Spider):
    name = 'trabajandoTodo'

    start_urls = ['https://www.trabajando.cl/jobs/home/']

    def parse(self, response):
        # SIGUIENDO LA FICHA DE CADA OFERTA
        for href in response.css('h2.elcargo a::attr(href)').extract():
            yield response.follow(href, self.parse_author)

        # SIGUIENTE PAGINA
        for href in response.xpath('//*[@id="nextPageEmpresa"]/@href'):
            yield response.follow(href, self.parse)

        # CONTENIDO DE LA FICHA DE OFERTA
    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'Titulo'        : extract_with_css('h1.offerTitleText span::text'),
            'nombre_empresa': extract_with_xpath('//*[@id="detalle_oferta"]/div[1]/div[3]/div[1]/div/div[1]/h4/text()'),
            'Categoria'     : extract_with_css('div.datos-empresa h3.categoria_empresa::text'),
            'Cargo'         : extract_with_xpath('//*[@id="detalle_oferta"]/div[2]/div[3]/div[1]/div[2]/text()'),
            'Vacantes'      : response.css('div.col-md-8.txt::text')[1].extract().strip(),
            'Sueldo'        : response.css('div.col-md-8.txt::text')[10].extract().strip(),
            'Publicado'     : extract_with_xpath('//*[@id="detalle_oferta"]/div[1]/div[2]/ul/li[1]/h4/text()'),
            'Finaliza'      : extract_with_xpath('//*[@id="detalle_oferta"]/div[1]/div[2]/ul/li[2]/h4/text()'),
            'url'           : response.url,


        }

