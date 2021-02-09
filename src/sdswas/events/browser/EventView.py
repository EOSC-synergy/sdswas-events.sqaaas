from plone.dexterity.browser.view import DefaultView
import datetime as dt
import re
from pytz import UTC as utc
import locale

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

        if (self.context.open_end):
            return self.context.start.strftime('%H:%M') +" GMT - open"

        if (self.context.end):
            diff = self.context.end - self.context.start
            if (diff.days >= 1): return '-'

        return self.context.start.strftime('%H:%M') + " - " + self.context.end.strftime('%H:%M') + " GMT"

    def duration(self):
        ##Display value of the field Duration (computed from the event's start and end fields)
        if (not(self.context.start) or not(self.context.end)): return '-'

        if (self.context.open_end):
            return 'Open end'

        diff = self.context.end - self.context.start
        days = diff.days
        result = ''

        if days > 0:
            result = str(days) + ' day'
            if days > 1: result += 's'
        else:
            hours, minutes = divmod(diff.seconds,60*60)

            result = ''
            if hours > 0:
                result = str(hours) + ' h '

            if minutes > 0:
                result += str(int(minutes/60)) + ' m'

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

        brains = self.context.getFolderContents(contentFilter={"portal_type" : "Image"})
        results = []
        for brain in brains:
            resObj = brain.getObject()
            results.append({
             'title': resObj.Title(),
             'absolute_url': resObj.absolute_url()
            })
        return results

    def is_upcoming(self):
        return self.context.start >= utc.localize(dt.datetime.now())

    def presentations(self):
        brains = self.context.portal_catalog(
            path = {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1},
            portal_type=["presentation"],
            review_state="published",
            sort_on=["getPresentationDate"], ###second criteria should be "sortable_title"
            sort_order="descending")

        #brains = self.context.getFolderContents(contentFilter={"portal_type" : "presentation"})
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

        return results

    def numPresentations(self):

        brains = self.context.portal_catalog(
            path = {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1},
            portal_type=["presentation"],
            review_state="published")
        return len(brains)