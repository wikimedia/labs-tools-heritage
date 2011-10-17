#!/usr/bin/python
# -*- coding: utf-8  -*-
'''
Tool to copy a flickr stream to Commons

# Get a set to work on (start with just a username).
# * Make it possible to delimit the set (from/to)
#For each image
#*Check the license
#*Check if it isn't already on Commons
#*Build suggested filename
#**Check for name collision and maybe alter it
#*Pull description from Flinfo
#*Show image and description to user
#**Add a nice hotcat lookalike for the adding of categories
#**Filter the categories
#*Upload the image

Todo:
*Check if the image is already uploaded (SHA hash)
*Check and prevent filename collisions
**Initial suggestion
**User input
*Filter the categories

'''
#
# (C) Multichill, 2009, 
# (C) Strainu, 2011
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id: flickrripper.py 9042 2011-03-13 10:14:47Z xqt $'

import sys, urllib, re,  StringIO, hashlib, base64, time
sys.path.append("/home/project/e/r/f/erfgoed/pywikipedia")
sys.path.append("../../../pywikipedia/trunk/pywikipedia")
import wikipedia as pywikibot
import config, query, imagerecat, upload

import flickrapi                  # see: http://stuvel.eu/projects/flickrapi
import xml.etree.ElementTree
from Tkinter import *
from PIL import Image, ImageTk    # see: http://www.pythonware.com/products/pil/
import io, json
import os, posixpath

flickr_allowed_license = {
    0 : False, # All Rights Reserved
    1 : False, # Creative Commons Attribution-NonCommercial-ShareAlike License
    2 : False, # Creative Commons Attribution-NonCommercial License
    3 : False, # Creative Commons Attribution-NonCommercial-NoDerivs License
    4 : True,  # Creative Commons Attribution License
    5 : True,  # Creative Commons Attribution-ShareAlike License
    6 : False, # Creative Commons Attribution-NoDerivs License
    7 : True,  # No known copyright restrictions
    8 : True,  # United States Government Work
}

templates_for_flickr_license = {
    0 : u'{{copyvio|Flickr, licensed as "All Rights Reserved" which is not a free license --~~~~}}\n', # All Rights Reserved
    1 : u'{{copyvio|Flickr, licensed as "Creative Commons Attribution-NonCommercial-ShareAlike" which is not a free license --~~~~}}\n', # Creative Commons Attribution-NonCommercial-ShareAlike License
    2 : u'{{copyvio|Flickr, licensed as "Creative Commons Attribution-NonCommercial" which is not a free license --~~~~}}\n', # Creative Commons Attribution-NonCommercial-ShareAlike License
    3 : u'{{copyvio|Flickr, licensed as "Creative Commons Attribution-NonCommercial-NoDerivs" which is not a free license --~~~~}}\n', # Creative Commons Attribution-NonCommercial-ShareAlike License
    4 : u'{{cc-by-2.0}}',  # Creative Commons Attribution License
    5 : u'{{cc-by-sa-2.0}}',  # Creative Commons Attribution License
    6 : u'{{copyvio|Flickr, licensed as "Creative Commons Attribution-NoDerivs" which is not a free license --~~~~}}\n', # Creative Commons Attribution-NonCommercial-ShareAlike License
    7 : u'{{Flickr-no known copyright restrictions}}',  # No known copyright restrictions
    8 : u'{{PD-USGov}}',  # United States Government Work
}

ripper_config = {
    'country': u'es',
    'lang': u'es',
    'group': u'1737383@N20', # Hint: Take the group id from the head\link to rss 
    'monument_template': u'BIC',
    'monument_regexp': u'(?:BIC[:=]?)?(RI-51-([0-9]+)(-[0-9]+)?)',
    'categories': u'[[Category:Cultural heritage monuments in Spain]]\n[[Category:Flickr images from Wiki Loves Monuments 2011 in Spain]]',
}

def getPhoto(flickr = None, photo_id = ''):
    '''
    Get the photo info and the photo sizes so we can use these later on

    TODO: Add exception handling

    '''
    
    gotPhoto = False
    while not gotPhoto:
        try:
            photoInfo = flickr.photos_getInfo(photo_id=photo_id)
            #xml.etree.ElementTree.dump(photoInfo)
            
            # TODO: Replace this call with the attributes of the <photo> tag. See http://www.flickr.com/services/api/misc.urls.html
            photoSizes = flickr.photos_getSizes(photo_id=photo_id)
            #xml.etree.ElementTree.dump(photoSizes)
            gotPhoto = True
        except flickrapi.exceptions.FlickrError:
            gotPhotos = False
            pywikibot.output(u'Flickr api problem, sleeping')
            time.sleep(30)

	# Return an object with all the relevant fields
	photo = {}
	photo['photo_id'] = photo_id
	photo['url'] = getPhotoUrl(photoSizes)
	photo['license'] = int(photoInfo.find('photo').attrib['license']) # Numeric value
	photo['title'] = photoInfo.find('photo').find('title').text
	if photo['title'] is not None:
		photo['title'] = photo['title'].strip()
	photo['user_id'] = photoInfo.find('photo').find('owner').attrib['nsid']
	photo['username'] = photoInfo.find('photo').find('owner').attrib['username']
	photo['realname'] = photoInfo.find('photo').find('owner').attrib['realname']
	photo['location'] = photoInfo.find('photo').find('owner').attrib['location']
	photo['description'] = photoInfo.find('photo').find('description').text
	photo['date_taken'] = photoInfo.find('photo').find('dates').attrib['taken']
	photo['date_posted'] = photoInfo.find('photo').find('dates').attrib['posted']
	photo['tags'] = getTags(photoInfo)
	
	location = photoInfo.find('photo').find('location')
	if location is not None:
	    photo['latitude'] = location.attrib['latitude']
	    photo['longitude'] = location.attrib['longitude']
    photo['photopage'] = photoInfo.find('photo').find('urls').find('url').text

    return photo

def isAllowedLicense(photo = None):
    '''
    Check if the image contains the right license

    TODO: Maybe add more licenses
    '''

    license = photo['license']
    if flickr_allowed_license[int(license)]:
        return True
    else:
        return False

def getPhotoUrl(photoSizes = None):
    '''
    Get the url of the jpg file with the highest resolution
    '''
    url = ''
    # The assumption is that the largest image is last
    for size in photoSizes.find('sizes').findall('size'):
        url = size.attrib['source']
    return url

def downloadPhoto(photoUrl = '', imagedir = False):
    '''
    Download the photo and store it in a StrinIO.StringIO object.

    TODO: Add exception handling

    '''
    
    filename = False
    if imagedir:
        filename = os.path.join(imagedir,posixpath.basename(urllib.url2pathname(photoUrl)))
        
        if os.path.exists(filename):
            return StringIO.StringIO(io.open(filename, "rb").read())
    
    imageFile=urllib.urlopen(photoUrl).read()
    
    if filename:
        io.open(filename, "wb").write(imageFile)
    
    return StringIO.StringIO(imageFile)

def findDuplicateImages(photoStream=None,
                        site=pywikibot.getSite(u'commons', u'commons')):
    ''' Takes the photo, calculates the SHA1 hash and asks the mediawiki api
    for a list of duplicates.

    TODO: Add exception handling, fix site thing

    '''
    hashObject = hashlib.sha1()
    hashObject.update(photoStream.getvalue())
    return site.getFilesFromAnHash(base64.b16encode(hashObject.digest()))

def getTags(photoInfo = None):
    ''' Get all the tags on a photo '''
    result = []
    for tag in photoInfo.find('photo').find('tags').findall('tag'):
        result.append(tag.attrib['raw'])

    return result

def getFlinfoDescription(photo_id = 0):
    '''
    Get the description from http://wikipedia.ramselehof.de/flinfo.php

    TODO: Add exception handling, try a couple of times
    '''
    parameters = urllib.urlencode({'id' : photo_id, 'raw' : 'on'})

    rawDescription = urllib.urlopen(
        "http://wikipedia.ramselehof.de/flinfo.php?%s" % parameters).read()

    return rawDescription.decode('utf-8')

def getDescription(photo):
	'''
	Get the description, similar to flinfo, but without connecting to a remote server
	 Differences with flinfo:
	  * flinfo doesn't show seconds for the date
	  * flinfo converts some tags into categories
	  * This doesn't undo html entities (but MediaWiki will!)
	'''
	
	author = u'[http://www.flickr.com/people/' + photo['user_id'] + ' '
	
	if photo['realname']:
		author += photo['realname']
	else:
		author += photo['username']
	author += ']'
	if photo['location']:
		author += u' from ' + photo['location']
	
	if photo['description'] is not None:
		desc = photo['description']
	elif photo['title'] is not None:
		desc = photo['title']
	else:
		desc = u''
	
	if photo['title'] is not None:
		source = photo['title']
	else:
		source = 'Flickr'
	
	# Don't create wikilinks by error
	desc = desc.replace('[', '&#x5B;')
	desc = desc.replace(']', '&#x5D;')
	
	desc = re.sub('<a href="([^"]+)"(?: target="_blank")?(?: rel="nofollow")?>([^<]*)</a>', '[\\1 \\2]', desc) # Convert html links to wikitext
	desc = re.sub('<b>([^"]+)</b>', "'''\\1'''", desc) # Convert html bold to wikitext
	desc = re.sub('<i>([^"]+)</i>', "''\\1''", desc) # Convert html italic to wikitext
	
	description = u'''{{Information
|Description=%s
|Source=[%s %s]
|Date=%s
|Author=%s
|Permission=
|other_versions=
}}
''' % (desc, photo['photopage'], source, photo['date_taken'], author)
	
	try:
		description += u"{{Location dec|" + photo['latitude'] + "|" + photo['longitude'] + "|source:Flickr}}\n"
	except:
		True

	description += u"\n=={{int:license-header}}==\n"
	description += templates_for_flickr_license[photo['license']]
	description += u"\n{{flickrreview}}\n"
	description += u"\n{{subst:unc}}\n" # Mark the file as uncategorized
	
	return description

def getFilename(photo=None, site=pywikibot.getSite(u'commons', u'commons'),
                project=u'Flickr'):
    ''' Build a good filename for the upload based on the username and the
    title. Prevents naming collisions.

    '''
    username = photo['username']
    title = photo['title']
    if title and not re.match('^(IMG|DSC)_\d+$', title):
        title =  cleanUpTitle(title)
    elif photo['description']:
        title =  cleanUpTitle(photo['description'])
    else:
        title = u''

    #baseFilename = u'File:%s - %s - %s' % (project, username, title)
    baseFilename = u'%s - %s' % (username, title)
    baseFilename = u'%s' % (title)
    print baseFilename

    if pywikibot.Page(site, u'File:%s.jpg'
                      % (baseFilename) ).exists():
        i = 2
        while True:
            if (pywikibot.Page(site, u'File:%s (%s).jpg'
                               % (baseFilename, str(i))).exists()):
                i = i + 1
            else:
                return u'%s (%s).jpg' % (baseFilename,
                                                   str(i))
    else:
        return u'%s.jpg' % (baseFilename)

def cleanUpTitle(title):
    ''' Clean up the title of a potential mediawiki page. Otherwise the title of
    the page might not be allowed by the software.

    '''
    title = title.strip()
    title = re.sub(u"[<{\\[]", u"(", title)
    title = re.sub(u"[>}\\]]", u")", title)
    title = re.sub(u"[ _]?\\(!\\)", u"", title)
    title = re.sub(u",:[ _]", u", ", title)
    title = re.sub(u"[;:][ _]", u", ", title)
    title = re.sub(u"[\t\n ]+", u" ", title)
    title = re.sub(u"[\r\n ]+", u" ", title)
    title = re.sub(u"[\n]+", u"", title)
    title = re.sub(u"[?!]([.\"]|$)", u"\\1", title)
    title = re.sub(u"[&#%?!]", u"^", title)
    title = re.sub(u"[;]", u",", title)
    title = re.sub(u"[/+\\\\:]", u"-", title)
    title = re.sub(u"--+", u"-", title)
    title = re.sub(u",,+", u",", title)
    title = re.sub(u"[-,^]([.]|$)", u"\\1", title)
    title = title.replace(u" ", u"_")
    return title

def getMonumentId(photo):
    prog = re.compile(ripper_config['monument_regexp'])
    for tag in photo['tags']:
        print tag
        m = prog.match(tag.upper())
        if m <> None:
            return m.group(1)
    return u'';

def buildDescription(photo, flinfoDescription=u'', flickrreview=False, reviewer=u'',
                     override=u'', addCategory=u'', removeCategories=False):
    ''' Build the final description for the image. The description is based on
    the info from flickrinfo and improved.

    '''
    description = flinfoDescription
    description = description.replace(u'|Description=', u'|Description={{' + ripper_config['lang'] + '|1=');
    print "monument", getMonumentId(photo)
    description = description.replace(u'\n|Source=', u'}}\n{{' + ripper_config['monument_template'] + '|' + getMonumentId(photo) + '}}\n|Source=');
    if removeCategories:
        description = pywikibot.removeCategoryLinks(description,
                                                    pywikibot.getSite(
                                                        'commons', 'commons'))
    if override:
        description = description.replace(u'{{cc-by-sa-2.0}}\n', u'')
        description = description.replace(u'{{cc-by-2.0}}\n', u'')
        description = description.replace(u'{{flickrreview}}\n', u'')
        description = description.replace(
            u'{{copyvio|Flickr, licensed as "All Rights Reserved" which is not a free license --~~~~}}\n',
            u'')
        description = description.replace(u'=={{int:license}}==',
                                          u'=={{int:license}}==\n' + override)
    elif flickrreview:
        if reviewer:
            description = description.replace(u'{{flickrreview}}',
                                              u'{{flickrreview|' + reviewer +
                                              '|{{subst:CURRENTYEAR}}-{{subst:CURRENTMONTH}}-{{subst:CURRENTDAY2}}}}')
											  
    description = description + u'\n{{Wiki Loves Monuments 2011|' + ripper_config['country'] + '}}'
    description = description + u'\n' + ripper_config['categories'] + '\n'
    description = description.replace(u'{{subst:unc}}\n', u'')
    if addCategory:
        description = description + u'\n[[Category:' + addCategory + ']]\n'
    description = description.replace(u'\r\n', u'\n')
    description = re.sub(u'BIC=([A-Za-záÁéÉíÍóÓúÚ ]+)\nID=(RI-[0-9-]+)\n?', u'\\1 (\\2)', description) # Formato usado por la Universidad de Alcalá
    return description

def compareDescriptions(photo):
	flinfoDescription = getFlinfoDescription(photo['photo_id'])
	description = getDescription(photo)
	
	flinfoDescription = re.sub('(\\[\\[Category:[^\\]]+\\]\\]\n)+', '{{subst:unc}}', flinfoDescription).strip()
	description = re.sub('(Date=[0-9-]+ [0-9-]+:[0-9-]+):[0-9-]+', '\\1', description).strip()
	if (flinfoDescription == description):
		print photo['photo_id'], " equal\n"
		return
	print photo['photo_id'], " differs:\n"
	
	f = io.open(photo['photo_id'] + '-flinfo.txt', 'w')
	f.write(flinfoDescription)
	f.close()
	f = io.open(photo['photo_id'] + '-info.txt', 'w')
	f.write(description)
	f.close()
	
	pywikibot.output(flinfoDescription)
	pywikibot.output("//****//\n")
	pywikibot.output(description)
	return

def processPhoto(photo, photoStream, flickrreview=False, reviewer=u'',
                 override=u'', addCategory=u'', removeCategories=False,
                 autonomous=False):
        ''' Process a single Flickr photo '''
        
        #Don't upload duplicate images, should add override option
        duplicates = findDuplicateImages(photoStream)
        if duplicates:
            pywikibot.output(u'Found duplicate image at %s' % duplicates.pop())
        else:
            site=pywikibot.getSite(u'commons', u'commons')
            filename = getFilename(photo, site)
            flinfoDescription = getDescription(photo)
            pywikibot.output(flinfoDescription)
            photoDescription = buildDescription(photo, flinfoDescription,
                                                flickrreview, reviewer,
                                                override, addCategory,
                                                removeCategories)
            #pywikibot.output(photoDescription)
            if not autonomous:
                while True:
                    (newPhotoDescription, newFilename, skip) = Tkdialog(
                        photoDescription, photoStream, filename, u' '.join(photo['tags'])).run()
                    
                    if skip or newFilename == filename:
                        break
                    if not pywikibot.Page(site, u'File:' + newFilename).exists():
                        break
                    filename = newFilename # Show the dialog again to choose a different filename
                    photoDescription = newPhotoDescription
                    photoStream = StringIO.StringIO(photoStream.getvalue())
            else:
                newPhotoDescription = photoDescription
                newFilename = filename
                skip = False
        
        #pywikibot.output(newPhotoDescription)
        #if (pywikibot.Page(title=u'File:'+ filename, site=pywikibot.getSite()).exists()):
        # I should probably check if the hash is the same and if not upload it under a different name
        #pywikibot.output(u'File:' + filename + u' already exists!')
        #else:
            #Do the actual upload
            #Would be nice to check before I upload if the file is already at Commons
            #Not that important for this program, but maybe for derived programs
            #skip = True
            if not skip:
                bot = upload.UploadRobot(photo['url'],
                                         description=newPhotoDescription,
                                         useFilename=newFilename,
                                         keepFilename=True,
                                         verifyDescription=False)
                bot._contents = photoStream.getvalue()
                bot.upload_image(debug=False)
                return 1

        return 0

class Tkdialog:
    ''' The user dialog. '''
    def __init__(self, photoDescription, photo, filename, tags = u''):
        self.root=Tk()
        #"%dx%d%+d%+d" % (width, height, xoffset, yoffset)
        self.root.geometry("%ix%i+0+0"%(config.tkhorsize, config.tkvertsize))

        self.root.title(filename)
        self.photoDescription = photoDescription
        self.filename = filename
        self.photo = photo
        self.skip=False
        self.exit=False

        ## Init of the widgets
        # The image
        self.image=self.getImage(self.photo, 400, 300)
        self.imagePanel=Label(self.root, image=self.image)

        self.imagePanel.image = self.image

        # The filename
        self.filenameLabel=Label(self.root,text=u"Suggested filename")
        self.filenameField=Entry(self.root, width=100)
        self.filenameField.insert(END, filename)

        # The description
        self.descriptionLabel=Label(self.root,text=u"Suggested description")
        self.descriptionScrollbar=Scrollbar(self.root, orient=VERTICAL)
        self.descriptionField=Text(self.root)
        self.descriptionField.insert(END, photoDescription)
        self.descriptionField.config(state=NORMAL, height=12, width=100, padx=0, pady=0, wrap=WORD, yscrollcommand=self.descriptionScrollbar.set)
        self.descriptionScrollbar.config(command=self.descriptionField.yview)
        
        # Show flickr tags for reference on description
        self.tagsLabel=Label(self.root,text=u"Flickr tags")
        self.tagsField=Entry(self.root, width=100)
        self.tagsField.insert(END, tags)

        # The buttons
        self.okButton=Button(self.root, text="OK", command=self.okFile)
        self.skipButton=Button(self.root, text="Skip", command=self.skipFile)

        ## Start grid

        # The image
        self.imagePanel.grid(row=0, column=0, rowspan=11, columnspan=4)

        # The buttons
        self.okButton.grid(row=11, column=1, rowspan=2)
        self.skipButton.grid(row=11, column=2, rowspan=2)

        # The filename
        self.filenameLabel.grid(row=13, column=0)
        self.filenameField.grid(row=13, column=1, columnspan=3)

        # The tags
        self.tagsLabel.grid(row=14, column=0)
        self.tagsField.grid(row=14, column=1, columnspan=3)

        # The description
        self.descriptionLabel.grid(row=15, column=0)
        self.descriptionField.grid(row=15, column=1, columnspan=3)
        self.descriptionScrollbar.grid(row=15, column=5)
        

    def getImage(self, photo, width, height):
        ''' Take the StringIO object and build an imageTK thumbnail '''
        image = Image.open(photo)
        image.thumbnail((width, height))
        imageTk = ImageTk.PhotoImage(image)
        return imageTk

    def okFile(self):
        ''' The user pressed the OK button. '''
        self.filename=self.filenameField.get()
        self.photoDescription=self.descriptionField.get(0.0, END)
        self.root.destroy()

    def skipFile(self):
        ''' The user pressed the Skip button. '''
        self.skip=True
        self.root.destroy()

    def run(self):
        ''' Activate the dialog and return the new name and if the image is
        skipped.

        '''
        self.root.mainloop()
        return (self.photoDescription, self.filename, self.skip)


def getPhotoIds(flickr=None, user_id=u'', group_id=u'', photoset_id=u'',
              start_id='', end_id='', tags=u''):
    ''' Loop over a set of Flickr photos. '''
    result = []
    retry = False
    if not start_id:
        found_start_id=True
    else:
        found_start_id=False

    # http://www.flickr.com/services/api/flickr.groups.pools.getPhotos.html
    # Get the photos in a group
    if group_id:
        #First get the total number of photo's in the group
        photos = flickr.groups_pools_getPhotos(group_id=group_id,
                                               user_id=user_id, tags=tags,
                                               per_page='100', page='1')
        pages = photos.find('photos').attrib['pages']

        for i in range(1, int(pages) + 1):
            gotPhotos = False
            while not gotPhotos:
                try:
                    for photo in flickr.groups_pools_getPhotos(
                        group_id=group_id, user_id=user_id, tags=tags,
                        per_page='100', page=i
                        ).find('photos').getchildren():
                        gotPhotos = True
                        if photo.attrib['id']==start_id:
                            found_start_id=True
                        if found_start_id:
                            if photo.attrib['id']==end_id:
                                pywikibot.output('Found end_id')
                                return
                            else:
                                yield photo.attrib['id']

                except flickrapi.exceptions.FlickrError:
                    gotPhotos = False
                    pywikibot.output(u'Flickr api problem, sleeping')
                    time.sleep(30)

    # http://www.flickr.com/services/api/flickr.photosets.getPhotos.html
    # Get the photos in a photoset
    elif photoset_id:
        photos = flickr.photosets_getPhotos(photoset_id=photoset_id,
                                            per_page='100', page='1')
        pages = photos.find('photoset').attrib['pages']

        for i in range(1, int(pages)+1):
            gotPhotos = False
            while not gotPhotos:
                try:
                    for photo in flickr.photosets_getPhotos(
                        photoset_id=photoset_id, per_page='100', page=i
                        ).find('photoset').getchildren():
                        gotPhotos = True
                        if photo.attrib['id']==start_id:
                            found_start_id=True
                        if found_start_id:
                            if photo.attrib['id']==end_id:
                                pywikibot.output('Found end_id')
                                return
                            else:
                                yield photo.attrib['id']

                except flickrapi.exceptions.FlickrError:
                    gotPhotos = False
                    pywikibot.output(u'Flickr api problem, sleeping')
                    time.sleep(30)

    # http://www.flickr.com/services/api/flickr.people.getPublicPhotos.html
    # Get the (public) photos uploaded by a user
    elif user_id:
        photos = flickr.people_getPublicPhotos(user_id=user_id,
                                               per_page='100', page='1')
        pages = photos.find('photos').attrib['pages']
        #flickrapi.exceptions.FlickrError
        for i in range(1, int(pages)+1):
            gotPhotos = False
            while not gotPhotos:
                try:
                    for photo in flickr.people_getPublicPhotos(
                        user_id=user_id, per_page='100', page=i
                        ).find('photos').getchildren():
                        gotPhotos = True
                        if photo.attrib['id'] == start_id:
                            found_start_id=True
                        if found_start_id:
                            if photo.attrib['id'] == end_id:
                                pywikibot.output('Found end_id')
                                return
                            else:
                                yield photo.attrib['id']

                except flickrapi.exceptions.FlickrError:
                    gotPhotos = False
                    pywikibot.output(u'Flickr api problem, sleeping')
                    time.sleep(30)

    return

def getPhotos(flickr=None, user_id=u'', group_id=u'', photoset_id=u'',
              start_id='', end_id='', tags=u''):

    for photo_id in getPhotoIds(flickr, user_id, group_id, photoset_id,
                                  start_id, end_id, tags):
        yield getPhoto(flickr, photo_id)
    return

def usage():
    '''
    Print usage information

    TODO : Need more.
    '''
    pywikibot.output(
        u"Flickrripper is a tool to transfer flickr photos to Wikimedia Commons")
    pywikibot.output(u"-group_id:<group_id>\n")
    pywikibot.output(u"-photoset_id:<photoset_id>\n")
    pywikibot.output(u"-user_id:<user_id>\n")
    pywikibot.output(u"-tags:<tag>\n")
    return

def main():
    site = pywikibot.getSite(u'commons', u'commons')
    pywikibot.setSite(site)
    #imagerecat.initLists()

    #Get the api key
    if config.flickr['api_key']:
        flickr = flickrapi.FlickrAPI(config.flickr['api_key'])
    else:
        pywikibot.output('Flickr api key not found! Get yourself an api key')
        pywikibot.output(
            'Any flickr user can get a key at http://www.flickr.com/services/api/keys/apply/')
        return

    group_id = u''
    photoset_id = u''
    user_id = u''
    start_id= u''
    end_id=u''
    tags = u''
    addCategory = u''
    removeCategories = False
    autonomous = False
    totalPhotos = 0
    uploadedPhotos = 0
    json_in = False
    json_out = False
    imagedir = False
    action = 3

    # Do we mark the images as reviewed right away?
    if config.flickr['review']:
        flickrreview = config.flickr['review']
    else:
        flickrreview = False

    # Set the Flickr reviewer
    if config.flickr['reviewer']:
        reviewer = config.flickr['reviewer']
    elif 'commons' in config.sysopnames['commons']:
        print config.sysopnames['commons']
        reviewer = config.sysopnames['commons']['commons']
    elif 'commons' in config.usernames['commons']:
        reviewer = config.usernames['commons']['commons']
    else:
        reviewer = u''

    # Should be renamed to overrideLicense or something like that
    override = u''
    for arg in pywikibot.handleArgs():
        if arg.startswith('-group_id'):
            if len(arg) == 9:
                group_id = pywikibot.input(u'What is the group_id of the pool?')
            else:
                group_id = arg[10:]
        elif arg.startswith('-photoset_id'):
            if len(arg) == 12:
                photoset_id = pywikibot.input(u'What is the photoset_id?')
            else:
                photoset_id = arg[13:]
        elif arg.startswith('-user_id'):
            if len(arg) == 8:
                user_id = pywikibot.input(
                    u'What is the user_id of the flickr user?')
            else:
                user_id = arg[9:]
        elif arg.startswith('-start_id'):
            if len(arg) == 9:
                start_id = pywikibot.input(
                    u'What is the id of the photo you want to start at?')
            else:
                start_id = arg[10:]
        elif arg.startswith('-end_id'):
            if len(arg) == 7:
                end_id = pywikibot.input(
                    u'What is the id of the photo you want to end at?')
            else:
                end_id = arg[8:]
        elif arg.startswith('-tags'):
            if len(arg) == 5:
                tags = pywikibot.input(
                    u'What is the tag you want to filter out (currently only one supported)?')
            else:
                tags = arg[6:]
        elif arg == '-flickrreview':
            flickrreview = True
        elif arg.startswith('-reviewer'):
            if len(arg) == 9:
                reviewer = pywikibot.input(u'Who is the reviewer?')
            else:
                reviewer = arg[10:]
        elif arg.startswith('-override'):
            if len(arg) == 9:
                override = pywikibot.input(u'What is the override text?')
            else:
                override = arg[10:]
        elif arg.startswith('-addcategory'):
            if len(arg) == 12:
                addCategory = pywikibot.input(
                    u'What category do you want to add?')
            else:
                addCategory = arg[13:]
        elif arg == '-removecategories':
            removeCategories = True
        elif arg == '-autonomous':
            autonomous = True
        elif arg.startswith('-jsonin'):
            if len(arg) == 7:
                json_in = pywikibot.input(
                    u'What json file do you want to read from?')
            else:
                json_in = arg[8:]
        elif arg.startswith('-jsonout'):
            if len(arg) == 8:
                json_out = pywikibot.input(
                    u'What json file do you want to write to?')
            else:
                json_out = arg[9:]
            json_out = io.open(json_out, 'wb')
            json_out.write('[')
        elif arg.startswith('-action'):
            if len(arg) == 7:
                action = pywikibot.input(
                    u'What action do you want to perform (read/showurl/download/upload)?')
            else:
                action = arg[8:]
            action = { 'read': 0, 'showurl': 1, 'download': 2, 'upload': 3, 'error': -1 }.get(action, 'error')
            if action == -1:
                pywikibot.output(u'Wrong action given')
                return

        elif arg.startswith('-imagedir'):
            if len(arg) == 9:
                imagedir = pywikibot.input(
                    u'Which folder should be used to save/load the images?')
            else:
                imagedir = arg[10:]
        else:
            pywikibot.output(u'Bad argument `%s\' given' % arg)
            return        
			
    if group_id == u'':
        group_id = ripper_config['group']

    iterator = None
    if json_in:
        f = io.open(json_in, 'r')
        iterator = iter(json.load(f))
        f.close()
    elif user_id or group_id or photoset_id:
        iterator = iter(getPhotos(flickr, user_id, group_id, photoset_id,
                                  start_id, end_id, tags))
    else:
        usage()
        return
     
    first = True
    for photo in iterator:
        if json_out:
            if not first:
                json_out.write(',\n')
            json_out.write(json.dumps(photo))
            first = False
        
        if action == 1:
			print photo['url']
        
        if action >= 2:
            if isAllowedLicense(photo) or override:
                photoStream = downloadPhoto(photo['url'], imagedir)
                
                if action >= 3:
                    uploadedPhotos += processPhoto(photo, photoStream, flickrreview,
                                           reviewer, override, addCategory,
                                           removeCategories, autonomous)
            totalPhotos += 1
    
    if json_out:
        json_out.write(']')
        json_out.close()
    
    pywikibot.output(u'Finished running')
    pywikibot.output(u'Total photos: ' + str(totalPhotos))
    pywikibot.output(u'Uploaded photos: ' + str(uploadedPhotos))

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
