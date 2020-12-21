from plone.dexterity.browser.view import DefaultView

class PresentationView(DefaultView):

    def update(self):
        ## Disable all portlets
        super(DefaultView, self).update()
        self.request.set('disable_plone.rightcolumn',1)
        self.request.set('disable_plone.leftcolumn',1)

    def presentationDate(self):
        ##Display value of the field start (from event behaviour)
        return self.context.presentationDate.strftime('%-d %B %Y')