class DocumentationPatternRepository:
    """Repository of patterns that indicate documentation links"""

    def __init__(self):
        # Domain patterns that commonly host documentation
        self.doc_domains = [
            "gitbook.io",
            "readthedocs.io",
            "docs.github.com",
            "developer.mozilla.org",
            "confluence.",
            "zendesk.com",
            "help.",
            "support.",
            "wiki.",
        ]

        # URL path patterns that commonly indicate documentation
        self.doc_path_patterns = [
            r"/docs/",
            r"/documentation/",
            r"/guide/",
            r"/manual/",
            r"/help/",
            r"/knowledge/",
            r"/support/",
            r"/api/",
            r"/reference/",
            r"/wiki/",
        ]

        # Link text patterns that suggest documentation
        self.doc_text_patterns = [
            r"(?i)documentation",
            r"(?i)docs",
            r"(?i)developer guide",
            r"(?i)user guide",
            r"(?i)knowledge base",
            r"(?i)help center",
            r"(?i)manual",
            r"(?i)api reference",
            r"(?i)getting started",
            r"(?i)learn more",
        ]