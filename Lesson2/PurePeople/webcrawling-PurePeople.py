# coding: utf-8
import requests
import unittest
from bs4 import BeautifulSoup

website_prefix = "http://www.purepeople.com"
def _handle_request_result_and_build_soup(request_result):
  if request_result.status_code == 200:
    html_doc =  request_result.text
    soup = BeautifulSoup(html_doc,"html.parser")
    return soup


def _convert_string_to_int(string):
  if "K" in string:
    string = string.strip()[:-1]
    return float(string.replace(',','.'))*1000
  else:
    return int(string.strip())

def get_all_links_for_query(query):
  url = website_prefix + "/rechercher/"
  res = requests.post(url, data = {'q': query })
  soup = _handle_request_result_and_build_soup(res)
  specific_class = "c-article-flux__title"
  all_links = map(lambda x : x.attrs['href'] , soup.find_all("a", class_= specific_class))

  return all_links

def get_share_count_for_page(page_url):
  res = requests.get(page_url)
  soup = _handle_request_result_and_build_soup(res)
  specific_class = "c-sharebox__stats-number"
  share_count_text = soup.find("span", class_= specific_class).text
  return  _convert_string_to_int(share_count_text)

def get_popularity_for_people():
  query = str(input("First celebrity : "))
  query2 = str(input("Second celebrity : "))
  url_people = get_all_links_for_query(query)
  url_people2 = get_all_links_for_query(query2)
  results_people = []
  results_people2 = []
  for url in url_people:
      results_people.append(get_share_count_for_page(website_prefix + url))
  for url in url_people2:
      results_people2.append(get_share_count_for_page(website_prefix + url))
  if sum(results_people) > sum(results_people2):
      print (str(query) + ' est le plus populaire avec ' + str(int(sum(results_people)  - sum(results_people2))) + ' Partages de plus')
  else:
      print (str(query2) + ' ' + str(int(sum(results_people2)  - sum(results_people))) + ' Partages de plus')

get_popularity_for_people()

class Lesson1Tests(unittest.TestCase):
    def testShareCount(self):
        self.assertEqual(get_share_count_for_page("http://www.purepeople.com/article/brigitte-macron-decroche-une-jolie-couv-a-l-etranger_a306389/1") , 139)

    def testConvertStringInt(self):
        self.assertEqual(_convert_string_to_int("\n                            86\n                    ") , 86)
        self.assertEqual(_convert_string_to_int("5,84K") , 5840)
        self.assertEqual(_convert_string_to_int("\n                            1,6K\n                   ") , 1600)

def main():
    unittest.main()

if __name__ == '__main__':
    main()