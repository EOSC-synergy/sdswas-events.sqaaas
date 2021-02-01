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

        return events

    def past_events_all(self):
        events = self.past_events()
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
                'event_type': resObj.portal_type
            })
        return results

    def past_events_batch(self, start, size):

        events = self.past_events()
        results = []
        batch = events[start:size]
        for event in batch:
            resObj = event.getObject()
            results.append({
                'title': resObj.Title(),
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'lead_image_url': resObj.absolute_url(),
                'end': resObj.end,
                'event_type': resObj.portal_type
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
                'event_type': resObj.portal_type
            })

        return results

    def resources_page_url(self):
        ###Returns the absolute link to the Resources page
        portal = api.portal.get()
        resource_folder = portal.unrestrictedTraverse("resources")
        return resource_folder.absolute_url_path()

    def highlighted_upcoming_events(self):
        ## Returns generic events and webinars with categorization "highlighted-home" sorted by date descendantly
        events = self.context.portal_catalog(
                 portal_type=["generic_event","webinar"],
                review_state="published",
                Subject=["highlighted-home"],
                end= {'query':dt.date.today(),
                    'range':'min'},
                sort_on=["start"], ###second criteria should be "sortable_title"
                sort_order="descending")

        results = []
        for event in events:
            resObj = event.getObject()
            results.append({
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'description': resObj.description,
            })

        return results