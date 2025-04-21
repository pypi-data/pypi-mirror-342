class EcosystemPatternRepository:
    """Repository of patterns that identify ecosystem relationships, builders, and collaboration"""

    def __init__(self):
        # Domains commonly associated with ecosystem and project showcases
        self.ecosystem_domains = [
            "showcase.",
            "ecosystem.",
            "community.",
            "gallery.",
            "partners.",
            "developers.",
            "marketplace.",
            "expo.",
            "apps.",
            "extensions.",
            "plugins.",
        ]

        # URL path patterns indicating ecosystem/builder content
        self.ecosystem_path_patterns = [
            r"/ecosystem/",
            r"/showcase/",
            r"/community/",
            r"/built-with/",
            r"/case-studies/",
            r"/customers/",
            r"/partners/",
            r"/users/",
            r"/success-stories/",
            r"/integrations/",
            r"/extensions/",
            r"/marketplace/",
            r"/plugins/",
            r"/addons/",
            r"/gallery/",
            r"/examples/",
            r"/projects/",
            r"/contributors/",
            r"/whos-using/",
        ]

        # Link text patterns suggesting ecosystem content
        self.ecosystem_text_patterns = [
            r"(?i)ecosystem",
            r"(?i)showcase",
            r"(?i)built with",
            r"(?i)powered by",
            r"(?i)case stud(y|ies)",
            r"(?i)success stor(y|ies)",
            r"(?i)who('s| is) using",
            r"(?i)our users",
            r"(?i)our customers",
            r"(?i)integrations?",
            r"(?i)extensions?",
            r"(?i)plugins?",
            r"(?i)addons?",
            r"(?i)community projects",
            r"(?i)community contributions",
            r"(?i)user contributions",
            r"(?i)featured projects",
            r"(?i)gallery",
        ]

        # Header/title patterns suggesting ecosystem sections
        self.ecosystem_header_patterns = [
            r"(?i)ecosystem",
            r"(?i)who('s| is) using",
            r"(?i)built (on|with)",
            r"(?i)powered by",
            r"(?i)trusted by",
            r"(?i)customer(s| success)",
            r"(?i)case stud(y|ies)",
            r"(?i)success stor(y|ies)",
            r"(?i)showcase",
            r"(?i)featured (users|customers|projects)",
            r"(?i)community (projects|showcase)",
            r"(?i)partner(s| program)",
            r"(?i)(our|notable) users",
            r"(?i)companies using",
            r"(?i)in production",
            r"(?i)contributor(s| showcase)",
            r"(?i)extension (gallery|showcase)",
            r"(?i)plugin (directory|marketplace)",
            r"(?i)apps? (built|marketplace|gallery)",
        ]

        # Content phrases that suggest ecosystem descriptions
        self.ecosystem_content_patterns = [
            r"(?i)built (on|with) (our|this)",
            r"(?i)(companies|organizations|projects) (using|powered by)",
            r"(?i)(is|are) using (our|this)",
            r"(?i)powered by (our|this)",
            r"(?i)extend(s|ing)? (the|our) (platform|ecosystem)",
            r"(?i)integrated with",
            r"(?i)build(s|ing)? (on top of|with)",
            r"(?i)leverage(s|ing)? (our|this)",
            r"(?i)extend(s|ing)? (the|our) (functionality|capabilities)",
            r"(?i)based on (our|this)",
            r"(?i)implemented (with|using)",
            r"(?i)developed (with|using)",
            r"(?i)(join|be part of) (our|the) ecosystem",
        ]

        # Builder and contribution-specific patterns
        self.builder_patterns = [
            r"(?i)how to (build|contribute)",
            r"(?i)build(ing)? (with|on)",
            r"(?i)develop(ing)? (with|on)",
            r"(?i)contribute to",
            r"(?i)contributor guide",
            r"(?i)developer program",
            r"(?i)join (our|the) (ecosystem|community)",
            r"(?i)become a (contributor|partner)",
            r"(?i)extend (our|the) (platform|ecosystem)",
            r"(?i)create (your own|an?) (plugin|extension|integration)",
            r"(?i)developer (resources|portal)",
            r"(?i)sdk",
            r"(?i)api (access|integration)",
            r"(?i)partner (program|portal)",
        ]

        # Visual cues that often indicate ecosystem showcases
        self.visual_indicators = [
            r"logo grid",
            r"logo carousel",
            r"client logos",
            r"partner logos",
            r"customer logos",
            r"company logos",
            r"card gallery",
            r"project cards",
            r"showcase gallery",
            r"case study cards",
            r"testimonials",
            r"user testimonials",
        ]

        # Collaboration-specific patterns
        self.collaboration_patterns = [
            r"(?i)how to collaborate",
            r"(?i)collaboration (guide|opportunities)",
            r"(?i)working together",
            r"(?i)partner(ship|ing) (opportunities|program)",
            r"(?i)join (our|the) (community|ecosystem)",
            r"(?i)community (contribution|participation)",
            r"(?i)open (source|collaboration)",
            r"(?i)contribute (code|documentation|resources)",
            r"(?i)become a (partner|contributor|maintainer)",
            r"(?i)collaboration (framework|model)",
            r"(?i)(business|technical) partnership",
            r"(?i)developer relations",
            r"(?i)community (engagement|involvement)",
        ]

        # Key meta tags that might indicate ecosystem content
        self.meta_tag_patterns = [
            r"(?i)ecosystem",
            r"(?i)showcase",
            r"(?i)community",
            r"(?i)partner program",
            r"(?i)integration",
            r"(?i)extension",
            r"(?i)plugin",
            r"(?i)marketplace",
            r"(?i)collaboration",
            r"(?i)use cases",
            r"(?i)case studies",
            r"(?i)success stories",
        ]

        # Schema.org types that often indicate ecosystem relationships
        self.schema_types = [
            "Product",
            "SoftwareApplication",
            "Organization",
            "BusinessPartner",
            "ProgramMembership",
            "CreativeWork",
            "SoftwareSourceCode",
            "WebApplication",
        ]