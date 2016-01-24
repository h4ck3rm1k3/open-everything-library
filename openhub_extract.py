#!/usr/bin/python3

import lxml
from lxml.html import  html5parser
#import sys
import getopt
import pprint
import sys
from lxml import etree

# name: String,
# url: String,
# html_url: String,
# created_at: String,
# updated_at: String,
# description: String,
# homepage_url: String,
# download_url: String,
# url_name: String,
# medium_logo_url: String,
# small_logo_url: String,
# user_count: String,
# average_rating: String,
# rating_count: String,
# review_count: String,
# analysis_id: String,
# tags: String,
# licenses: String,
# links: String
# "USER_COUNT",
# "YEAR_CONTRIBUTORS", "result/project/analysis/twelve_month_contributor_count")
# "YEAR_COMMITS", "result/project/analysis/twelve_month_commit_count")
# "MAIN_LANGUAGE","result/project/analysis/main_language_name"
# "ACTIVITY", "result/project/project_activity_index/description"
# "ACTIVITY_INDX", "result/project/project_activity_index/value"
# "FIRST_COMMIT", "result/project/analysis/min_month"
# "MOST_RECENT_COMMIT", "result/project/analysis/max_month"
# "FACTOIDS" "result/project/analysis/factoids"

def debug(name, x, depth = 1):
    print (name + ":")
    d = {
        'context' :context(x, depth ),
    }

    if len(x.attrib.keys())>0:
        d['attr'] = x.attrib
        
    if x.text:
        d['text'] = x.text
        
    pprint.pprint(d)
    
    for y in x:
        debug(name + "Child", y, depth + 1)
    
def clean(t):
    return t.replace('{http://www.w3.org/1999/xhtml}','html:')

def crit(a):
    c = []

    for k in a:
        if k in ('capture','follow'):
            pass
        else:
            v = a[k]
            c.append("@" + k + "=" + "'" + v + "'")

    return "[" + " and ".join(c) + "]"


def context(x, depth=-1):    
    p = x.getparent()
    if depth == 0 :
        p = None # stop
    if p != None:
        return context(x.getparent(), depth -1) + "/"+ clean(x.tag) + crit(x.attrib)
    else:
        return clean(x.tag)

def paths(doc, xpath):

    try:
        r = doc.xpath(
            xpath,
            namespaces={
                'html': 'http://www.w3.org/1999/xhtml'
            })
    except Exception as e:
        print "Check",xpath
        print e
        raise e
    return r


def process(fn):
    print("File in:",fn)
    o = html5parser.parse(fn)
    #pprint.pprint(o)

    #NS="{http://www.w3.org/1999/xhtml}"
    NS="{html}:"

    for base in paths(o,
                      "/html:html/html:body[@zoom='1']/html:div[@id='page' and @class='container']/html:div[@id='page-contents']/html:div[@id='projects_show_page' and @class='col-md-12']"
    ):
        #print("FOUND\n")
        #print(base)
        #pprint.pprint( base.attrib)
        #pprint.pprint( base.tag)
        #pprint.pprint( base.text)
        for section1 in paths(base,
                          "./html:div[@id='project_masthead']/html:div[@id='project_header' and @class='col-md-11']"
        ):
            ##            print("section 1\n")

            for  section1_1 in paths(
                    section1,
                    "./html:div[@class='pull-left project_title']"):

                for  title in paths(
                        section1_1,
                        "./html:h1[@class='float_left' and @itemprop='name']/html:a[ @itemprop='url']"):
                    print "title:", title.text
                    print "project_internal_href: http://openhub.net" + title.attrib['href']


            for section_1_2 in paths(
                    section1,
                    "./html:div[@id='widgets' and @class='col-md-3 pull-right no_padding']"):
                
                for activity in paths(
                        section_1_2,
                        "./html:div[@id='project_header_activity_indicator' and @class='pull-left']/html:a"):
                    print "activity:", activity.attrib['class'], activity.attrib['title']
                    for activity_text in paths(
                            activity,
                            "../html:div[@class='thirtyfive_project_activity_text']"
                    ):
                        print "activity_text: ", activity_text.text

                for activity_interaction in paths(
                        section_1_2,
                        "./html:div[@itemtype='CreativeWork' and @itemprop='interactionCount']/html:div[@id='i_use_this_container' and @class='pull-right']/html:div[@class='use_count']/a"
                ):
                    print("UseCount:" + activity_interaction.text                 )
                    

    for  projects_show_page_item in paths(
            base,
            "./html:div[@itemtype='http://schema.org/ItemPage' and @id='projects_show_page']"
    ):

        #'context': "/html:div[@id='page_contents']/html:div/html:h2[@class='pull-left']",
        analysis_count = 0 
        for  analysis_timestamp in paths(
                projects_show_page_item,
                ".//html:div[@id='analysis_timestamp' and @class='pull-right soft']/html:i/html:abbr"):
            #debug("analysis_timestamp",analysis_timestamp)
            analysis_count = analysis_count + 1
            print "Analysis_" + str(analysis_count) + " : "+ analysis_timestamp.attrib['title'] 


 
        for  projects_show_page_item_div in paths(
                projects_show_page_item,
                "./html:div[@class='col-md-12']/html:div[@id='page_contents']/html:div[@class='row']/html:div[@class='col-md-6']"):


            #"html:div/html:dl[@class='dl-horizontal unstyled']]",

            for enlistments in paths(
                    projects_show_page_item_div,
                    "./html:div/html:dl[@class='dl-horizontal unstyled']/html:dd[@style='margin-bottom: .5em;']"):
                #debug("enlistment",enlistments)
                if len(enlistments.text) > 1:
                    s = enlistments.text
                    s = s.replace("\n","")
                    print ("Enlistments:" + s)
                
                            
            for  projects_show_page_item_1 in paths(
                    projects_show_page_item_div,
                    "./html:div[@class='well']/html:dl[@class='dl-horizontal unstyled']"
            ):

                #debug("Item1",projects_show_page_item_1)
                for d_license in paths(
                        projects_show_page_item_1,
                        "./html:dd[@style='margin-bottom: .5em;']/html:span[@itemtype='http://schema.org/CreativeWork' and @itemscope='']/html:span[@itemprop='publishingPrinciples']/html:a"):
                    print "License:" + d_license.attrib['href']

                    
                for dd in paths(
                        projects_show_page_item_1,
                        "./html:dd[@style='margin-bottom: .5em;']"):
                    for href in paths(
                            dd,
                            "./html:a[@itemprop='url']/html:i[@class='icon-external-link']/.."):
                        url = href.attrib['href']
                        print ("ExternalURL: " + url)


             
            for description in paths(
                    projects_show_page_item_div,
                    "./html:div[@id='project_summary' and @itemprop='description']"
            ):
                print "Description:..." 
                #print("Description:" + etree.tostring(description, pretty_print=True))
                

    # projects_show_page_item section_2_1 
    # projects_show_page_item section_2_1 /html:dt/html:a[@href='/html:p/html:${PROJECTNAME}/html:enlistments']
    # projects_show_page_item section_2_1 /html:dt/html:a[@href='/html:p/html:${PROJECTNAME}/html:licenses']
    # projects_show_page_item section_2_1 /html:dt/html:a[@href='/html:p/html:${PROJECTNAME}/html:managers']
    # projects_show_page_item section_2_1 /html:dt/html:a[@href='/html:p/html:${PROJECTNAME}/html:similar']


    #section_2_2 = "/html:div[@class='col-md-12']/html:div[@id='page_contents']/html:div[@class='row']/html:div[@class='col-md-6']"
    #projects_show_page_item section_2_2 /html:div[@id='project_summary' and @itemprop='description']/html:p
    #projects_show_page_item section_2_2 /html:div[@itemtype='http://schema.org/CreativeWork' and @itemscope='' and @id='project_tags']
    #projects_show_page_item section_2_2 /html:div[@itemtype='http://schema.org/CreativeWork' and @itemscope='' and @id='project_tags']/html:p[@style='padding-left: 20px;' and @class='tags']/html:a[@href='/html:tags?names=TAG' and @class='tag' and @itemprop='keywords']
        for tags in paths(
                projects_show_page_item,
                ".//html:div[@id='project_tags']" +
                "/html:p[@class='tags']" +
                "/html:a[@href and @class='tag' and @itemprop='keywords']"):
            #debug("Tags",tags)
            #print ("tag" + tags.attrib["href"])
            print ("tag_text:" + tags.text)
            #{'attr': {'href': '/tags?names=jquery', 'class': 'tag', 'itemprop': 'keywords'},
            #/html:p[@style='padding-left: 20px;' and @class='tags']/html:a[@href='/tags?names=jquery' and @class='tag' and @itemprop='keywords']",


    # spinner... needs login
    #section_2_3 ="/html:div[@class='col-md-12']/html:div[@id='page_contents']/html:div[@id='proj_rating' and @class='col-md-3']"
    #projects_show_page_item section_2_3/html:div/html:div[@class='clear']/html:div[@star_style='big' and @style='margin-left: 9px' and @score='0' and @class='jrating needs_login pull-left' and @id='${PROJECTNAME}' and @data-show='projects/html:show/html:community_rating']
    #projects_show_page_item section_2_3/html:div/html:span[@style='margin-left: 5px;']/html:a[@href='/html:p/html:${PROJECTNAME}/html:reviews/html:new']

    projects_show_page_item_4= "/html:div[@class='margin_left_20 margin_right_20']/html:div[@class='footer-navigation']/html:div[@class='actions col-md-3 margin_bottom_20 no_padding']/html:ul[@class='nav nav-stacked nav-pills']/html:h4[@class='selected linked']/html:a[@href='/html:p/html:${PROJECTNAME}']"

    # for x in paths(o,
    #                "/html:/html:html:div[@class='well searchable']"
    #                #"/html:/html:{ns}:div[@class='well searchable']".format(ns=NS)
    #                #"/html:html/html:body[@zoom='1']/html:div[@id='page' and @class='container']/html:div[@id='page-contents']/html:div[@id='projects_index_page' and @class='col-md-12']/html:div[@id='projects_index_list']/html:div[@id='project_341570' and @class='well searchable']"
    # ):
    #     print("\n\nFOUND")
    #     for keywords in paths(
    #             x,
    #             "./html:/html:html:div[@class='tags']/html:html:a[@href and @class='tag' and @itemprop='keywords']"
    #     ):
    #         print("\t","Keywords", keywords.text)
    #     for lang in paths(
    #             x,
    #         "./html:/html:html:div[@class='add-info']/html:html:div[@class='main_language pull-left']/html:html:span"
    #     ):
    #         print("\t","Lang:",lang.text)
    #     for changedate in paths(x,
    #                             "./html:/html:html:div[@class='info pull-left']/html:html:p/html:i/html:html:abbr[@class='date']"): #and @title
    #         print("\t","Changedate:",etree.tostring(changedate))
    #     for lic in paths(
    #             x,
    #             "./html:/html:html:div[@class='add-info']/html:html:div[@class='licenses pull-right']/html:html:span"
    #     ):
    #         print("\t","License:",lic.text)
    #     for content in paths(x,
    #                       "./html:html:div[@id='inner_content' and @class='pull-left']"):
    #         for heading in paths(content,
    #                          "./html:html:h2[@class='title pull-left']"):
    #             for title in paths(heading,
    #                                "./html:html:a"):
    #                 print("\t","project.href",title.attrib['href'])
    #                 print("\t","project.title", title.attrib['title'])
    #         for summary in paths(content,
    #                              "./html:html:div[@class='info pull-left']/html:html:div[@class='desc']/html:html:span[@style='display: inline' and @id and @class='proj_desc_toggle']"):
    #             print("\t","Summary:",summary.text.replace("\n"," "))
    #         for desc in paths(content,
    #                           "./html:html:div[@class='info pull-left']/html:html:div[@class='desc']/html:html:span[@style='display: none' and @id and @class='proj_desc_toggle']"
    #                           ):
    #             print("\t","Desc", desc.text.replace("\n"," "))
    #         for something in paths(
    #                 content,
    #                 "./html:html:div[@class='stats pull-left']/html:html:p" #/html:html:a[@href]
    #         ):
    #             print("\t", something[1].text,":",something[0].text)
    #         for reviews in paths(
    #                 content,
    #                 "./html:html:div[@class='reviews-and-pai pull-left']"
    #         ):
    #             #print "\t","reviews:",etree.tostring(reviews)
    #             #print "\t", something[1].text,":",something[0].text
    #             for reviews2 in paths(
    #                     reviews,
    #                     "./html:html:div[@class='reviews']/html:html:a[@href]"):
    #                 print("\t","Reviews:",reviews2.text)
    #             for act in paths(
    #                     reviews,
    #                     "./html:html:div[@class='twentyfive_project_activity_text']"):
    #                 print("\t","activity:",act.text)
    #             for rat in paths(
    #                     reviews,
    #                     "./html:/html:html:span[@itemprop='ratingValue']"):
    #                 print("\t","rating:",rat.text)


def sample():
    todo = [
        'golazo',
        'highspeedtransactiongridiusa',
        'groovyscript',
        'openjweb',
        'proxy6151',
        'docusearch',
        'aost',
        'htmlcompressor'
    ]
    base = "sources/openhub/details/"
    for x in todo :
        process(base + x + ".html")

sample()
