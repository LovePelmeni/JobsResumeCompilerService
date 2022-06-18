from rest_framework import negotiation



class CVNegotiationContentClass(negotiation.BaseContentNegotiation):

    def select_renderer(self, request, renderers, format_suffix=None):
        content_type = request.headers.get('Content-Type')
        for renderer in renderers:
            if content_type in renderer.allowed_media_types:
                return renderer


