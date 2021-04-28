from plone.dexterity.browser.view import DefaultView
import datetime as dt
import re
from pytz import UTC as utc
import locale
from plone.batching import Batch
from plone.namedfile import NamedBlobFile
from plone import api
import transaction
import shutil, os

class EventView(DefaultView):

    def update(self):

        locale.setlocale(locale.LC_TIME,"en_US.UTF-8")

        ## Disable all portlets
        super(DefaultView, self).update()
        self.request.set('disable_plone.rightcolumn',1)
        self.request.set('disable_plone.leftcolumn',1)


    def language(self):
        ##Display value of the field language
        value = self.context.event_language
        display_value =  value if value else "-"
        return display_value

    def start(self):
        ##Display value of the field start (from event behaviour)
        return self.context.start.strftime('%-d %B %Y')

    def time(self):

        if (self.context.whole_day): return 'Whole day'

        if (not(self.context.end) and not(self.context.start)): return '-'

        start_display = self.context.start.replace(tzinfo=utc).strftime('%H:%M')
        end_display = self.context.end.replace(tzinfo=utc).strftime('%H:%M')

        if (self.context.open_end):
            return start_display +" UTC - open"

        if (self.context.end):
            diff = self.context.end - self.context.start
            if (diff.days >= 1): return '-'

        return start_display + " - " + end_display + " UTC"

    def duration(self):
        ##Display value of the field Duration (computed from the event's start and end fields)
        if (not(self.context.start) or not(self.context.end)): return '-'

        if (self.context.open_end):
            return 'Open end'

        timedelta = self.context.end - self.context.start
        #Compute difference in hours and
        days = timedelta.days
        seconds = timedelta.seconds
        hours = seconds//3600
        minutes = (seconds//60)%60
        result = ''
        if (days == 0):
            #Single day event: Compute duration in hours and minutes if the whole day option has not been set
            if (self.context.whole_day):
                result = '1 day'
            else:
                result = str(hours) + ' h '

                if minutes > 0:
                    result += str(minutes) + ' m'
        else:
            #Multiple day event: Compute duration in days
            days += 1
            result = str(days) + ' day'
            if (days > 1): result += 's'
        return result

    def downloadfile_url(self):
        if (self.context.document):
            return self.context.absolute_url()+"/@@download/document/"+self.context.document.filename
        else:
            return ""

    def embedded_url(self):
        ## Returns the URL stored in the field embedded_url to be used as the source URL of the video field
        ## If it is not a valid youtube embed URL then convert it
        url = self.context.embedded_url

        ##If it is a Youtube URL, process it to generate the embed URL
        regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
        match = regex.match(url)
        if match:
            url = "https://www.youtube.com/embed/"+match.group('id')
        return url

    def images(self):

        if not(self.context.has_key("pictures")): return None

        brains = self.context["pictures"].getFolderContents(contentFilter={"portal_type" : "Image"})

        results = []
        for brain in brains:
            resObj = brain.getObject()
            results.append({
             'title': resObj.Title(),
             'absolute_url': resObj.absolute_url()
            })

        return results

    def is_upcoming(self):
       return  self.context.end.replace(tzinfo=utc) > dt.datetime.now(utc)

    def presentations(self, searchableText, b_size, b_start):

        if not(self.context.has_key("presentations")): return None

        searchParams = {
            "portal_type" : "presentation",
            "review_state": "published"
            #"sort_on": ["getPresentationDate"], ##this index needs to be created and the second criteria should be "sortable_title"
            #"sort_order": "descending"
            }

        if (searchableText): searchParams[ "SearchableText"] = searchableText

        brains = self.context["presentations"].getFolderContents(contentFilter=searchParams)

        results = []
        for brain in brains:
            resObj = brain.getObject()
            results.append({
            'title': resObj.Title(),
            'absolute_url': resObj.absolute_url(),
            'author': resObj.author,
            'presentation_date': resObj.presentationDate.strftime('%-d %B %Y'),
            'doc_filepath': resObj.absolute_url()+"/@@download/document/"+resObj.document.filename
            })

        results = Batch(results, size=b_size, start=b_start, orphan=0)

        return results

    def numPresentations(self):

        if not(self.context.has_key("presentations")): return 0

        brains = self.context["presentations"].getFolderContents(
            contentFilter={
                "portal_type" : "presentation",
                "review_state": "published"})

        return len(brains)

    def presentations_zip_link(self):
    # Return URL of the zip file containing the event's presentations folder.
    # Check if it has already been generated and it is not outdated, otherwise create it
    # The zip is a plone File stored in the event's dir with name "presentations-zip"

        if not(self.context.has_key("presentations")): return ""

        zipurl = ""
    #  try:
        files = self.context.getFolderContents(
            contentFilter=  {
                "portal_type" : "File",
                "title": "presentations-zip"})

        generate_zip = False

        if (len(files)):
            # Regenerate zip if the folder has been modified (added/removed entries)
            # or any presentation is newer than the zip

            zip = files[0].getObject() # There should be only one file with this name
            folder_modified = self.context["presentations"].modified()
            if folder_modified > zip.modified(): #folder modified (added/removed entries)
                #print("Presentations zip is outdated: folder is newer (",folder_modified,") than the zip (", zip.modified(),")")
                generate_zip = True
            else:
                presentations = self.context["presentations"].getFolderContents(
                    contentFilter={
                        "portal_type" : "presentation",
                        "review_state": "published"})

                for item in presentations:
                    item_modified = item.getObject().modified()
                    if item_modified > zip.modified():
                        #print("Presentations zip is outdated: found at least one presentation with date newer (",item_modified,") than the zip (", zip.modified(),")")
                        generate_zip = True

            if generate_zip: #Zip is outdated: delete it
                #print("Deleting zip file:", zip.absolute_url())
                zip.aq_parent.manage_delObjects([zip.getId()])
                transaction.commit()

        else: #Zip does not exist
            print("zip no exist")
            generate_zip = True

        zipurl = self.generate_presentations_zip() if generate_zip else zip.absolute_url() + '/@@download'

    #    except Exception as e:
     #       print("Error getting link to the presentations zip of event ",self.context.title, ":",e)

        return zipurl

    def generate_presentations_zip(self):
    # Return the link to the presentations zip. If it does not exist, generate it.
    # The zip is Plone file stored in the event's folder with title self.context.presentations_zipname.

        if not(self.context.has_key("presentations")): return ""

        brains = self.context["presentations"].getFolderContents(
            contentFilter=  {
                "portal_type" : "presentation",
                "review_state": "published"})

        # Create folder for this event if it does not exist
        dirname = u'{0}-presentations'.format(self.context.id)
        print("---------- Generating zip of event presentations folder for event with title: '",self.context.title,"'----------")

        currentpath = os.getcwd()
        zipurl = ""
        try:
            os.chdir('/tmp')

            if os.path.exists(dirname):
                shutil.rmtree(dirname)

            os.mkdir(dirname)

            #Insert files in the folder
            for brain in brains:
                resObj = brain.getObject()
                filedoc = resObj.document
                filename = filedoc.filename
                f = open(os.path.join(dirname, filename), 'wb')
                f.write(filedoc.data)
                f.close()
                #print("Saved {}".format(filename))

            #Zip the folder, delete the folder, create a plone File with the zip folder and remove zip folder from the file system
            shutil.make_archive(dirname, 'zip',dirname)
            shutil.rmtree(dirname)
            zipurl = self.upload_zip(dirname)
        finally:
            os.chdir(currentpath)

        return zipurl

    def upload_zip(self, filename):
    # Upload zip file fylesystem dir (/tmp) to the current Plone context
    # The zip filename is "filename"

        zip_filename = "{}.zip".format(filename)

        zip_file = api.content.create(
            type='File',
            title=u'presentations-zip',
            container=self.context,
        )

        try:
            f = open(zip_filename, 'rb')
        except IOError:
            print("Error: Zip file can't be uploaded to Plone, it does not appear to exist.")
            return 0

        zip_file.file = NamedBlobFile(
            data=f,
            filename=zip_filename,
            contentType='application/zip'
        )

        f.close()
        zip_file.reindexObject()
        transaction.commit()
        return zip_file.absolute_url() + '/@@download'

