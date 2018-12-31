import grow
import yaml
from grow import documents
from grow.common import utils
from protorpc import messages


class GrowYamlLocalization(grow.Preprocessor):
    KIND = 'fields-localization'

    class Config(messages.Message):
        tag = messages.StringField(1)
        count = messages.IntegerField(2)
        content_file = messages.StringField(3)

    def __init__(self, *args, **kwargs):
        super(GrowYamlLocalization, self).__init__(*args, **kwargs)

    def get_content(self, path):
        content = self.pod.read_yaml(path)
        return content

    def get_short(self, doc):
        try:
            return doc.short_name
        except AttributeError:
            return doc.pod_path.split("/")[-1][:-5]

    def process_page(self, doc):
        print "Processing: {}".format(doc)
        path = doc.pod_path
        content = self.get_content(path)

        self.rename_property(content, "$title")
        self.rename_property(content, "description")
        self.rename_property(content, "metaTitle")
        self.rename_property(content, "metaDescription")

        for index, section in enumerate(content["sections"]):
            self.localize_section(section)

        self.pod.write_yaml(path, content)

    def localize_section(self, section):
        for attr, value in section.iteritems():
            if isinstance(section[attr], list):
                for component in section[attr]:
                    self.localize_component(component)

    def localize_component(self, component):
        if isinstance(component, dict):
            key_values = list(component.iteritems())
            for attr, value in key_values:
                if isinstance(component[attr], list):
                    for inner_component in component[attr]:
                        self.localize_component(inner_component)
                else:
                    if attr in LOCALIZED_FIELDS and value:
                        self.rename_property(component, attr)

                if attr == 'paragraphs':
                    self.rename_property(component, attr)

    def rename_property(self, segment, attr):
        if attr in segment:
            localized_key = attr + "@"
            segment[localized_key] = segment[attr]
            del segment[attr]

    def mark_groups(self, group):
        self.top_level = self.pod.get_collection(group)
        collections = (collection for collection in self.pod.list_collections() if collection.title not in ("Dev Components", "Shared", "Documentation"))
        for collection in collections:
            docs = [doc for doc in collection.docs() if doc.locale == "en_US"]

            if len(self.tags) > 0:
                docs = [doc for doc in docs if doc.pod_path in self.tags]

            for doc in docs:
                self.process_page(doc)

    def run(self, *args, **kwargs):
        for group in LOCALIZED_GROUPS:
            self.mark_groups(group)

LOCALIZED_GROUPS = [
    "pages"
]

LOCALIZED_FIELDS = [
    "headline",
    "text",
    "label",
    "description",
    "title",
    "error",
    "occupation",
    "quote",
    "paragraphs",
    "eyebrow",
    "subheadline",
    "introduction",
    "goal"
]
