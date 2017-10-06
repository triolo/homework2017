import urllib.request
import re
import os

PT = os.path.abspath("plain")
root = os.path.abspath("")
app_size = []


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
    for j in range(2006, 2015):
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
    fulltext = download_page(articlelink)
    m = re.search(r'(<div class=\"body_contents\">(.*?)</div>)', fulltext, flags=re.DOTALL)
    tbox = m.group(1)
    return tbox, fulltext


def clean(text):
    regTags = re.compile('(<.*?>)', re.DOTALL)
    regSpaces = re.compile('\s{2,}',re.DOTALL)
    regBrackets = re.compile('{.*?}', re.DOTALL)
    #regLatin = re.compile(r'[a-zA-Z]+',re.DOTALL)
    regHeader = re.compile(r'(Admin|Татьяна).*?Table\s*', re.DOTALL)
    cleantext = regTags.sub("", text)
    cleantext = regBrackets.sub("", cleantext)
    cleantext = replace_punct(cleantext)
    cleantext = regSpaces.sub(" ", cleantext)
    try:
        cleantext = regHeader.sub("", cleantext)
        print("Header was dirty, but I cleaned it")
    except:
        print("Header is clean or something went wrong")
    return cleantext

def replace_punct(text):
    text = text.replace("&#8220;","“")
    text = text.replace("&#8221;","”")
    text = text.replace("&#8212;","—")
    text = text.replace("&#8230;","…")
    text = text.replace("&#8230;", "…")
    text = text.replace("&#9;", "\t")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&#160;", " ")
    return text

def directories():
    os.chdir(root)
    if not os.path.exists("plain"):
        os.mkdir("plain")
    os.chdir("plain")
    for i in range(2006, 2015):
        for j in range(1, 13):
            path = str(i)+ "/" + str(j)
            if not os.path.exists(path):
                os.makedirs(path)
    os.chdir(root)
    if not os.path.exists("mystem-xml"):
        os.mkdir("mystem-xml")
    os.chdir("mystem-xml")
    for i in range(2006, 2015):
        for j in range(1, 13):
            path = str(i)+ "/" + str(j)
            if not os.path.exists(path):
                os.makedirs(path)
    os.chdir(root)
    if not os.path.exists("mystem-plain"):
        os.mkdir("mystem-plain")
    os.chdir("mystem-plain")
    for i in range(2006, 2015):
        for j in range(1, 13):
            path = str(i)+ "/" + str(j)
            if not os.path.exists(path):
                os.makedirs(path)
    os.chdir(root)
    return 0


def form_path_name(link):
    match = re.search(r"(/[0-9]{4}/[0-9]{1,}?)/(.*?).html", link)
    path = match.group(1)
    name = match.group(2)
    print(path, name)
    return path, name

def write_into(cleantext, path, name, metaplain):
    os.chdir(PT + path)
    with open(name + ".txt", "w", encoding="utf-8") as f:
        try:
            f.write(metaplain + cleantext)
        except Exception:
            print("Error writing")
        else:
            print("Successful writing")
    return

def get_metadata(text):
    meta = {'author': "Not found", 'title': "Not found", 'URL': "Not found", 'site_name': "Not found", 'publ_year': "Not found", 'category': "Not found", 'path': "Not found"}
    try:
        m = re.search(r"<meta property=\"article:author\" content=\"(.*?)\"/>", text)
        meta['author'] = m.group(1)
    except:
        print("Author not found")
    else:
        print("Author successfully found", meta['author'])


    try:
        m = re.search(r"<meta property=\"og:title\" content=\"(.*?)\"/>", text)
        meta['title'] = m.group(1)
    except:
        print("Title not found")
    else:
        print("Title successfully found")


    try:
        m = re.search(r"<meta property=\"og:url\" content=\"(.*?)\"/>", text)
        meta['URL'] = m.group(1)
        path, name = form_path_name(meta['URL'])
        meta['path'] = path + "/" + name
    except:
        print("URL not found")
    else:
        print("URL successfully found")


    try:
        m = re.search(r"<meta property=\"og:site_name\" content=\"(.*?)\">", text)
        meta['site_name'] = m.group(1)
    except:
        print("Site_name not found")
    else:
        print("Site_name successfully found")


    try:
        m = re.search(r"<o:LastSaved>(.*?)T.*?</o:LastSaved>", text)
        meta['publ_year'] = m.group(1)
    except:
        print("Publ_year not found")
    else:
        print("Publ_year successfully found")


    try:
        m = re.search(r"<meta property=\"og:description\" content=\"(.*?)\"/>", text)
        meta['category'] = m.group(1)
    except:
        print("Category not found")
    else:
        print("Category successfully found")

    return meta

def write_csv_header():
    header = "path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size	source\tpublication	publisher\tpubl_year\tmedium\tcountry\tregion\tlanguage"
    with open(root + "/" + "metadata.csv", "w", encoding="utf-8") as f:
        f.write(header)
    return 0

def meta_to_csv(meta):
    mtadta = "\n{0}\t{1}\t\t\t{2}\t{3}\tпублицистика\t\t{4}\t\tнейтральный\tн-возраст\tн-уровень\tфедеральная\t{5}\t{6}\t\t{7}\tгазета\tРоссия\tNONE\tru"
    mtaformatted = mtadta.format(meta['path'], meta['author'], meta['title'], meta['publ_year'], meta['category'], meta['URL'], meta['site_name'], meta['publ_year'])
    with open(root + "/" + "metadata.csv", mode="a", encoding="utf-8") as file:
        file.write(mtaformatted)
    print(mtaformatted)
    return 0

def meta_to_plain(meta):
    plain_meta = "@au {0}\n@ti {1}\n@da {2}\n@topic {3}\n@url {4}\n"
    pm_formatted = plain_meta.format(meta['author'], meta['title'], meta['publ_year'], meta['category'], meta['URL'])
    return pm_formatted

def corpus_size():
    size = 0
    for root, dirs, files in os.walk(PT):
        for f in files:
            with open(os.path.join(root, f), "r", encoding="utf-8") as f1:
                oneline = f1.read()
                item_size = oneline.count(" ") + 1
                size += item_size
    print("Оценочный размер корпуса: ", size)
    return 0

def mystem():
    argx = "-cgind --format xml "
    argp = "-cgind "
    for root, dirs, files in os.walk("plain"):
        for f in files:
            input_file_path = os.path.join(os.path.abspath(root), f)
            output_file_path = input_file_path.replace("plain", "mystem-xml")
            output_file_path = output_file_path.replace(".txt", ".xml")
            print(input_file_path)
            print(output_file_path)
            os.system(r"/Users/triolo/mystem " + argx + input_file_path + " " + output_file_path)
    for root, dirs, files in os.walk("plain"):
        for f in files:
            input_file_path = os.path.join(os.path.abspath(root), f)
            output_file_path = input_file_path.replace("plain", "mystem-plain")
            print(input_file_path)
            print(output_file_path)
            os.system(r"/Users/triolo/mystem " + argp + input_file_path + " " + output_file_path)
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
            try:
                txt, fulltext = get_text(link)
            except:
                print("Error while searching text")
            else:
                meta = get_metadata(fulltext)
                metaplain = meta_to_plain(meta)
                meta_to_csv(meta)
                txt = clean(txt)
                pth, nme = form_path_name(link)
                write_into(txt, pth, nme, metaplain)
    return 0
#directories()
#write_csv_header()
#main()
#corpus_size()
mystem()