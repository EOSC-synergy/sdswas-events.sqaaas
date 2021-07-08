from plone.dexterity.browser.view import DefaultView
from plone import api
import datetime as dt
from Products.AdvancedQuery import  Eq, Le, In, Ge, MatchGlob
from plone.batching import Batch
from sdswas.customViews.browser.NewsletterForm import NewsletterForm
from pytz import UTC as utc

class EventListView(DefaultView):

    def update(self):
        ## Disable all portlets
        super(DefaultView, self).update()
        self.request.set('disable_plone.rightcolumn',1)
        self.request.set('disable_plone.leftcolumn',1)

    def past_events(self, searchableText, b_size, b_start):
        ## Returns past generic events and webinars that contains "text" in any field with indexer "SearchableText"

        searchParams = {
            "path": "/".join(self.context.getPhysicalPath()), # Limit the search to the current folder and its children
            "portal_type": ["generic_event",  "webinar"],
            "review_state": "published",
            "end": {'query':dt.datetime.now(),
                    'range':'max'},
            "sort_on": ["start", "sortable_title"],
            "sort_order": ["descending", "ascending"]
        }

        if (searchableText): searchParams[ "SearchableText"] = searchableText

        events = self.context.portal_catalog(searchParams)

        results = []
        for event in events:
            resObj = event.getObject()
            results.append({
                'title': resObj.Title(),
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'lead_image_url': resObj.absolute_url(),
                'event_type': resObj.portal_type
            })

        results = Batch(results, size=b_size, start=b_start, orphan=0)

        return results

    def upcoming_events(self):
        now = dt.datetime.utcnow()
        clausetype = Eq("portal_type", "generic_event") | Eq("portal_type", "webinar")
        not_finished = ~ Le("end", now) # in progress
        ready_to_publish = Eq("review_state", "published")
        query = clausetype & not_finished & ready_to_publish & Eq("effectiveRange", now)
        events = self.context.portal_catalog.evalAdvancedQuery(query, (('start','asc'),('sortable_title', 'asc')))
        return events

    def upcoming_events_all(self):
        ## Returns generic events and webinars that satisfy: starting or to_be_started | started & not_finished
        ##effectiveRange return only objects whose effective_date is in the past and effective_date has been introduced in UTC in the system*/
        results = []
        events = self.upcoming_events()
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

    def events_folder_url(self):
        events_folder = api.portal.get().unrestrictedTraverse("news-events/events")
        return events_folder.absolute_url_path()

    def upcoming_events_subset(self, numitems):
        ## Returns the next 'numitems' upcoming events (both generic events and webinars), sorted by date ascendantly
        results = []
        all_events =  self.upcoming_events()
        latests = self.upcoming_events()[:numitems]
        for event in latests:
            resObj = event.getObject()
            results.append({
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'Title': resObj.Title,
            })

        return results

    def pastevents_url(self):
        ###Returns the absolute link to the Past Events view
        url = ""
        url = api.portal.get().unrestrictedTraverse("news-events/events").absolute_url_path() + "/@@eventslist_past"
        return url

    def subscribe_link(self):
       return NewsletterForm.subscribe_link(self)
