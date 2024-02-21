import os
import io
import tkinter as tk
import tkinter.filedialog as fd
import bs4
import shutil


def print_usage(dir_path):
    print('Using ' + dir_path)


def format_all_html_files(dir_path):
    for path, subdirs, files in os.walk(dir_path):
        for file in files:
            name, extension = os.path.splitext(file)
            if extension != '.html':
                continue

            print("\033[38;5;039mFormatting\033[0m [\033[38;5;002m✔\033[0m] : " + path.replace("\\", '/') + "/" + file)
            modify_navbar_in_file(path + "/" + file)
            modify_searchbar_in_file(path + "/" + file)


def modify_navbar_in_file(file):
    with io.open(file) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, 'html.parser')

    nav_links = soup.find_all("li")

    if len(nav_links) == 0:
        return

    icon_script_link = soup.new_tag("script", src="https://kit.fontawesome.com/f785611823.js", crossorigin="anonymous")
    soup.head.append(icon_script_link)

    for i in range(len(nav_links)):
        icon = None

        if nav_links[i].text == "Overview":
            icon = soup.new_tag("i", **{'class': 'fas fa-columns'})
        if nav_links[i].text == "Package":
            icon = soup.new_tag("i", **{'class': 'fas fa-cubes'})
        if nav_links[i].text == "Class":
            icon = soup.new_tag("i", **{'class': 'far fa-file-code'})
        if nav_links[i].text == "Tree":
            icon = soup.new_tag("i", **{'class': 'fas fa-sitemap'})
        if nav_links[i].text == "Index":
            icon = soup.new_tag("i", **{'class': 'far fa-address-book'})
        if nav_links[i].text == "Help":
            icon = soup.new_tag("i", **{'class': 'far fa-question-circle'})
        if icon is None:
            continue

        nav_links[i].insert(0, icon)

    with open(file, "w") as outf:
        outf.write(str(soup.prettify(formatter="html")))


def modify_searchbar_in_file(file):
    with io.open(file) as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, 'html.parser')

    old_search = soup.find("div", **{'class': 'sub-nav'})
    if old_search is None:
        return

    old_search.decompose()

    content_div = soup.new_tag("div", **{'class': 'nav-list-search'})
    search_input = soup.new_tag("input", **{'type': 'text', 'id': 'search-input', 'value': 'search', 'disabled': 'disabled'})
    reset_button = soup.new_tag("input", **{'type': 'reset', 'id': 'reset-button', 'value': 'reset', 'disabled': 'disabled'})
    soup.html.header.nav.div.ul.append(content_div)
    soup.html.header.nav.div.ul.div.append(search_input)
    soup.html.header.nav.div.ul.div.append(reset_button)

    with open(file, "w") as outf:
        outf.write(str(soup.prettify(formatter="html")))


def generate_script():
    tk.Tk().withdraw()
    directory_path = fd.askdirectory()

    print('Starting documentation formatting for folder ' + directory_path)

    if not directory_path:
        print('[\033[38;5;001mNo folder chosen\033[0m] Exiting program.')
        return

    print_usage(directory_path)
    format_all_html_files(directory_path)
    replace_css_files_content(directory_path)


def replace_css_files_content(directory_path):
    print('\033[38;5;214mReplacing\033[0m [\033[38;5;002m✔\033[0m] : ' + directory_path + '/stylesheet.css')
    shutil.copyfile(directory_path + '/stylesheet.css', 'custom-files/stylesheet.css')
    print('\033[38;5;214mReplacing\033[0m [\033[38;5;002m✔\033[0m] : ' + directory_path + '/jquery-ui.overrides.css')
    shutil.copyfile(directory_path + '/jquery-ui.overrides.css', 'custom-files/jquery-ui.overrides.css')


def print_prog_name():
    with open('custom-files/progname.txt', 'r') as f:
        text = list(f)
        row_len = len(text[4])

    colors = [39, 75, 111, 147, 183, 219, 218, 217, 216, 215, 214]
    chunk_size = len(colors)
    chunk_len = row_len // chunk_size

    for line in text:
        for i in range(len(colors)):
            start = i * chunk_len
            to = i * chunk_len + chunk_len

            if i != len(colors) - 1:
                print('\033[38;5;{}m{}'.format(colors[i], line[start:to]), end='')
            else:
                print('\033[38;5;{}m{}'.format(colors[i], line[start::]), end='')

    print('\033[0m')


print_prog_name()
generate_script()
