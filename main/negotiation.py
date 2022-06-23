from rest_framework import negotiation



class CVNegotiationContentClass(negotiation.BaseContentNegotiation):

    def select_renderer(self, request, renderers, format_suffix=None):
        pass

