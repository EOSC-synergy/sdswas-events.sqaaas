from plone.dexterity.browser.view import DefaultView
from plone import api
import datetime as dt
from Products.AdvancedQuery import  Eq, Le, In, Ge, MatchGlob
from plone.batching import Batch

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
            "sort_on": ["start"], ###second criteria should be "sortable_title"
            "sort_order": "desc"
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
        ## Returns generic events and webinars that satisfy: starting or to_be_started | started & not_finished

        now = dt.date.today()
        path = "/".join(self.context.getPhysicalPath()) # Limit the search to the current folder and its children
        clausepath = Eq("path", path)
        clausetype = Eq("portal_type", "generic_event") | Eq("portal_type", "webinar")
        starting_or_to_be_started = Ge("start", now) #start now or in the future
        started = ~ Ge("start", now)
        not_finished = ~ Le("end", now) # in progress
        query = clausepath & clausetype & (starting_or_to_be_started | started & not_finished) & Eq("review_state", "published")

        # The following result variable contains iterable of CatalogBrain objects
        events = self.context.portal_catalog.evalAdvancedQuery(query, (('start','asc'),))

        results = []
        for event in events:
            resObj = event.getObject()
            results.append({
                'title': resObj.Title(),
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'event_start_date_gcalendar': resObj.start.strftime('%Y%m%d'),
                'event_end_date_gcalendar': resObj.end.strftime('%Y%m%d'),
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

    def upcoming_events_subset(self, numitems):
        ## Returns the next 'numitems' upcoming events (both generic events and webinars), sorted by date ascendantly
        events = self.context.portal_catalog(
                 portal_type=["generic_event","webinar"],
                review_state="published",
                end= {'query':dt.date.today(),
                    'range':'min'},
                sort_on=["start"], ###second criteria should be "sortable_title"
                sort_order="ascending")

        results = []
        latests = events[:3]
        for event in latests:
            resObj = event.getObject()
            results.append({
                'event_start_date': resObj.start.strftime('%-d %B %Y'),
                'event_start_date_gcalendar': resObj.start.strftime('%Y%m%d'),
                'absolute_url': resObj.absolute_url(),
                'location': resObj.location,
                'description': resObj.description,
            })

        return results

    def pastevents_url(self):
        ###Returns the absolute link to the Past Events view
        url = ""
        url = api.portal.get().unrestrictedTraverse("news-events/events").absolute_url_path() + "/@@eventslist_past"
        return url