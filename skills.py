#!/usr/bin/env python3

import requests, re, subprocess, csv, sys, os, json
from bs4 import BeautifulSoup

def check_int(x):
  try:
    int(x)
    return True
  except ValueError:
    return False

def page_number(url):
  s = requests.session()
  r = s.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  page_number = []
  page_all = soup.find_all('a', {"class": "page-link"})

  for page in page_all:
    try:
      page_number.append([p.text for p in page if p.text])
    except:
      pass

  page_number = [int(page) for sublist in page_number for page in sublist if check_int(page)]
  try:
    return sorted(page_number, key=int, reverse=True)[0]
  except:
    return 1

def get_offers(keyword):
  base_url = "https://nofluffjobs.com/pl/" + keyword
  jobs = []
  i=0
  for p in range(1,(page_number(base_url)+1)):

    url = base_url + "?page=" + str(p)
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('a', href=True, limit=None):
      link = a.get('href')
      if "/job/" in link :
        jobs.append("https://nofluffjobs.com" + str(link))
        i = i + 1

  print('Total number of pages with job offers:', p)
  print('Total job offers:', i)

  return(jobs)

def get_skill(url):
  s = requests.session()
  r = s.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')

  skills_batch = soup.find_all('h3')

  hierarchy = ["musthave", "nice2have", "other"]
  skill = {}
  i = 0
  for requirements in skills_batch:
    try:
      req = [r.text.strip('" ').strip(' "').lower() for r in requirements if r.text]
      skill[hierarchy[i]]=req
      if i < len(skills_batch) :
        i+= 1
    except:
      pass
  skill["url"]=url
  return skill

def skill_collection(offers, skills_file ="devops-skills.txt"):
  skill_collection = {}
  offers = (x for x in offers if x is not None)
  for url in offers:
    name = url.split('/')[-1].rsplit('-',1)[0]
    skill_collection[name] = get_skill(url)

  with open(skills_file, 'w') as skills_file:
    skills_file.write(json.dumps(skill_collection))
  skills_file.close()

def main():
  category_filter = str(sys.argv[1])
  offers = get_offers(category_filter)
  skill_collection(offers, category_filter + "-skills.txt")

if __name__ == "__main__":
  main()
