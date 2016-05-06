from calibre.ebooks.conversion.mobioutput import MOBIOutput
import makeoeb
import base
import time
from config import *
from calibre.utils.bytestringio import byteStringIO
import __builtin__, logging
default_log = logging.getLogger()
__builtin__.__dict__['default_log'] = default_log
class RailsBook:
    def __init__(self, hs):
        self.title = hs['title']
        self.masthead_path = hs['masthead_path']
        self.cover_path = hs['cover_path']
        self.desc = hs['desc']
        self.lang = hs['lang']
        self.feeds = hs['feeds']
        self.oldest_article = hs['oldest_article']


def createMobi(bk):
    opts = makeoeb.getOpts('kindlepw')
    oeb = makeoeb.CreateOeb(default_log, None, opts)

    title = bk.title

    makeoeb.setMetaData(oeb, title)
    oeb.container = makeoeb.ServerContainer()

    # cover
    mhfile = bk.masthead_path
    coverfile = bk.cover_path

    if mhfile:
        id_, href = oeb.manifest.generate('masthead', mhfile)  # size:600*60
        oeb.manifest.add(id_, href, makeoeb.MimeFromFilename(mhfile))
        oeb.guide.add('masthead', 'Masthead Image', href)

    if coverfile:
        id_, href = oeb.manifest.generate('cover', coverfile)
        item = oeb.manifest.add(id_, href, makeoeb.MimeFromFilename(coverfile))
        oeb.guide.add('cover', 'Cover', href)
        oeb.metadata.add('cover', id_)

    itemcnt, imgindex = 0, 0
    from collections import OrderedDict
    sections = OrderedDict()
    toc_thumbnails = {}  # map img-url -> manifest-href
    if not bk:
        default_log.warn('not exist book <%s>' % bk.title)


    book = base.BaseFeedBook(imgindex=imgindex)
    book.title = bk.title
    book.description = bk.desc
    book.language = bk.lang
    book.oldest_article = bk.oldest_article
    book.fulltext_by_readability = True
    feeds = bk.feeds
    book.feeds = [(feed["title"], feed["url"], feed["fulltext"]) for feed in feeds]

    try:
        for sec_or_media, url, title, content, brief, thumbnail in book.Items(opts):
            if not sec_or_media or not title or not content:
                continue

            if sec_or_media.startswith(r'image/'):
                id_, href = oeb.manifest.generate(id='img', href=title)
                item = oeb.manifest.add(id_, href, sec_or_media, data=content)
                if thumbnail:
                    toc_thumbnails[url] = href
                imgindex += 1
            else:
                # id, href = oeb.manifest.generate(id='feed', href='feed%d.html'%itemcnt)
                # item = oeb.manifest.add(id, href, 'application/xhtml+xml', data=content)
                # oeb.spine.add(item, True)
                sections.setdefault(sec_or_media, [])
                sections[sec_or_media].append((title, brief, thumbnail, content))
                itemcnt += 1
    except Exception as e:
        default_log.warn("Failure in pushing book '%s' : %s" % (book.title, str(e)))
    print itemcnt
    if itemcnt > 0:
        from utils import InsertToc
        InsertToc(oeb, sections, toc_thumbnails)
        oIO = byteStringIO()
        o = MOBIOutput()
        o.convert(oeb, oIO, opts, default_log)

        of_name = "/tmp/"+ time.strftime("%Y-%m-%d_%H%M%S", time.localtime()) + ".mobi"
        with open(of_name, "w") as f:
            f.write(str(oIO.getvalue()))
        return of_name
    return ""

# main

# TODO
# load json into bk object
# GET(bk)
# return output_filename
