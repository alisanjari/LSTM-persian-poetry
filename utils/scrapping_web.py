
from bs4 import BeautifulSoup
from requests import get
import locale
import csv
import os

URL = r'https://rira.ir/?page=view&mod=classicpoems&obj=poem&id='
SAVE_PATH = r'D:/learning-ai/LSTM-persian-poetry'


KEYS = ['id','pagenum','multipage', \
        'id2','ord2','id3','ord3','id4','ord4','pagenum_pre','pagenum_afr',
        'catgo','shaer','ketab','bakhsh','title']

def process_key_items(html_soup):
    """Return Dictionary of parsed elements from Html string"""

    info_dict = {}
    all_tag_a = html_soup.find_all('a')

    numeric_info2 = all_tag_a[2].get('href').split('=')
    info_dict['id2'] = numeric_info2[4].split('&')[0]
    info_dict['ord2'] = numeric_info2[5]

    numeric_info3 = all_tag_a[3].get('href').split('=')
    info_dict['id3'] = numeric_info3[4].split('&')[0]
    info_dict['ord3'] = numeric_info3[5]

    numeric_info4 = all_tag_a[4].get('href').split('=')
    info_dict['id4'] = numeric_info4[4].split('&')[0]
    info_dict['ord4'] = numeric_info4[5]

    info_dict['id'] = all_tag_a[6].get('href').split('=')[4].split('&')[0]

    pagenum_afr = None
    pagenum_pre = None

    if len(all_tag_a) == 10:


        info_dict['multipage'] = False
        info_dict['pagenum'] = 1
        info_dict['pagenum_pre'] = pagenum_pre
        info_dict['pagenum_afr'] = pagenum_afr

    if len(all_tag_a) == 11:
        #print()

        #print(all_tag_a[7].text)
        #print(all_tag_a[7].get('href'))
        #print(all_tag_a[8].text)
        #print(all_tag_a[8].get('href'))

        if all_tag_a[7].text == 'صفحه‌ی قبل':
            splitted = all_tag_a[7].get('href').split('=')
            if len(splitted) == 7:
                pagenum_pre = int(all_tag_a[7].get('href').split('=')[-1])
            else:
                pagenum_pre = 1

            pagenum     = pagenum_pre + 1
        elif all_tag_a[7].text == 'صفحه‌ی بعد':
            splitted = all_tag_a[7].get('href').split('=')
            if len(splitted) == 7:
                pagenum_afr = int(all_tag_a[7].get('href').split('=')[-1])
            else:
                pagenum_afr = None

            pagenum     = pagenum_afr - 1
        else:
            pagenum = None

        info_dict['multipage'] = True
        info_dict['pagenum']     = pagenum
        info_dict['pagenum_pre'] = pagenum_afr
        info_dict['pagenum_afr'] = pagenum_pre

    if len(all_tag_a) == 12:

        pagenum_pre = None
        pagenum     = None
        pagenum_afr = None



        if all_tag_a[7].text == 'صفحه‌ی قبل' :
            if len(all_tag_a[7].get('href').split('=')) > 5:
                pagenum_pre = int(all_tag_a[7].get('href').split('=')[-1])
            else:
                pagenum_pre = 1

            pagenum = pagenum_pre + 1
        if all_tag_a[8].text == 'صفحه‌ی بعد' :

            if len(all_tag_a[8].get('href').split('=')) > 5:
                pagenum_afr = int(all_tag_a[8].get('href').split('=')[-1])
                pagenum = pagenum_afr - 1
            else:
                pagenum_afr = None
                pagenum = pagenum_pre + 1

        info_dict['multipage']   = True
        info_dict['pagenum_pre'] = pagenum_pre
        info_dict['pagenum_afr'] = pagenum_afr
        info_dict['pagenum']     = pagenum

    catgo = all_tag_a[1].text
    shaer = all_tag_a[2].text
    ketab = all_tag_a[3].text
    bakhsh= all_tag_a[4].text
    title = all_tag_a[5].text

    info_dict['title']  = title
    info_dict['bakhsh'] = bakhsh
    info_dict['ketab']  = ketab
    info_dict['shaer']  = shaer
    info_dict['catgo']  = catgo
    return info_dict

def process_poem(url):
    """Extract poet from the url link"""

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    beyts = html_soup.find_all('span', class_ = 'verse')
    beyts = [beyt.text for beyt in beyts]
    info_dict = process_key_items(html_soup)
    info_dict['beyts']  = beyts

    return info_dict

def write_file(poet, info_dict):
    """Save the poem into a file"""

    filename = SAVE_PATH  + '/' + poet + '/' + str(info_dict['id']) + '_'+ str(info_dict['pagenum']) \
               + '_' + info_dict['id2']  +'_' + info_dict['ord2'] \
               + '_' + info_dict['id3'] + '_' + info_dict['ord3'] \
               + '_' + info_dict['id4'] + '_' + info_dict['ord4']  + '.txt'

    print(filename)
    with open(filename, 'w', encoding='utf-16') as f:
        txt = ','.join([str(info_dict[k]) for k in KEYS ])
        txt = txt + '\n' + '\n'.join([x for x in info_dict['beyts']])
        f.write(txt)


    locale.setlocale(locale.LC_ALL, '')
    DELIMITER = ';'# if locale.localeconv()['decimal_point'] == ',' else ','

    list_of_lists = [[info_dict[k] for k in KEYS]]
    with open('D:/poem/molana.csv', 'a', newline='', encoding='utf-16') as csvfile:

        writer = csv.writer(csvfile, delimiter=DELIMITER)
        writer.writerows(list_of_lists)

def read_poems(poet, start, end):
    """
    Process all the poem of the poet

    :poet (str): The number in the link for the first poem
    :param start: The number in the link for the first poem
    :param end: The number in the link for the last poem
    :return:
        (None) save the poems in the path identified by SAVE_PATH
    """

    failed = []

    for i in range(start, end + 1):
        url = URL + str(i)
        try:
            info_dict = process_poem(url)
            write_file(poet, info_dict)
            if info_dict['multipage']:
                keep_going = True
                pagenum = 2
                while keep_going:
                    try:
                        tempurl = url + '&lim=20&pageno=' + str(pagenum)
                        info_dict = process_poem(tempurl)
                        print('here')
                        write_file(poet, info_dict)
                        pagenum = pagenum + 1
                    except:
                        keep_going = False

        except:
            failed.append(i)

    print('Failed for %d out of %d pages'%( len(failed), end - start + 1 ), failed)

def test_RUMI():
    """
    Example of using read_poem function for Rumi.
    https://en.wikipedia.org/wiki/Rumi
    """

    start = 11051
    end  = 11902
    read_poems(start, end)

def test_JAMI():
    """
    Example of using read_poem function for JAMI.
    https://en.wikipedia.org/wiki/Jami
    """

    start = 4107
    end = 4126

    foldersave = SAVE_PATH  + '/jami'

    if not os.path.isdir(foldersave):
        os.mkdir(foldersave)

    read_poems('jami' ,start, end)
