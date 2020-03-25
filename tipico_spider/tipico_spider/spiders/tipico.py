import time
import scrapy
import datetime
from selenium import webdriver
from time import sleep
from parsel import Selector


class TipicoSpider(scrapy.Spider):
    name = 'tipico'
    start_urls = ['https://www.tipico.de/program/scoresPopup.faces']

    def __init__(self):
        self.driver = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')


    def parse(self, response):
        self.driver.get(response.url)
        sleep(5)
        sel = Selector(text=self.driver.page_source)
        football_button = self.driver.find_element_by_xpath("//span[contains(text(),'Football')]/parent::a")
        football_button.click()
        sleep(50)
        sel = Selector(text=self.driver.page_source)
        for row in sel.xpath("//div[@class='t_cell w_113 left'][1]/parent::div[@class='e_active ']/parent::div"):
            country = row.xpath("./parent::div[@class='e_active e_noCache ']//parent::div[@class='border_ccc']/div/div[@class='t_head cf']/div/text()").extract_first()
            country_replace = country.replace('Results » Football - ', '')
            
            league = row.xpath("./parent::div[@class='e_active e_noCache ']/div[@class='t_subhead cf']/div[@class='red pad_l_9 left']/text()").extract_first()
            league_replace = league.replace(',', '')

            cl = str(country_replace) + "_" + str(league_replace)
            
            home = row.xpath("./div[@class='e_active ']/parent::div/div[@class='e_active ']/div[@class='t_cell w_113 left'][1]/text()").extract_first()
            home_strip = home.strip()
            home_c = str(home_strip) + " " + "(" + str(country_replace) + ")"

            away = row.xpath("./div[@class='e_active ']/parent::div/div[@class='e_active ']/div[@class='t_cell w_113 left'][2]/text()").extract_first()
            away_strip = away.strip()
            away_c = str(away_strip) + " " + "(" + str(country_replace) + ")"
            
            score = row.xpath("./div[@class='e_active ']/parent::div/div[@class='e_active ']/div[@class='w_175 grey bl align_c overWhiteSpace left'][1]/text()").extract_first()
            score_list = []
            score_replace1 = score.replace(')', '')
            score_replace2 = score_replace1.replace(' (', '#')
            score_list.append(score_replace2)
            try:
                ft, ht = zip(*(s.split("#") for s in score_list))
                ft1, ft2 = zip(*(s.split(":") for s in ft))
                ht1, ht2 = zip(*(s.split(":") for s in ht))
            except:
                ft = None
                ht = None
                ft1 = None
                ft2 = None
                ht1 = None
                ht2 = None


            m_date = row.xpath("./div[@class='e_active ']/parent::div/div[@class='e_active ']/div[@class='w_40 bl align_c left'][1]/text()").extract_first()
            m_date_split = m_date.split('.')
            day = m_date_split[0]
            mounth = m_date_split[1]
            now = datetime.datetime.now()
            now_year = now.year
            now_year1 = str(now_year)
            current_date = now_year1 + '-' + mounth + '-' + day
            datetime_object = datetime.datetime.strptime(current_date, '%Y-%m-%d').date()

            m_time = row.xpath("./div[@class='e_active ']/parent::div/div[@class='e_active ']/div[@class='w_40 bl align_c left'][2]/text()").extract_first()

            date_time = current_date + " " + m_time
            date_time1 = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')

             


            yield {
                'country': country_replace,
                'league': league_replace,
                'cl': cl,
                'home': home_strip,
                'home_country': home_c,
                'away': away_strip,
                'away_country' : away_c,
                'm_date': datetime_object,
                'm_time': m_time,
                'dt': date_time1,
                'ft1': ft1,
                'ft2': ft2,
                'ht1': ht1,
                'ht2': ht2
            }
        self.driver.quit()

