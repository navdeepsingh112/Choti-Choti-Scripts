from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class YouTubeCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()  # You may need to specify the path to your chromedriver executable

    def scroll_down(self):
        # Scroll down the page to load more content
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Add a small delay to allow content to load

    def crawl(self, search_query):
        url = f"https://www.youtube.com/results?search_query={search_query}"
        self.driver.get(url)

        video_urls = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to load more content
            self.scroll_down()
            
            # Get the new height of the page
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If no more content is loaded, break the loop
                break
            last_height = new_height

        # After scrolling, retrieve all video links
        video_links = self.driver.find_elements(By.CSS_SELECTOR, 'a.yt-simple-endpoint')
        for link in video_links:
            video_url = link.get_attribute('href')
            if video_url:
                video_urls.append(video_url)

        return video_urls

    def close(self):
        self.driver.quit()

# Example usage
search_query = input("Enter your YouTube search query: ")
crawler = YouTubeCrawler()
video_urls = crawler.crawl(search_query)
print(video_urls)
crawler.close()
