from plone.dexterity.browser.view import DefaultView
from plone import api
import datetime as dt

class EventListView(DefaultView):

    def update(self):
        ## Disable all portlets
        super(DefaultView, self).update()
        self.request.set('disable_plone.rightcolumn',1)
        self.request.set('disable_plone.leftcolumn',1)

    def past_events(self):
        ## Returns generic events and webinars with a date older than today
        events = self.context.portal_catalog(
                 portal_type=["generic_event","webinar"],
                review_state="published",
                end= {'query':dt.datetime.now(),
                    'range':'max'},
                sort_on=["start"], ###second criteria should be "sortable_title"
                sort_order="descending")

        results = []
        for event in events:
            resObj = event.getObject()
            results.append({
                'title': resObj.Title(),
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'lead_image_url': resObj.absolute_url(),
                'end': resObj.end,
                'start': resObj.start.strftime('%-d %B %Y')
            })

        return results

    def upcoming_events(self):
        ## Returns generic events and webinars with a date newer or equal to today
        events = self.context.portal_catalog(
                 portal_type=["generic_event","webinar"],
                review_state="published",
                end= {'query':dt.date.today(),
                    'range':'min'},
                sort_on=["start"], ###second criteria should be "sortable_title"
                sort_order="descending",
                sort_limit = 3)

        results = []
        for event in events:
            resObj = event.getObject()
            results.append({
                'title': resObj.Title(),
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'lead_image_url': resObj.absolute_url(),
                'end': resObj.end,
                'start': resObj.start.strftime('%Y%m%d'),
            })

        return results

    def resources_page_url(self):
        ###Returns the absolute link to the Resources page
        portal = api.portal.get()
        resource_folder = portal.unrestrictedTraverse("resources")
        return resource_folder.absolute_url_path()

