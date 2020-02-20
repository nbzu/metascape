import scrapy
from genecards.items import GenecardsItem

import pandas as pd

class GenecardsSpider(scrapy.Spider):
    name = "genecards"

    def start_requests(self):
        df = pd.read_csv('input.csv')
        for cluster, row in df.iteritems():
            for gene_name in row :
                if not pd.isnull(gene_name):
                    burp0_url = "https://www.genecards.org/cgi-bin/carddisp.pl?gene=" + gene_name
                    burp0_cookies = {
                        "ASP.NET_SessionId":"egn2rlbap1ag3zll4bxf2qq1",
                        "rvcn":"RDZWUjVxCOUWEB5gezAsD_WHpdsyYHmgfZbvOG-wkEthhvnxhk1NDEaK__SDTHYaPHHxmv4xftSoyBGAWRrWnG5Uxs01",
                        "ARRAffinity":"68016c959d4d63d2d506b06af260b9037b4062d3a25bfd2917e24e286fbe0a71",
                        "visid_incap_146342":"XGlLz1tISIS8Bim2EYWJCtTHgF0AAAAAQUIPAAAAAACW+FNXfxeUPMc8VaJ4r9x7",
                        "nlbi_146342":"IR1rT0OzAyPycgH/mewSQgAAAAAv6r7AMaTubWQ4LoO9yT4y",
                        "incap_ses_896_146342":"w8tjFNpfLzceLFDxDzxvDNXHgF0AAAAAmtKtVL8ZM0oB9d6g0LZznQ==",
                        "_ga":"GA1.2.272735959.1568720851",
                        "_gid":"GA1.2.357598591.1568720851",
                        "_gat":"1",
                        "__gads":"ID=2560068a5d356b3c:T=1568720864:S=ALNI_MbzwxLJu1_fKGRPN59CuChoU6fctg"
                    }
                    burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
                    request = scrapy.Request(
                        url=burp0_url,
                        meta={
                            'gene_name':gene_name,
                            'cluster':cluster
                        },
                        callback=self.parse,
                        headers=burp0_headers,
                        cookies=burp0_cookies,
                        dont_filter = True
                    )
                    yield request
            

    def parse(self, response):
        # 不一定所有的都有这三栏,要校验一下
        clean = lambda x : ' '.join([' '.join(i.split()) for i in x])
        item = GenecardsItem() 
        item['_1_cluster'] = response.meta['cluster']
        item['_2_gene_name'] = response.meta['gene_name']
        item['_3_first'] = clean(response.selector.xpath('//*[@id="summaries"]/div[contains(.,"Entrez Gene Summary for")]//text()').extract())
        item['_4_second'] = clean(response.selector.xpath('//*[@id="summaries"]/div[contains(.,"GeneCards Summary for")]//text()').extract())
        item['_5_third'] = clean(response.selector.xpath('//*[@id="summaries"]/div[contains(.,"UniProtKB/Swiss-Prot Summary for")]//text()').extract())
        yield item