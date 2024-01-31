from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from accounts.models import ManagerProfile, User
from property.models import Property, Feature, PropertyType



@registry.register_document
class PropertyDocument(Document):

    features = fields.NestedField(
        properties={
            'name': fields.TextField(),
        })
    
    property_type = fields.NestedField(
        properties={
            'name': fields.TextField(),
        })

    class Index:
        # Name of the Elasticsearch index
        name = 'properties'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Property # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'address',
            'description',
            'city',
            'state',
            'zip_code',
            'country',
            'price_per_night',
            'parlours',
            'bedrooms',
            'bathrooms',
            'guests_capacity',
        ]
    #     related_models = [Feature, PropertyType]  # Optional: to ensure the property will be re-saved when Feature or PropertyType is updated

    # # def get_queryset(self):
    # #     """Not mandatory but to improve performance we can select related in one sql request"""
    # #     return super(PropertyDocument, self).get_queryset().select_related(
    # #         'property_manager'
    # #     )

    # def get_instances_from_related(self, related_instance):
    #     """If related_models is set, define how to retrieve the Property instance(s) from the related model.
    #     The related_models option should be used with caution because it can lead in the index
    #     to the updating of a lot of items.
    #     """
    #     if isinstance(related_instance, Feature):
    #         return related_instance.properties
    #     elif isinstance(related_instance, PropertyType):
    #         return related_instance.properties






@registry.register_document
class UserDocument(Document):

    managers = fields.NestedField(properties={
        'company_name': fields.TextField(),
        'properties_managed': fields.TextField(),
        'about': fields.TextField(),
    })

    # renters = fields.NestedField(properties={
    #     'occupation': fields.TextField(),
    #     'job_title': fields.TextField(),
    # })

    class Index:
        # Name of the Elasticsearch index
        name = 'users'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = User # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'username',
            'first_name',
            'last_name',
            'gender',
            # 'phone_number'
        ]
        related_models=[ManagerProfile]


    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Property instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, ManagerProfile):
            return related_instance.manager
        # elif isinstance(related_instance, PropertyType):
        #     return related_instance.properties





        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Configure how the index should be refreshed after an update.
        # See Elasticsearch documentation for supported options:
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-refresh.html
        # This per-Document setting overrides settings.ELASTICSEARCH_DSL_AUTO_REFRESH.
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000