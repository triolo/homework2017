import urllib.request
import re
import os

if not os.path.exists("plaintext"):
    os.mkdir("plaintext")
G = os.path.abspath("plaintext")

def download_page(pageUrl):
    text = ""
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('utf-8')
        print("Success at: ", pageUrl)
    except:
        print('Error at', pageUrl)
    return text


def issue_links():
    issues = []
    commonUrl = 'http://magazines.russ.ru/sib/'
    for j in range(2006, 2007):
        for i in range(1, 13):
            issueUrl = commonUrl + str(j) + '/' +str(i)
            issues.append(issueUrl)
    print(issues)
    return issues


def get_article_links(issue):
    text = download_page(issue)
    eachissuelinks = re.findall(r'(/sib/[0-9]*/[0-9]*/.*?.html)', text)
    return eachissuelinks


def get_text(articlelink):
    text = download_page(articlelink)
    m = re.search(r'(<div class=\"body_contents\">(.*?)</div>)', text, flags=re.DOTALL)
    tbox = m.group(1)
    return tbox


def clean(text):
    regTags = re.compile('(<.*?>)', re.DOTALL)
    regSpaces = re.compile('\s{2,}',re.DOTALL)
    regBrackets = re.compile('{.*?}', re.DOTALL)
    regLatin = re.compile(r'[a-zA-Z]+',re.DOTALL)
    cleantext = regSpaces.sub(" ", text)
    cleantext = regTags.sub("", cleantext)
    cleantext = regBrackets.sub("", cleantext)
    cleantext = regLatin.sub("", cleantext)
    return cleantext

def directories():
    os.chdir("plaintext")
    for i in range(2006, 2015):
        for j in range(1, 13):
            path = str(i)+ "/" + str(j)
            if not os.path.exists(path):
                os.makedirs(path)
    return 0


def form_path_name(link):
    match = re.search(r"(/[0-9]{4}/[0-9]{1,}?)/(.*?).html", link)
    path = match.group(1)
    name = match.group(2)
    print(path, name)
    return path, name

def write_into(cleantext, path, name):
    os.chdir(G + path)
    with open(name + ".txt", "w", encoding="utf-8") as f:
        try:
            f.write(cleantext)
            print("Successful writing")
        except:
            print("Error writing")
    return


def main():
    siteaddress = 'http://magazines.russ.ru'
    allissuelinks = []
    issuelinks = issue_links()
    for link in issuelinks:
        eachissuelinks = get_article_links(link)
        allissuelinks.append(eachissuelinks)
    for issue in range (len(allissuelinks)):
        for link in allissuelinks[issue]:
            link = siteaddress + link
            print(link)
            txt = get_text(link)
            txt = clean(txt)
            pth, nme = form_path_name(link)
            write_into(txt, pth, nme)

    return 0
main()
#directories()