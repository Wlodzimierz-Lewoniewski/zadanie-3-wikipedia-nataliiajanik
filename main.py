import requests
import re

def ekstrakcja_danych_z_artykulu(url_suffix):
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{url_suffix}"
    response = requests.get(url)
    
    html_content = response.text
    
    #with open("zawartosc.html", "w", encoding="utf-8") as file:
    #    file.write(html_content)
    
    pattern = r'mw-category-generated".*?<li><a href="([^"]+)" title="[^"]+">.*?</a></li>\s*<li><a href="([^"]+)" title="[^"]+">.*?</a></li>'
    matches = re.search(pattern, html_content, re.DOTALL)
    links = []

    if matches:
        links.append(matches.group(1))
        links.append(matches.group(2))
        
        
    for link in links:
        article_url = f"https://pl.wikipedia.org/{link}"
        article_response = requests.get(article_url)
        article_content = article_response.text
        
        #internal links
        positionInternal = article_content.find('id="mw-content-text"')
        html_internal_links = article_content[positionInternal:]
        
        pattern_internal_links = r'href="[^:]+?".+?title="(.*?)"'
        internal_links_names = re.findall(pattern_internal_links, html_internal_links)[:5]
        
        if internal_links_names:
            print(" | ".join(internal_links_names))
        else:
            print("\n")
        
        #imgs
        img_position = article_content.find('mw-content-ltr mw-parser-output')
        html_imgs = article_content[img_position:]
    
        pattern_imgs = r'<img.+?src="(.+?)"'
        imgs_links = re.findall(pattern_imgs, html_imgs)[:3]
        
        if imgs_links:
            print(" | ".join(imgs_links))
        else:
            print("\n")       
            
        #external links
        external_links_position = article_content.find('id="Przypisy"')
        if external_links_position is not None:
            external_links_position = article_content.find(r'mw-references-wrap')
            html_external_links = article_content[external_links_position:]
            pattern_external_links = r'"(http.+?)"'
            external_links = re.findall(pattern_external_links, html_external_links)[:3]
            if external_links:
                print(" | ".join(external_links))
        else:
            print("\n")
        
        #categories
        categories_position = article_content.find('mw-normal-catlinks')
        html_categories = article_content[categories_position:]
    
        pattern_categories = r'<li.+?>(.+?)</a></li>'
        categories_links = re.findall(pattern_categories, html_categories)[:3]
        
        if categories_links:
            print(" | ".join(categories_links))
        else:
            print("\n")   
            
article_name = input()
article_name = article_name.replace(" ", "_")
ekstrakcja_danych_z_artykulu(article_name)
