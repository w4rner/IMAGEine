
import scrape_images 
from selenium import webdriver

# Sears tower search 
sears_tower_url = "https://www.google.com/search?tbm=isch&source=hp&biw=1536&bih=759&ei=TS16WuKfDseAtgWEzKcw&q=sears+tower&oq=sears+tower&gs_l=img.3...64600.66152.0.66263.0.0.0.0.0.0.0.0..0.0....0...1ac.1.64.img..0.0.0....0.q996ARtSelE"
driver = webdriver.Firefox()
sears_tower_search = scrape_images.get_pics_from_search(sears_tower_url, driver, 10)
# 
# hull_house_url = "https://www.google.com/search?q=hull+house+chicago&rlz=1C1CHBD_enUS759US759&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi3ydb7iZXZAhVQ7FMKHbsZB3MQ_AUICigB&biw=1536&bih=759"
# hull_house_search = scrape_images.get_pics_from_search(hull_house_url, driver, 10)


#other_search_url = "https://www.google.com/search?tbm=isch&source=hp&biw=1536&bih=759&ei=i855Wt65KonwsAWRzaTYBw&q=Arthur+H.+Compton+House+Illinois&oq=Arthur+H.+Compton+House+Illinois&gs_l=img.3...5886.7255.0.7448.0.0.0.0.0.0.0.0..0.0....0...1ac.1.64.img..0.0.0....0.uq9inO-sWU0"
#other_search_url = "https://www.google.com/search?tbm=isch&source=hp&biw=1536&bih=759&ei=i855Wt65KonwsAWRzaTYBw&q=Frank+Lloyd+Wright+Home+And+Studio+Illinois&oq=Frank+Lloyd+Wright+Home+And+Studio+Illinois&gs_l=img.3...5886.7255.0.7448.0.0.0.0.0.0.0.0..0.0....0...1ac.1.64.img..0.0.0....0.uq9inO-sWU0"
#other_search = scrape_images.get_pics_from_search(other_search_url, driver, 10)
