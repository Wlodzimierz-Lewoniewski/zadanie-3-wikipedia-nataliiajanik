import requests
import re

def ekstrakcja_danych_z_artykulu(url_suffix):
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{url_suffix}"
    response = requests.get(url)
    
    html_content = response.text
    
    aricles_position = re.search(r'mw-category-generated', html_content).start()
    articles_content = html_content[aricles_position:]
    
    pattern = r'<a.+?href="\/wiki([^:]+?)".+?>(.+?)<\/a>'
    links = re.findall(pattern, articles_content)[:2]
    
    for link in links:
        article_url = f"https://pl.wikipedia.org/wiki{link[0]}"
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
        
        if len(imgs_links) > 3:
            imgs_links = imgs_links[:3]
        print(" | ".join(imgs_links))
            
        #external links
        external_links_position = article_content.find('id="Przypisy"')
        if external_links_position != -1:
            html_external_links = re.search(r'id="Przypisy"(.+)', article_content, re.DOTALL)
            if html_external_links:
                html_external_links = re.search(r'class="references"(.+?)<\/ol>', html_external_links.group(), re.DOTALL)
                if html_external_links:
                    external_links = re.findall(r'"(http.+?)"', html_external_links.group())
                    if len(external_links) > 3:
                        external_links = external_links[:3]    
                print(" | ".join(external_links))
        else:
            print("\n")
        
        #categories
        html_categories = re.search(r'mw-normal-catlinks(.+?)</div>', article_content, re.DOTALL)
    
        if html_categories:
            html_categories = html_categories.group(1)  # Wydobywamy tekst między 'mw-normal-catlinks' i '</div>'
            categories_links = re.findall(re.compile(r'<li.+?>(.+?)</a></li>'), html_categories)
            if len(categories_links) > 3:
                categories_links = categories_links[:3]
            print(" | ".join(categories_links))
        else:
            print("\n")

        
article_name = input()
article_name = article_name.replace(" ", "_")
ekstrakcja_danych_z_artykulu(article_name)
